import json
import os
from typing import Any, List

from anyscale.authenticate import get_auth_api_client
from anyscale.cli_logger import BlockLogger
from anyscale.shared_anyscale_utils.util import slugify
from anyscale.shared_anyscale_utils.utils.protected_string import ProtectedString
from anyscale.util import get_endpoint
from anyscale.utils.imports.gcp import try_import_gcp_secretmanager


"""anyscale/experimental_integrations.py: Experimental util functions for W&B integration and secret store prototypes."""

WANDB_API_KEY_NAME = "WANDB_API_KEY_NAME"  # pragma: allowlist secret
WANDB_PROJECT_NAME = "WANDB_PROJECT_NAME"
WANDB_GROUP_NAME = "WANDB_GROUP_NAME"

log = BlockLogger()  # Anyscale CLI Logger


def get_aws_secret(secret_name: str, **kwargs) -> ProtectedString:
    """
    Get secret value from AWS secrets manager.

    Arguments:
        secret_name: Key of your secret
        kwargs: Optional credentials passed in to authenticate instance
    """
    import boto3

    client = boto3.client("secretsmanager", **kwargs)
    response = client.get_secret_value(SecretId=secret_name)

    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in response:
        secret = response.pop("SecretString")
    else:
        secret = response.pop("SecretBinary")

    return ProtectedString(secret)


def get_gcp_secret(secret_name: str, **kwargs) -> ProtectedString:
    """
    Get secret value from GCP secrets manager.

    Arguments:
        secret_name: Key of your secret
        kwargs: Optional credentials passed in to authenticate instance
    """
    import google

    secretmanager = try_import_gcp_secretmanager()

    client = secretmanager.SecretManagerServiceClient(**kwargs)
    _, project_name = google.auth.default()

    name = f"projects/{project_name}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})

    return ProtectedString(response.payload.data.decode())


def wandb_get_api_key() -> ProtectedString:
    """
    Returns W&B API key based on key set in WANDB_API_KEY_NAME in
    AWS or GCP secrets manager.

    Assumes instance is running with correct IAM role, so credentials
    don't have to be passed to access secrets manager.
    """
    secret_names: List[str] = []
    wandb_api_key_name_env_var = os.environ.get(WANDB_API_KEY_NAME)
    if wandb_api_key_name_env_var:
        secret_names.append(wandb_api_key_name_env_var)
    cluster_id = os.environ.get("ANYSCALE_SESSION_ID")
    api_client = get_auth_api_client(log_output=False).api_client

    # Get cloud from cluster to use the correct method to
    # get secrets from a cloud.
    if cluster_id:
        cluster = api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get(
            cluster_id
        ).result
        cloud_id = cluster.cloud_id
        cloud = api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
    else:
        raise Exception(f"Unable to find cluster {cluster_id}")

    # Store alternate secret name to try fetching in list to ensure
    # backward compatibility with old secret naming convention
    secret_names.append(f"anyscale_{cloud.id}/{cluster.creator_id}/wandb_api_key")
    secret_names.append(f"wandb_api_key_{cluster.creator_id}")

    if cloud.provider != "AWS" and cloud.provider != "GCP":
        raise Exception(
            "The Anyscale W&B integration is currently only supported for AWS and GCP clouds."
        )
    for secret_name in secret_names:
        try:
            if cloud.provider == "AWS":
                region = cloud.region
                secret = get_aws_secret(secret_name, region_name=region)
            elif cloud.provider == "GCP":
                secret = get_gcp_secret(secret_name)
            return secret
        except Exception:
            log.info(f"Unable to fetch API key with name {secret_name}.")

    raise Exception("Unable to fetch API key from cloud secrets manager.")


def wandb_setup_api_key_hook() -> str:
    """
    Returns W&B API key based on key set in WANDB_API_KEY_NAME in
    AWS or GCP secrets manager. This returns the API key in plain text,
    so take care to not save the output in any logs.

    The WANDB_SETUP_API_KEY_HOOK will point to this method so it will
    be called by the OSS WandbLoggerCallback. Because this is called
    before wandb.init(), any other setup can also be done here.
    """
    protected_api_key = wandb_get_api_key()
    # Set environment variables to define default W&B project and group.
    set_wandb_project_group_env_vars()

    # API key returned in plaintext because the OSS WandbLoggerCallback
    # accepts the API key as a string arguement.
    return protected_api_key._UNSAFE_DO_NOT_USE


def set_wandb_project_group_env_vars():
    """
    Set WANDB_PROJECT_NAME and WANDB_GROUP_NAME environment variables
    for the OSS WandbLoggerCallback to use, based on the default mapping
    for production jobs, workspaces, and Ray jobs.
    """
    api_client = get_auth_api_client(log_output=False).api_client

    if os.environ.get("ANYSCALE_HA_JOB_ID"):
        production_job_id = os.environ.get("ANYSCALE_HA_JOB_ID")
        production_job = api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
            production_job_id
        ).result

        os.environ[WANDB_PROJECT_NAME] = "anyscale_default_project"
        os.environ[WANDB_GROUP_NAME] = slugify(production_job.name)
    elif os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"):
        workspace_id = os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID")
        workspace = api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get(
            workspace_id
        ).result

        os.environ[WANDB_PROJECT_NAME] = slugify(workspace.name)
    elif (
        json.loads(os.environ.get("RAY_JOB_CONFIG_JSON_ENV_VAR", json.dumps({})))
        .get("metadata", {})
        .get("job_name")
    ):
        ray_job_name = (
            json.loads(os.environ.get("RAY_JOB_CONFIG_JSON_ENV_VAR", json.dumps({})))
            .get("metadata", {})
            .get("job_name")
        )
        cluster_id = os.environ.get("ANYSCALE_SESSION_ID")
        if cluster_id:
            cluster_name = api_client.get_session_api_v2_sessions_session_id_get(
                cluster_id
            ).result.name
        else:
            cluster_name = "anyscale_default_project"
        os.environ[WANDB_PROJECT_NAME] = slugify(cluster_name)
        os.environ[WANDB_GROUP_NAME] = slugify(ray_job_name)


def wandb_send_run_info_hook(run: Any) -> None:
    """
    The WANDB_PROCESS_RUN_INFO points to this method and is called on
    the `run` output of `wandb.init()`.

    Send the W&B URL to the control plane, and populate the link back to
    Anyscale from the W&B run config.
    """
    try:
        import wandb
    except ImportError:
        raise Exception("Unable to import wandb.")

    assert isinstance(
        run, wandb.sdk.wandb_run.Run
    ), "`run` argument must be of type wandb.sdk.wandb_run.Run"

    api_client = get_auth_api_client(log_output=False).api_client

    if os.environ.get("ANYSCALE_HA_JOB_ID"):
        production_job_id = os.environ.get("ANYSCALE_HA_JOB_ID")
        api_client.update_wandb_run_values_api_v2_experimental_integrations_update_wandb_run_values_production_job_id_get(
            production_job_id=production_job_id,
            wandb_project_url=run.get_project_url(),
            wandb_group=run.group,
        )
        run.config.anyscale_logs = get_endpoint(f"/jobs/{production_job_id}")
    if os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"):
        workspace_id = os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID")
        api_client.update_wandb_run_values_for_workspace_api_v2_experimental_integrations_update_wandb_run_values_for_workspace_workspace_id_get(
            workspace_id=workspace_id,
            wandb_project_url=run.get_project_url(),
            wandb_group=run.group,
        )
        workspace = api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get(
            workspace_id
        ).result
        cluster_id = workspace.cluster_id
        if cluster_id:
            run.config.anyscale_logs = get_endpoint(
                f"/workspaces/{workspace_id}/{cluster_id}"
            )
