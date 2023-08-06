import json
import os
import warnings
from pathlib import Path
import shutil
from typing import Any, Dict, List, Union

from cement.utils.shell import exec_cmd2
from hmd_cli_tools.hmd_cli_tools import read_manifest
from hmd_cli_tools.okta_tools import get_auth_token

HMD_HOME = os.environ.get("HMD_HOME", None)


def build(
    image_name: str,
    runs: List[str],
    templates: List[str],
    contexts: List[str],
    variables: Dict[str, Any],
    repo_path: str,
    deps: bool,
    links: List[str],
):
    project_path = Path(repo_path)

    if not project_path.exists():
        raise Exception("Input project could not be located")

    manifest = read_manifest()
    generate_cfgs: Dict[str, Any] = manifest.get("generate", {})

    if len(runs) == 0:
        runs = [k for k in generate_cfgs]

    for run in runs:
        transform_context = generate_cfgs[run]

        output_path = transform_context.get("output", None)
        if output_path is None:
            output_path = project_path
        else:
            output_path = project_path / output_path

        os.makedirs(output_path, exist_ok=True)

        template_path = project_path / ".mickey_cache"

        if not template_path.exists():
            os.makedirs(template_path)
        if not "config" in transform_context:
            transform_context["contexts"] = [
                *transform_context.get("contexts", []),
                *contexts,
            ]
            transform_context["templates"] = [
                *transform_context.get("templates", []),
                *templates,
            ]
            transform_context["template_packages"] = manifest.get("templates", {})
            transform_context["context_definitions"] = manifest.get("contexts", {})

        transform_context["variables"] = {
            **transform_context.get("variables", {}),
            **variables,
        }
        transform_context["run_name"] = run
        transform_context["project_name"] = manifest.get("name", None)
        img_tag = os.environ.get("HMD_TF_MICKEY_VERSION", "stable")
        print(f"Running {image_name}:{img_tag}")

        skip_deps = ["-e", 'MICKEY_SKIP_DEPS="true"'] if not deps else []

        gh_env = []
        gh_user = os.environ.get("HMD_GH_USERNAME")
        gh_pat = os.environ.get("HMD_GH_PASSWORD")

        if gh_user:
            gh_env.extend(["-e", f"HMD_GH_USERNAME={gh_user}"])
        else:
            warnings.warn(
                "WARNING: Environment variable HMD_GH_USERNAME not found. Cannot pull from GitHub. Please set with 'hmd config set-env HMD_GH_USERNAME <username>'"
            )

        if gh_pat:
            if os.path.exists(gh_pat):
                gh_pat = Path(gh_pat).read_text()
            gh_env.extend(["-e", f"HMD_GH_PASSWORD={gh_pat}"])
        else:
            warnings.warn(
                "WARNING: Environment variable HMD_GH_PASSWORD not found. Cannot pull from GitHub. Please set with 'hmd config set-env HMD_GH_PASSWORD <path to PAT file>'"
            )

        link_volumes = []
        artifact_url = (
            [
                "-e",
                f"HMD_ARTIFACT_LIBRARIAN_URL={os.environ.get('HMD_ARTIFACT_LIBRARIAN_URL')}",
            ]
            if os.environ.get("HMD_ARTIFACT_LIBRARIAN_URL") is not None
            else []
        )

        for ln in links:
            link_volumes.extend(["-v", ln])

        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{project_path}:/hmd_transform/input",
            "-v",
            f"{output_path}:/hmd_transform/output",
            "-v",
            f"{template_path}:/hmd_transform/cache",
            *link_volumes,
            "-e",
            f"TRANSFORM_INSTANCE_CONTEXT={json.dumps(transform_context)}",
            "-e",
            f"HMD_AUTH_TOKEN={get_auth_token()}",
            "-e",
            f"HMD_CUSTOMER_CODE={os.environ.get('HMD_CUSTOMER_CODE')}",
            "-e",
            f"HMD_REGION={os.environ.get('HMD_REGION')}",
            *artifact_url,
            *skip_deps,
            *gh_env,
            f"{image_name}:{img_tag}",
        ]

        return_code = exec_cmd2(command)

        if return_code != 0:
            raise Exception(f"Process completed with non-zero exit code: {return_code}")


def init():
    manifest_path = Path("meta-data") / "manifest.json"
    prj_name = os.path.basename(os.getcwd())
    init_files = os.path.join(os.path.dirname(__file__), "init_files/")

    default_manifest = {
        "name": prj_name,
        "description": "",
        "generate": {
            "example_tables": {
                "contexts": ["ref:tables"],
                "templates": [f"{prj_name}/sql"],
            },
        },
        "contexts": {"tables": {"each": ["src/mickey/data/*.json"]}},
        "templates": ["./src/mickey/templates"],
    }

    if not os.path.exists(manifest_path):
        print("Cannot find ./meta-data/manifest.json. Creating one...")
        if not os.path.exists(Path("meta-data")):
            os.mkdir("meta-data")
        manifest = {
            "name": prj_name,
            "description": "",
        }
    else:
        manifest = read_manifest()

    if "generate" not in manifest:
        print("Adding generate property to project manifest...")
        manifest["generate"] = default_manifest["generate"]

    if "templates" not in manifest:
        print(
            "Adding templates property to manifest. Defaulting to ['./src/mickey/templates']."
        )

        if not os.path.exists("./src/mickey/templates"):
            shutil.copytree(
                Path(init_files) / "templates", Path("./src/mickey/templates")
            )

        manifest["templates"] = default_manifest["templates"]

    if not os.path.exists("./src/mickey/templates"):
        print("Creating local templates directory...")
        os.makedirs("./src/mickey/templates")

    if "contexts" not in manifest:
        print("Adding contexts property to manifest...")
        if not os.path.exists("./src/mickey/data"):
            shutil.copytree(Path(init_files) / "data", Path("./src/mickey/data"))
        manifest["contexts"] = default_manifest["contexts"]

    with open(manifest_path, "w") as mf:
        print("Writing new manifest file to ./meta-data/manifest.json")
        json.dump(manifest, mf)
