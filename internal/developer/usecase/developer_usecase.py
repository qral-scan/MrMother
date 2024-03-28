from internal.developer.repository.developer_repository import developer_repository


class developer_usecase:
    repository: developer_repository

    def __init__(self, repository) -> None:
        self.repository = repository
        pass

    def start_build_job(self) -> Exception:
        err = self.repository.create_build_job()
        return err
