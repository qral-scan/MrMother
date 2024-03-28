

import json
import requests
from internal.domain.merge_request import PullRequestSchema, PullRequest, RequestedReviewersResponse, RequestedReviewersResponseSchema, User, UserSchema
from marshmallow import ValidationError
from typing import List, Tuple
from internal.utilities.config import Config

class merge_request_repository:

    def __init__(self) -> None:
        pass

    def get_merge_request_reviews(self, pull_request_number):
        url = f"https://api.github.com/repos/qral-scan/usb/pulls/{pull_request_number}/requested_reviewers"
        response = requests.get(url, headers={'Authorization': f'Bearer {Config().get('github_token')}'})
        try:
            result = RequestedReviewersResponseSchema().load(response)
            return result
        except Exception as e:
            return e, None
        return

    def get_merge_request_requested_reviewers(self, pull_request_number):
        return

    def get_merge_status(self, pull_request_number) -> bool:
        url = f'https://api.github.com/repos/qral-scan/usb/pulls/{pull_request_number}/merge'
        response = requests.get(url, headers={'Authorization': f'Bearer {Config().get('github_token')}'}).text
        return

    def get_all(self) -> Tuple[Exception, List[PullRequest]]:
        url = f'https://api.github.com/repos/{Config().get('github_owner')}/{Config().get('github_repo')}/pulls'
        response = requests.get(url, headers={'Authorization': f'Bearer {Config().get('github_token')}'}).text
        try:
            result: List[PullRequest] = PullRequestSchema().loads(
                response, many=True)
            return None, result
        except Exception as e:
            return e, None
