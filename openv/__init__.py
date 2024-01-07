import os
from onepassword import OnePassword

DOTENV_VAULT = ".env"

op = OnePassword()


class VaultNotFoundError(Exception):
    def __init__(self, vault):
        self.vault = vault
        super().__init__(f"Vault: {self.vault} not found.")


def _validate_dotenv_vault_exists() -> None:
    vault_names = [vault["name"] for vault in op.list_vaults()]
    if not DOTENV_VAULT not in vault_names:
        raise VaultNotFoundError(vault=DOTENV_VAULT)


def load_openv(project: str) -> None:
    item_ids = [
        item["id"] for item in op.list_items(vault=".env") if item["title"] == project
    ]
    if not len(item_ids):
        raise Exception(f"There are no projects with the name: {project}")
    if len(item_ids) > 1:
        raise Exception(f"There are multiple projects with the name: {project}")
    item_id = item_ids[0]
    fields = {
        field["label"]: field["value"]
        for field in op.get_item(uuid=item_id)["fields"]
        if "value" in field.keys()
    }
    for key, val in fields.items():
        if val is not None:
            os.environ[key] = val
