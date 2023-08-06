import os
import typing
import functools

from aws_cdk import App


# Constants
ALLOWED_ENVIRONMENTS = os.environ.get("ALLOWED_ENVIRONMENTS", [])
COMMON_ENVIRONMENT_KEY = os.environ.get("COMMON_ENVIRONMENT_KEY", "default")
ENVIRONMENT_CONTEXT_KEY = os.environ.get(
    "ENVIRONMENT_CONTEXT_KEY", "environment"
)

# Shared var
app_context = {}


aws_account = os.environ.get("CDK_DEFAULT_ACCOUNT")
aws_region = os.environ.get("CDK_DEFAULT_REGION")


def combine_configurations(
    config: typing.Any,
    key: typing.Optional[str] = None,
    exclude_keys: typing.Optional[list] = None,
) -> typing.Any:
    exclude_keys = exclude_keys or []

    def filter_config(conf: dict) -> dict:
        if aws_account and aws_account in conf:
            return filter_config(conf[aws_account])
        elif aws_region and aws_region in conf:
            return filter_config(conf[aws_region])

        filtered_config = {
            k: v for k, v in conf.items() if k not in exclude_keys
        }
        return filtered_config if key is None else filtered_config.get(key, {})

    if isinstance(config, dict) is False:
        return config

    # Environments
    environment = get_environment()
    if environment is None:
        # Not environment app
        return filter_config(config.get(COMMON_ENVIRONMENT_KEY, config))

    environments = ALLOWED_ENVIRONMENTS + [COMMON_ENVIRONMENT_KEY]
    env_config = (
        {k: v for k, v in config.items() if k in environments}
        if len(ALLOWED_ENVIRONMENTS) > 0
        else config
    )
    if len(env_config) == 0:
        # Not environment app
        return filter_config(config)

    combined_config = dict(
        env_config.get(COMMON_ENVIRONMENT_KEY, {}),
        **env_config.get(environment, {}),
    )
    return filter_config(combined_config)


def get_context_variable(key: str) -> typing.Any:
    context_variable = app_context["app"].node.try_get_context(key)
    context_variable = combine_configurations(context_variable)
    return context_variable


@functools.lru_cache(maxsize=None)
def get_environment(app: typing.Optional[App] = None) -> typing.Optional[str]:
    environment = (app or app_context["app"]).node.try_get_context(
        ENVIRONMENT_CONTEXT_KEY
    ) or os.getenv(ENVIRONMENT_CONTEXT_KEY.upper())
    app_context[ENVIRONMENT_CONTEXT_KEY] = environment
    return environment


def env(**kwargs):
    """
    """
    environment = get_environment()

    def filter_env(conf: dict):
        if not isinstance(conf, dict):
            return conf
        if environment in conf:
            return filter_env(conf.get(environment))
        if aws_account and aws_account in conf:
            return filter_env(conf.get(aws_account))
        if aws_region and aws_region in conf:
            return filter_env(conf.get(aws_region))
        if COMMON_ENVIRONMENT_KEY in conf:
            return filter_env(conf.get(COMMON_ENVIRONMENT_KEY))
        return conf

    return filter_env(kwargs)


@functools.lru_cache(maxsize=None)
def context_var(var: str, default: typing.Any = None, app: typing.Optional[App] = None, required: bool = False) -> typing.Optional[str]:
    app = app or app_context["app"]
    value = app.node.try_get_context(var) or os.getenv(var)  or default
    if value is None and required:
        raise Exception(f"{var} context variable is required")
    return value
