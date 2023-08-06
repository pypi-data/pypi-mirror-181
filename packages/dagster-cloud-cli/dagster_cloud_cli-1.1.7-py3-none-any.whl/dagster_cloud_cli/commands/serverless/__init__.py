import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import List

import dagster._check as check
import pkg_resources
import typer
from dagster_cloud_cli import gql, pex_utils, ui
from dagster_cloud_cli.commands.workspace import wait_for_load
from dagster_cloud_cli.config_utils import (
    DEPLOYMENT_CLI_OPTIONS,
    dagster_cloud_options,
    get_location_document,
)
from dagster_cloud_cli.core import pex_builder
from dagster_cloud_cli.utils import add_options
from typer import Argument, Option, Typer

app = Typer(help="Build and deploy your code to Dagster Cloud.")

_BUILD_OPTIONS = {
    "source_directory": (
        Path,
        Option(
            None,
            "--source-directory",
            "-d",
            exists=False,
            help="Source directory to build for the image.",
        ),
    ),
    "base_image": (
        str,
        Option(None, "--base-image", exists=False),
    ),
    "env": (
        List[str],
        Option(
            [],
            "--env",
            exists=False,
            help="Environment variable to be defined in image, in the form of `MY_ENV_VAR=hello`",
        ),
    ),
}

DEPLOY_DOCKER_OPTIONS = {
    "image": (
        str,
        Option(
            None,
            "--image",
            exists=False,
            help="Override built Docker image tag. Should not be needed outside of debugging.",
            hidden=True,
        ),
    ),
    "base_image": (
        str,
        Option(None, "--base-image", exists=False, help="Custom base image"),
    ),
    "env": (
        List[str],
        Option(
            [],
            "--env",
            exists=False,
            help="Environment variable to be defined in image, in the form of `MY_ENV_VAR=hello`",
        ),
    ),
}


@contextmanager
def _template_dockerfile(env_vars, custom_base_image=None):
    DOCKERFILE_TEMPLATE = pkg_resources.resource_filename(
        "dagster_cloud_cli", "commands/serverless/Dockerfile"
    )
    base_image_command = (
        f"FROM {custom_base_image}" if custom_base_image else "FROM python:3.8-slim"
    )
    with open(DOCKERFILE_TEMPLATE, "r", encoding="utf-8") as template:
        dockerfile_content = "\n".join(
            [base_image_command, template.read(), *[f"ENV {env_var}" for env_var in env_vars]]
        )

        yield bytes(dockerfile_content, "utf-8")


def _build_image(source_directory, image, registry_info, env_vars, base_image):
    registry = registry_info["registry_url"]
    with _template_dockerfile(env_vars, base_image) as dockerfile_content:
        cmd = [
            "docker",
            "build",
            source_directory,
            "-t",
            f"{registry}:{image}",
            "-f",
            "-",
            "--platform",
            "linux/amd64",
        ]
        return subprocess.run(cmd, input=dockerfile_content, check=True).returncode


@app.command(name="build", short_help="Build image for Dagster Cloud code location.", hidden=True)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(_BUILD_OPTIONS)
def build_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,
):
    """Add or update the image for a code location in the workspace."""
    source_directory = str(kwargs.get("source_directory"))
    base_image = kwargs.get("base_image")
    env_vars = kwargs.get("env", [])
    _verify_docker()

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]

        if base_image and not ecr_info.get("allow_custom_base"):
            ui.warn("Custom base images are not enabled for this organization.")
            base_image = None

        retval = _build_image(source_directory, image, ecr_info, env_vars, base_image)
        if retval == 0:
            ui.print(f"Built image {registry}:{image}")


def _upload_image(image, registry_info):
    registry = registry_info["registry_url"]
    aws_token = registry_info["aws_auth_token"]
    if not registry or not aws_token:
        raise ui.error(
            "No registry found. You may need to wait for your Dagster serverless deployment to activate."
        )

    username, password = base64.b64decode(aws_token).decode("utf-8").split(":")
    subprocess.check_output(
        f"echo {str(password)} | docker login --username {str(username)} --password-stdin {registry}",
        shell=True,
    )
    return subprocess.call(
        ["docker", "push", f"{registry}:{image}"], stderr=sys.stderr, stdout=sys.stdout
    )


@app.command(
    name="upload",
    short_help="Upload the built code location image to Dagster Cloud's image repository.",
    hidden=True,
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def upload_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace."""

    _verify_docker()

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        retval = _upload_image(image, ecr_info)
        if retval == 0:
            ui.print(f"Pushed image {image} to {registry}")


@app.command(
    name="registry-info",
    short_help="Get registry information and temporary creds for an image repository",
    hidden=True,
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def registry_info_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace. Used by GH action to
    authenticate to the image registry"""

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry_url = ecr_info["registry_url"]
        aws_region = ecr_info.get("aws_region", "us-west-2")
        aws_token = ecr_info["aws_auth_token"]
        custom_base_image_allowed = ecr_info["allow_custom_base"]

        if not aws_token or not registry_url:
            return

        username, password = base64.b64decode(aws_token).decode("utf-8").split(":")

        values = [
            f"REGISTRY_URL={registry_url}",
            f"AWS_DEFAULT_REGION={aws_region}",
            f"AWS_ECR_USERNAME={username}",
            f"AWS_ECR_PASSWORD={password}",
        ]
        if custom_base_image_allowed:
            values.append("CUSTOM_BASE_IMAGE_ALLOWED=1")
        ui.print("\n".join(values) + "\n")


@app.command(
    name="deploy",
    short_help="Add a code location from a local directory",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(DEPLOY_DOCKER_OPTIONS)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def deploy_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    deployment: str,
    source_directory: Path = Argument(".", help="Source directory."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace."""

    location_name = kwargs.get("location_name")
    if not location_name:
        raise ui.error(
            "No location name provided. You must specify the location name as an argument."
        )

    if not source_directory:
        raise ui.error("No source directory provided.")

    _check_source_directory(source_directory)
    _verify_docker()

    env_vars = kwargs.get("env", [])
    base_image = kwargs.get("base_image")

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]

        commit_hash = kwargs.get("commit_hash") or str(uuid.uuid4().hex)
        default_image_tag = f"{deployment}-{location_name}-{commit_hash}"
        image_tag = kwargs.get("image") or default_image_tag

        retval = _build_image(source_directory, image_tag, ecr_info, env_vars, base_image)
        if retval != 0:
            return

        retval = _upload_image(image_tag, ecr_info)
        if retval != 0:
            return

        location_args = {**kwargs, "image": f"{registry}:{image_tag}"}
        location_document = get_location_document(location_name, location_args)
        gql.add_or_update_code_location(client, location_document)

        wait_for_load(
            client,
            [location_name],
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
            url=url,
        )

        workspace_url = f"{url}/workspace"
        ui.print(
            f"Added or updated location {location_name}. "
            f"View the status of your workspace at {workspace_url}."
        )


@app.command(
    name="upload-base-image",
    short_help="Upload a local Docker image to Dagster cloud, to use as a custom base image for deploy-python-executable.",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def upload_base_image_command(
    api_token: str,
    url: str,
    local_image: str = Argument(..., help="Pre-built local image, eg. 'local-image:local-tag'"),
    published_tag: str = Option(
        None,
        help="Published tag used to identify this image in Dagster Cloud. "
        "A tag is auto-generated if not provided.",
    ),
):
    if not published_tag:
        published_tag = _generate_published_tag_for_image(local_image)

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        published_image = f"{registry}:{published_tag}"

        # tag local image with new tag
        cmd = [
            "docker",
            "tag",
            local_image,
            published_image,
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as err:
            raise ui.error(
                f"Error tagging local image {local_image}: " + err.stderr.decode("utf-8")
            )

        # upload tagged image
        retval = _upload_image(image=published_tag, registry_info=ecr_info)
        if retval == 0:
            ui.print(f"Pushed image {published_tag} to {registry}.")
            ui.print(
                f"To use the uploaded image run: "
                f"dagster-cloud deploy-python-executable --base-image-tag={published_tag} [ARGS]"
            )


def _generate_published_tag_for_image(image: str):
    image_id = subprocess.check_output(["docker", "inspect", image, "--format={{.Id}}"])
    #  The id is something like 'sha256:518ad2f92b078c63c60e89f0310f13f19d3a1c7ea9e1976d67d59fcb7040d0d6'
    return image_id.decode("utf-8").replace(":", "_").strip()


@app.command(name="build-python-executable", short_help="Build a Python Executable", hidden=True)
def build_python_executable_command(
    code_directory: str,
    output_directory: str,
    python_version: str = typer.Option("3.8", help="Target Python version as 'major.minor'"),
):
    parsed_python_version = pex_builder.util.parse_python_version(python_version)
    ui.print("Building source...")
    source_path = pex_builder.source.build_source_pex(
        code_directory, output_directory=output_directory, python_version=parsed_python_version
    )
    ui.print(f"Built {source_path}")
    ui.print("Building dependencies...")
    deps_path = pex_builder.deps.build_deps_pex(
        code_directory, output_directory=output_directory, python_version=parsed_python_version
    )
    ui.print(f"Built {deps_path}")


@app.command(
    name="deploy-python-executable",
    short_help="[Fast Deploys] Add a code location from a local directory built as a Python executable.",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(pex_utils.DEPLOY_PEX_OPTIONS)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def deploy_python_executable_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    source_directory: Path = Argument(".", help="Source directory."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace, using Python executable."""

    location_name = kwargs.get("location_name")
    if not location_name:
        raise ui.error(
            "No location name provided. You must specify the location name as an argument."
        )

    if not source_directory:
        raise ui.error("No source directory provided.")

    _check_source_directory(source_directory)

    kwargs = pex_utils.build_upload_pex(
        url=url,
        api_token=api_token,
        location=location_name,
        python_source_dir=source_directory,
        kwargs=kwargs,
    )
    with gql.graphql_client_from_url(url, api_token) as client:
        location_document = get_location_document(location_name, kwargs)
        gql.add_or_update_code_location(client, location_document)

        wait_for_load(
            client,
            [location_name],
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
            url=url,
        )

        workspace_url = f"{url}/workspace"
        ui.print(
            f"Added or updated location {location_name}. "
            f"View the status of your workspace at {workspace_url}."
        )


def _verify_docker():
    if subprocess.call("docker -v", shell=True) != 0:
        raise ui.error("Docker must be installed locally to deploy to Dagster Cloud Serverless")


SOURCE_INSTRUCTIONS = (
    "You can specify the directory you want to deploy by using the `--source-directory` argument "
    "(defaults to current directory)."
)


def _check_source_directory(source_directory):
    contents = os.listdir(source_directory)

    if "setup.py" not in contents and "requirements.txt" not in contents:
        message = (
            "Could not find a `setup.py` or `requirements.txt` in the target directory. You must "
            "specify your required Python dependencies (including the `dagster-cloud` package) "
            "along with your source files to deploy to Dagster Cloud."
        )
        if source_directory == ".":
            message = f"{message} {SOURCE_INSTRUCTIONS}"
        raise ui.error(message)
