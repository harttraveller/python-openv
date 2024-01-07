class VaultNotFoundError(Exception):
    def __init__(self, vault: str) -> None:
        self.vault = vault
        super().__init__(f"Vault: {self.vault} not found.")


class ProjectNotFoundError(Exception):
    def __init__(self, project: str) -> None:
        self.project = project
        super().__init__(f"Project: {self.project} not found.")


class MultipleProjectsFoundError(Exception):
    def __init__(self, project: str) -> None:
        self.project = project
        super().__init__(f"There are multiple projects with the name: {self.project}")
