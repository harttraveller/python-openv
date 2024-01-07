import os
from onepassword import OnePassword

op = OnePassword()


def load_1penv(project: str) -> None:
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
