from typing import List, Tuple
from internal.developer.repository.developer_repository import developer_repository
from internal.domain.merge_request import PullRequest
from internal.merge_request.repository.merge_request_repository import (
    merge_request_repository,
)

class merge_request_usecase:
    mr_repository: merge_request_repository
    dev_repository: developer_repository

    def __init__(self, mr_repo, dev_repo) -> None:
        self.mr_repository = mr_repo
        self.dev_repository = dev_repo
        pass

    def check_pull_requests(
        self,
    ) -> Tuple[Exception, List[PullRequest], List[str], List[str]]:
        err, prs = self.mr_repository.get_all()
        if err != None:
            return err, []
        err, developers = self.dev_repository.get_all()
        review_devs = []
        asignee_devs = []
        if err != None:
            return err, []
        for pr in prs:
           if any(label.name == "draft" for label in pr.labels):
               prs.remove(pr)
        for pr in prs:
            err, reviews = self.mr_repository.get_merge_request_reviews(pr.number)
            if err != None:
                return err, []
            reviewes_approved = set()
            reviewes_asked_for_changes = set()
            for review in reviews:
                if review.state == 'COMMENTED':
                   reviewes_asked_for_changes.add(review.user.login) 
                if review.state == 'APPROVED':
                    reviewes_approved.add(review.user.login)
            reviewers = []
            gh_nicknames = self._find_occurrences(
                body=pr.body, string_list=developers)
            for nickname in gh_nicknames:
                err, tg_nickname = self.dev_repository.get_developer_tg_nickname(
                    gh_login=nickname
                )
                if nickname.removeprefix('@') not in reviewes_approved:
                    reviewers.append(tg_nickname)
                else:
                    reviewers.append(f'{nickname.removeprefix('@')} ✅')
            review_devs.append(reviewers)
            if pr.assignee != None:
                postfix = ''
                if pr.assignee.login in reviewes_approved:
                    postfix = ' ✅'
                _, pr.assignee.login = self.dev_repository.get_developer_tg_nickname(
                    gh_login=f"@{pr.assignee.login}"
                )
                pr.assignee.login += postfix
                

        return None, prs, review_devs, asignee_devs

    def _find_occurrences(self, body, string_list):
        occurrences = []
        if body is None:
            return []
        for string in string_list:
            if string in body:
                occurrences.append(string)
        return occurrences
