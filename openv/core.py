import os
from onepassword import OnePassword
from openv.constant import DOTENV_VAULT
from openv.exception import (
    VaultNotFoundError,
    ProjectNotFoundError,
    MultipleProjectsFoundError,
)


op = OnePassword()


def validate_dotenv_vault_exists() -> None:
    "Check the .env vault exists."
    vault_names = [vault["name"] for vault in op.list_vaults()]
    if not DOTENV_VAULT not in vault_names:
        raise VaultNotFoundError(vault=DOTENV_VAULT)


def get_uuid_for_project(project: str) -> str:
    uuids = [
        item["id"]
        for item in op.list_items(vault=DOTENV_VAULT)
        if item["title"] == project
    ]
    if not len(uuids):
        raise ProjectNotFoundError(project=project)
    if len(uuids) > 1:
        raise MultipleProjectsFoundError(project=project)
    return uuids[0]


def get_fields_for_project(uuid: str) -> dict[str, str]:
    return {
        field["label"]: field["value"]
        for field in op.get_item(uuid=uuid)["fields"]
        if "value" in field.keys()
    }


def set_environment_variables(fields: dict[str, str]) -> None:
    for key, val in fields.items():
        if val is not None:
            os.environ[key] = val


def load_openv(project: str) -> None:
    validate_dotenv_vault_exists()
    project_uuid = get_uuid_for_project(project=project)
    fields = get_fields_for_project(uuid=project_uuid)
    set_environment_variables(fields=fields)
