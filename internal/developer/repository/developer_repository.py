import ast
from typing import List, Tuple

import requests
from internal.domain.merge_request import User
from internal.utilities.config import Config


class developer_repository:
    developers: dict
    def __init__(self) -> None:
        list_of_dicts = ast.literal_eval(Config().get('developer_developers'))
        self.developers = {}
        for d in list_of_dicts:
            self.developers.update(d)

    def get_all(self) -> Tuple[Exception, List[str]]:
        try:
            return None, self.developers.keys()
        except Exception as e:
            return e, []

    def create_build_job(self) -> Exception:
        try:
            url = "https://api.github.com/repos/qral-scan/scout/actions/workflows/80617371/dispatches"
            response = requests.post(
                url,
                headers={"Authorization": f'Bearer {Config().get("github_token")}'},
                json={"ref": "main"},
            )
            if response.status_code == 204:
                return None
            else:
                return ValueError
        except Exception as e:
            return e

    def get_developer_tg_nickname(self, gh_login: str) -> Tuple[Exception, str]:
        try:
            return None, self.developers[gh_login]
        except Exception as e:
            return KeyError, None
        return
