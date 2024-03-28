from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields, validate, post_load


@dataclass
class User:
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: Optional[str]
    site_admin: Optional[bool]


@dataclass
class Label:
    id: Optional[int]
    node_id: Optional[str]
    url: Optional[str]
    color: Optional[str]
    default: Optional[bool]
    description: Optional[str]
    name: Optional[str]


@dataclass
class PullRequest:
    url: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    html_url: Optional[str]
    diff_url: Optional[str]
    patch_url: Optional[str]
    issue_url: Optional[str]
    number: Optional[int]
    state: Optional[str]
    locked: Optional[bool]
    title: Optional[str]
    user: Optional[User]
    body: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    closed_at: Optional[str]
    merged_at: Optional[str]
    merge_commit_sha: Optional[str]
    assignee: Optional[User]
    assignees: Optional[List]
    requested_reviewers: Optional[List]
    requested_teams: Optional[List]
    labels: Optional[List]
    milestone: Optional[dict]
    draft: Optional[bool]
    commits_url: Optional[str]
    review_comments_url: Optional[str]
    review_comment_url: Optional[str]
    comments_url: Optional[str]
    statuses_url: Optional[str]
    head: Optional[dict]
    base: Optional[dict]
    _links: Optional[dict]
    author_association: Optional[str]
    auto_merge: Optional[str]
    active_lock_reason: Optional[str]


class UserSchema(Schema):
    login = fields.String(allow_none=True)
    id = fields.Integer(allow_none=True)
    node_id = fields.String(allow_none=True)
    avatar_url = fields.URL(allow_none=True)
    gravatar_id = fields.String(allow_none=True)
    url = fields.URL(allow_none=True)
    html_url = fields.URL(allow_none=True)
    followers_url = fields.URL(allow_none=True)
    following_url = fields.URL(allow_none=True)
    gists_url = fields.URL(allow_none=True)
    starred_url = fields.URL(allow_none=True)
    subscriptions_url = fields.URL(allow_none=True)
    organizations_url = fields.URL(allow_none=True)
    repos_url = fields.URL(allow_none=True)
    events_url = fields.URL(allow_none=True)
    received_events_url = fields.URL(allow_none=True)
    type = fields.String(
        allow_none=True, validate=validate.OneOf(["User", "Organization"])
    )
    site_admin = fields.Boolean(allow_none=True)

    @post_load
    def make_user(self, data, many, **kwargs):
        if many is None:
            many = self.many
        if many:
            return [User(**user) for user in data]
        else:
            return User(**data)

    class Meta:
        target = User
        register_as_scheme = True


class LabelSchema(Schema):
    class Meta:
        target = Label
        register_as_scheme = True

    @staticmethod
    def _load_label_request(data: dict) -> Label:
        return Label(**data)

    @staticmethod
    def _load_label_requests(data: List[dict]) -> List[Label]:
        return [LabelSchema._load_label_request(item) for item in data]

    def load(self, data, many=None, **kwargs):
        if many is None:
            many = self.many

        if many:
            return self._load_label_requests(data)
        else:
            return self._load_label_request(data)

    id = fields.Integer(allow_none=True)
    node_id = fields.String(allow_none=True)
    url = fields.URL(allow_none=True)
    color = fields.String(allow_none=True)
    default = fields.Boolean(allow_none=True)
    description = fields.String(allow_none=True)
    name = fields.String(allow_none=True)


class PullRequestSchema(Schema):
    class Meta:
        target = PullRequest
        register_as_scheme = True

    @post_load
    def make_pull_request(self, data, **kwargs):
        return PullRequest(**data)

    url = fields.URL(allow_none=True)
    id = fields.Integer(allow_none=True)
    node_id = fields.String(allow_none=True)
    html_url = fields.URL(allow_none=True)
    diff_url = fields.URL(allow_none=True)
    patch_url = fields.URL(allow_none=True)
    issue_url = fields.URL(allow_none=True)
    number = fields.Integer(allow_none=True)
    state = fields.String(
        allow_none=True, validate=validate.OneOf(["open", "closed", "merged"])
    )
    locked = fields.Boolean(allow_none=True)
    title = fields.String(allow_none=True)
    user = fields.Nested(UserSchema, allow_none=True)
    body = fields.String(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    closed_at = fields.DateTime(allow_none=True)
    merged_at = fields.DateTime(allow_none=True)
    merge_commit_sha = fields.String(allow_none=True)
    assignee = fields.Nested(UserSchema, allow_none=True)
    assignees = fields.List(fields.Nested(UserSchema), allow_none=True)
    requested_reviewers = fields.List(
        fields.Nested(UserSchema), allow_none=True)
    requested_teams = fields.List(fields.Dict(), allow_none=True)
    labels = fields.Nested(LabelSchema, many=True, allow_none=True)
    milestone = fields.Dict(allow_none=True)
    draft = fields.Boolean(allow_none=True)
    commits_url = fields.URL(allow_none=True)
    review_comments_url = fields.URL(allow_none=True)
    review_comment_url = fields.URL(allow_none=True)
    comments_url = fields.URL(allow_none=True)
    statuses_url = fields.URL(allow_none=True)
    head = fields.Dict(allow_none=True)
    base = fields.Dict(allow_none=True)
    _links = fields.Dict(allow_none=True)
    author_association = fields.String(
        allow_none=True,
        validate=validate.OneOf(
            ["NONE", "OWNER", "COLLABORATOR", "MEMBER", "CONTRIBUTOR"]
        ),
    )
    auto_merge = fields.String(allow_none=True)
    active_lock_reason = fields.String(allow_none=True)


@dataclass
class RequestedReviewersResponse:
    users: Optional[List[User]]
    teams: Optional[List]


class RequestedReviewersResponseSchema(Schema):
    class Meta:
        target = RequestedReviewersResponse
        register_as_scheme = True

    @post_load
    def make_requested_reviewers_response(self, data, **kwargs):
        return RequestedReviewersResponse(**data)

    users = fields.Nested(UserSchema, many=True, allow_none=True)
    teams = fields.List(fields.Dict(), allow_none=True)
