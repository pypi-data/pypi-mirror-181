import logging
import os
import sys
from typing import Optional

import pydantic

from ..constants import DEFAULT_APP_ROOT
from ..log_config import load_logging_config

logger = logging.getLogger("azmlinfsrv")


class AMLInferenceServerConfig(pydantic.BaseSettings):
    # Root directory for the app
    app_root: str = pydantic.Field(default=DEFAULT_APP_ROOT)

    # Path to source directory
    source_dir: Optional[str] = pydantic.Field(default=None, env="AZUREML_SOURCE_DIRECTORY")

    # Path to entry script file
    entry_script: Optional[str] = pydantic.Field(default=None, env="AZUREML_ENTRY_SCRIPT")

    # Name of the service (used for Swagger schema generation)
    service_name: str = pydantic.Field(default="ML service", env="SERVICE_NAME")

    # Name of the workspace
    workspace_name: str = pydantic.Field(default="", env="WORKSPACE_NAME")

    # Prefix for the service path (used for Swagger schema generation)
    service_path_prefix: str = pydantic.Field(default="", env="SERVICE_PATH_PREFIX")

    # Version of the service (used for Swagger schema generation)
    service_version: str = pydantic.Field(default="1.0", env="SERVICE_VERSION")

    # Dictates how long scoring function with run before timeout in milliseconds.
    scoring_timeout: int = pydantic.Field(default=3600 * 1000, env="SCORING_TIMEOUT_MS")

    # When @rawhttp is used, whether the user requires on `request` object to have the flask v1 properties/behavior.
    flask_one_compatibility: bool = pydantic.Field(default=True)

    # Sets the Logging level
    log_level: str = pydantic.Field(default="INFO", env="AZUREML_LOG_LEVEL")

    # Whether to enable AppInsights
    app_insights_enabled: bool = pydantic.Field(default=False)

    # Key to user AppInsights
    app_insights_key: Optional[pydantic.SecretStr] = pydantic.Field(deafult=None)

    # Whether to enable model data collection
    model_dc_storage_enabled: bool = pydantic.Field(default=False)

    # Whether to log response to AppInsights
    app_insights_log_response_enabled: bool = pydantic.Field(default=True, env="APP_INSIGHTS_LOG_RESPONSE_ENABLED")

    # Enable CORS for the specified origins
    cors_origins: Optional[str] = pydantic.Field(default=None)

    # Path to model directory
    azureml_model_dir: str = pydantic.Field(default=None, env="AZUREML_MODEL_DIR")

    hostname: str = pydantic.Field(default="Unknown", env="HOSTNAME")

    # Start the inference server in DEBUGGING mode
    debug_port: Optional[int] = pydantic.Field(default=None, env="AZUREML_DEBUG_PORT")

    class Config:
        # For fields that do not have a value for "env", the environment variable name is built by concatenating this
        # value with the field name. As an example, the field `app_insights_key` will read its value from the
        # environment variable `AML_APP_INSIGHTS_KEY`.
        env_prefix = "AML_"


def log_config_errors(ex):
    for error in ex.errors():
        field = AMLInferenceServerConfig.__fields__[error["loc"][0]]
        env_variable = ", ".join(env_name.upper() for env_name in field.field_info.extra["env_names"])
        logger.critical(
            (
                "\n"
                "===============Configuration Error================="
                "\n"
                f"{field.name}: {error['msg']} (environment variable: {env_variable})"
                "\n"
                "==================================================="
            )
        )


try:
    config = AMLInferenceServerConfig()
    # Try to load from app root, if unsuccessful and entry script is set, try
    # to load from entry script directory
    if not load_logging_config(config.app_root) and config.entry_script:
        entry_script_dir = os.path.dirname(os.path.realpath(config.entry_script))
        load_logging_config(entry_script_dir)
except pydantic.ValidationError as ex:
    log_config_errors(ex)
    # Gunicorn treats '3' as a boot error and terminates the master.
    sys.exit(3)
