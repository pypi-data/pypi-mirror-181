from dataclasses import dataclass
import json
import os
from typing import Any, Dict, Optional
from unittest.mock import ANY, call, Mock, patch

import pytest

from anyscale.experimental_integrations import (
    get_aws_secret,
    get_endpoint,
    get_gcp_secret,
    set_wandb_project_group_env_vars,
    WANDB_API_KEY_NAME,
    wandb_get_api_key,
    WANDB_GROUP_NAME,
    WANDB_PROJECT_NAME,
    wandb_send_run_info_hook,
    wandb_setup_api_key_hook,
)
from anyscale.shared_anyscale_utils.utils.protected_string import ProtectedString


@pytest.mark.parametrize(
    "boto3_response",
    [
        {
            "ARN": "arn:aws:secretsmanager:us-west-2:188439194153:secret:my_key_name-V6JDx0",
            "Name": "my_key_name",
            "VersionId": "5a939f56-6566-42e4-9af9-673343aa61cf",
            "SecretString": "my_secret_val",
            "VersionStages": ["AWSCURRENT"],
            "ResponseMetadata": {
                "RequestId": "49887c5a-22e7-4f16-a3bb-e7344189fd1e",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "49887c5a-22e7-4f16-a3bb-e7344189fd1e",
                    "content-type": "application/x-amz-json-1.1",
                    "content-length": "275",
                    "date": "Tue, 08 Nov 2022 21:52:47 GMT",
                },
                "RetryAttempts": 0,
            },
        },
        {
            "ARN": "arn:aws:secretsmanager:us-west-2:188439194153:secret:my_key_name-V6JDx0",
            "Name": "my_key_name",
            "VersionId": "5a939f56-6566-42e4-9af9-673343aa61cf",
            "SecretBinary": "my_secret_val",
            "VersionStages": ["AWSCURRENT"],
            "ResponseMetadata": {
                "RequestId": "49887c5a-22e7-4f16-a3bb-e7344189fd1e",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "49887c5a-22e7-4f16-a3bb-e7344189fd1e",
                    "content-type": "application/x-amz-json-1.1",
                    "content-length": "275",
                    "date": "Tue, 08 Nov 2022 21:52:47 GMT",
                },
                "RetryAttempts": 0,
            },
        },
    ],
)
def test_get_aws_secret(boto3_response: Dict[str, Any]):
    mock_boto3_client = Mock(get_secret_value=Mock(return_value=boto3_response))
    mock_boto3 = Mock(client=Mock(return_value=mock_boto3_client))

    with patch.dict("sys.modules", boto3=mock_boto3):
        secret = get_aws_secret(secret_name="my_key_name", region_name="us-west-2")
        assert isinstance(secret, ProtectedString)
        assert secret._UNSAFE_DO_NOT_USE == "my_secret_val"

    mock_boto3.client.assert_called_once_with("secretsmanager", region_name="us-west-2")
    mock_boto3_client.get_secret_value.assert_called_once_with(SecretId="my_key_name")


def test_get_gcp_secret():
    mock_access_secret_version = Mock(
        return_value=Mock(payload=Mock(data="my_secret_val".encode()))
    )
    mock_secret_manager_client = Mock(access_secret_version=mock_access_secret_version)
    mock_secretmanager = Mock(
        SecretManagerServiceClient=Mock(return_value=mock_secret_manager_client)
    )
    mock_google_auth = Mock(default=Mock(return_value=(ANY, "gcp_project_name")))
    mock_google = Mock(
        auth=mock_google_auth, cloud=Mock(secretmanager=mock_secretmanager)
    )

    with patch.multiple(
        "anyscale.experimental_integrations",
        try_import_gcp_secretmanager=Mock(return_value=mock_secretmanager),
    ), patch.dict("sys.modules", google=mock_google):
        assert (
            get_gcp_secret("my_key_name", key1="val1")._UNSAFE_DO_NOT_USE
            == "my_secret_val"
        )
    mock_secretmanager.SecretManagerServiceClient.assert_called_once_with(key1="val1")
    mock_google_auth.default.assert_called_once()
    mock_access_secret_version.assert_called_once_with(
        request={
            "name": "projects/gcp_project_name/secrets/my_key_name/versions/latest"
        }
    )


@pytest.mark.parametrize("cluster_id", ["mock_cluster_id", ""])
@pytest.mark.parametrize("cloud_provider", ["AWS", "GCP", "invalid_provider"])
@pytest.mark.parametrize("secret_name", ["other_api_key_name", ""])
@pytest.mark.parametrize(
    "cloud_secret_manager_key_match",
    [
        None,
        "anyscale_mock_cloud_id/mock_user_id/wandb_api_key",
        "wandb_api_key_mock_user_id",
        "other_api_key_name",
    ],
)
def test_wandb_get_api_key(
    cluster_id: Optional[str],
    cloud_provider: str,
    secret_name: Optional[str],
    cloud_secret_manager_key_match: Optional[str],
):
    mock_api_client = Mock()
    mock_cluster = Mock(cloud_id="mock_cloud_id", creator_id="mock_user_id")
    mock_api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get = Mock(
        return_value=Mock(result=mock_cluster)
    )
    mock_cloud = Mock(provider=cloud_provider, region="mock_region_name")
    mock_cloud.id = "mock_cloud_id"
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
        return_value=Mock(result=mock_cloud)
    )

    called_secrets = []

    def get_secret(secret_name, **kwargs):
        called_secrets.append(secret_name)
        if (
            cloud_secret_manager_key_match
            and secret_name == cloud_secret_manager_key_match
        ):
            return ProtectedString("my_secret_val")
        raise Exception(f"No key with name {secret_name} in secret manager")

    mock_get_aws_secret = Mock(side_effect=get_secret)
    mock_get_gcp_secret = Mock(side_effect=get_secret)

    with patch.dict(
        os.environ, {WANDB_API_KEY_NAME: secret_name, "ANYSCALE_SESSION_ID": cluster_id}
    ), patch.multiple(
        "anyscale.experimental_integrations",
        get_auth_api_client=Mock(return_value=Mock(api_client=mock_api_client)),
        get_aws_secret=mock_get_aws_secret,
        get_gcp_secret=mock_get_gcp_secret,
    ):
        if (
            (not cluster_id)
            or (cloud_provider not in ["AWS", "GCP"])
            or (not cloud_secret_manager_key_match)
            or (
                cloud_secret_manager_key_match == "other_api_key_name"
                and secret_name != "other_api_key_name"
            )
        ):
            with pytest.raises(Exception):
                wandb_get_api_key()
            return

        assert wandb_get_api_key()._UNSAFE_DO_NOT_USE == "my_secret_val"
    mock_api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get.assert_called_once_with(
        cluster_id
    )
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
        "mock_cloud_id"
    )

    if cloud_provider == "AWS":
        mock_get_aws_secret.assert_has_calls(
            [call(secret, region_name="mock_region_name") for secret in called_secrets]
        )
        mock_get_gcp_secret.assert_not_called()
    elif cloud_provider == "GCP":
        mock_get_gcp_secret.assert_has_calls(
            [call(secret) for secret in called_secrets]
        )
        mock_get_aws_secret.assert_not_called()


def test_wandb_setup_api_key_hook():
    mock_wandb_get_api_key = Mock(return_value=ProtectedString("my_secret_val"))
    mock_set_wandb_project_group_env_vars = Mock()

    with patch.multiple(
        "anyscale.experimental_integrations",
        wandb_get_api_key=mock_wandb_get_api_key,
        set_wandb_project_group_env_vars=mock_set_wandb_project_group_env_vars,
    ):
        assert wandb_setup_api_key_hook() == "my_secret_val"

    mock_wandb_get_api_key.assert_called_once_with()
    mock_set_wandb_project_group_env_vars.assert_called_once_with()


def test_set_wandb_project_group_env_vars_for_prod_job():
    os_env_var_dict = {"ANYSCALE_HA_JOB_ID": "mock_ha_job_id"}
    mock_api_client = Mock()
    mock_production_job = Mock()
    mock_production_job.name = "mock_production_job_name"
    mock_api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get = Mock(
        return_value=Mock(result=mock_production_job)
    )
    mock_slugify = Mock(side_effect=(lambda x: x))
    with patch.dict(os.environ, os_env_var_dict), patch.multiple(
        "anyscale.experimental_integrations",
        get_auth_api_client=Mock(return_value=Mock(api_client=mock_api_client)),
        slugify=mock_slugify,
    ):
        set_wandb_project_group_env_vars()

        assert os.environ[WANDB_PROJECT_NAME] == "anyscale_default_project"
        assert os.environ[WANDB_GROUP_NAME] == "mock_production_job_name"
        mock_slugify.assert_called_once_with("mock_production_job_name")
        mock_api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get.assert_called_once_with(
            os.environ.get("ANYSCALE_HA_JOB_ID")
        )


@pytest.mark.parametrize(
    "os_env_var_dict",
    [
        {},
        {"ANYSCALE_HA_JOB_ID": "mock_ha_job_id"},
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "mock_workspace_id"},
        {
            "RAY_JOB_CONFIG_JSON_ENV_VAR": json.dumps(
                {"metadata": {"job_name": "mock_ray_job_name"}}
            )
        },
        {
            "ANYSCALE_SESSION_ID": "mock_cluster_id",
            "RAY_JOB_CONFIG_JSON_ENV_VAR": json.dumps(
                {"metadata": {"job_name": "mock_ray_job_name"}}
            ),
        },
    ],
)
def test_set_wandb_project_group_env_vars_for_workspace(
    os_env_var_dict: Dict[str, Any]
):
    os_env_var_dict = {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "mock_workspace_id"}
    mock_api_client = Mock()
    mock_workspace = Mock()
    mock_workspace.name = "mock_workspace_name"
    mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get = Mock(
        return_value=Mock(result=mock_workspace)
    )
    mock_slugify = Mock(side_effect=(lambda x: x))
    with patch.dict(os.environ, os_env_var_dict), patch.multiple(
        "anyscale.experimental_integrations",
        get_auth_api_client=Mock(return_value=Mock(api_client=mock_api_client)),
        slugify=mock_slugify,
    ):
        set_wandb_project_group_env_vars()
        assert os.environ[WANDB_PROJECT_NAME] == "mock_workspace_name"
        assert os.environ.get(WANDB_GROUP_NAME) is None
        mock_slugify.assert_called_once_with("mock_workspace_name")
        mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get.assert_called_once_with(
            os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID")
        )


@pytest.mark.parametrize(
    "os_env_var_dict",
    [
        {
            "RAY_JOB_CONFIG_JSON_ENV_VAR": json.dumps(
                {"metadata": {"job_name": "mock_ray_job_name"}}
            )
        },
        {
            "ANYSCALE_SESSION_ID": "mock_cluster_id",
            "RAY_JOB_CONFIG_JSON_ENV_VAR": json.dumps(
                {"metadata": {"job_name": "mock_ray_job_name"}}
            ),
        },
    ],
)
def test_set_wandb_project_group_env_vars_for_ray_job(os_env_var_dict: Dict[str, Any]):
    mock_api_client = Mock()
    Mock()
    mock_cluster = Mock()
    mock_cluster.name = "mock_cluster_name"
    mock_api_client.get_session_api_v2_sessions_session_id_get = Mock(
        return_value=Mock(result=mock_cluster)
    )
    mock_slugify = Mock(side_effect=(lambda x: x))
    with patch.dict(os.environ, os_env_var_dict), patch.multiple(
        "anyscale.experimental_integrations",
        get_auth_api_client=Mock(return_value=Mock(api_client=mock_api_client)),
        slugify=mock_slugify,
    ):
        set_wandb_project_group_env_vars()
        assert (
            os.environ[WANDB_PROJECT_NAME] == "mock_cluster_name"
            if os.environ.get("ANYSCALE_SESSION_ID")
            else "anyscale_default_project"
        )
        assert os.environ[WANDB_GROUP_NAME] == "mock_ray_job_name"
        mock_slugify.assert_called_with("mock_ray_job_name")


@pytest.mark.parametrize("mock_wandb", [Mock(), None])
@pytest.mark.parametrize(
    "os_env_var_dict",
    [
        {"ANYSCALE_HA_JOB_ID": "mock_ha_job_id"},
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "mock_workspace_id"},
    ],
)
def test_wandb_send_run_info_hook(mock_wandb, os_env_var_dict):
    @dataclass
    class MockRun:
        entity: str
        project: str
        group: Optional[str]
        config: Mock = Mock()

        get_project_url: Mock = Mock(return_value="mock_project_url")

    mock_run = MockRun(entity="mock_entity", project="mock_project", group="mock_group")
    if mock_wandb:
        mock_wandb.sdk = Mock(wandb_run=Mock(Run=MockRun))
    mock_api_client = Mock()
    mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get = Mock(
        return_value=Mock(result=Mock(cluster_id="mock_cluster_id"))
    )

    with patch.dict("sys.modules", wandb=mock_wandb), patch.dict(
        os.environ, os_env_var_dict
    ), patch.multiple(
        "anyscale.experimental_integrations",
        get_auth_api_client=Mock(return_value=Mock(api_client=mock_api_client)),
    ):
        if not mock_wandb:
            with pytest.raises(Exception):
                wandb_send_run_info_hook(mock_run)
                return
        else:
            wandb_send_run_info_hook(mock_run)
            if os.environ.get("ANYSCALE_HA_JOB_ID"):
                mock_api_client.update_wandb_run_values_api_v2_experimental_integrations_update_wandb_run_values_production_job_id_get.assert_called_once_with(
                    production_job_id=os.environ.get("ANYSCALE_HA_JOB_ID"),
                    wandb_project_url="mock_project_url",
                    wandb_group=mock_run.group,
                )
                assert mock_run.config.anyscale_logs == get_endpoint(
                    f"/jobs/{os.environ.get('ANYSCALE_HA_JOB_ID')}"
                )
            if os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"):
                mock_api_client.update_wandb_run_values_for_workspace_api_v2_experimental_integrations_update_wandb_run_values_for_workspace_workspace_id_get.assert_called_once_with(
                    workspace_id=os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"),
                    wandb_project_url="mock_project_url",
                    wandb_group=mock_run.group,
                )
                mock_api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get.assert_called_once_with(
                    os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID")
                )
                assert mock_run.config.anyscale_logs == get_endpoint(
                    f"/workspaces/{os.environ.get('ANYSCALE_EXPERIMENTAL_WORKSPACE_ID')}/mock_cluster_id"
                )
