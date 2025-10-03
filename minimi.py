from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import json
import itertools
import datetime


_id_counter = itertools.count(1)


def _next_id() -> int:
    return next(_id_counter)


@dataclass
class User:
    id: int
    name: str


@dataclass
class Comment:
    id: int
    author_id: int
    body: str
    created_at: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )


@dataclass
class Issue:
    id: int
    title: str
    description: str = ""
    status: str = "todo"  # todo, in_progress, done, etc.
    assignee_id: Optional[int] = None
    labels: List[str] = field(default_factory=list)
    priority: int = 100  # lower is higher priority
    comments: List[Comment] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )


@dataclass
class Sprint:
    id: int
    name: str
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    issues: List[int] = field(default_factory=list)
    active: bool = False


@dataclass
class Board:
    id: int
    name: str
    projects: List[str] = field(default_factory=list)
    issues: Dict[int, Issue] = field(default_factory=dict)
    sprints: Dict[int, Sprint] = field(default_factory=dict)


class BoardManager:
    """
    Simple in-memory manager that implements core operations for a Linear/Jira-like board.
    Designed for unit testing and as a foundation for API handlers or persistence later.
    """

    def __init__(self):
        self.boards: Dict[int, Board] = {}
        self.users: Dict[int, User] = {}

    # -- board/project lifecycle
    def create_board(self, name: str) -> Board:
        b = Board(id=_next_id(), name=name)
        self.boards[b.id] = b
        return b

    def add_project(self, board_id: int, project_name: str) -> None:
        board = self.boards[board_id]
        if project_name not in board.projects:
            board.projects.append(project_name)

    # -- user management
    def create_user(self, name: str) -> User:
        u = User(id=_next_id(), name=name)
        self.users[u.id] = u
        return u

    # -- issue CRUD
    def create_issue(
        self,
        board_id: int,
        title: str,
        description: str = "",
        assignee_id: Optional[int] = None,
        labels: Optional[List[str]] = None,
        priority: int = 100,
    ) -> Issue:
        board = self.boards[board_id]
        issue = Issue(
            id=_next_id(),
            title=title,
            description=description,
            assignee_id=assignee_id,
            labels=labels or [],
            priority=priority,
        )
        board.issues[issue.id] = issue
        return issue

    def get_issue(self, board_id: int, issue_id: int) -> Issue:
        return self.boards[board_id].issues[issue_id]

    def update_issue(self, board_id: int, issue_id: int, **fields) -> Issue:
        issue = self.get_issue(board_id, issue_id)
        for k, v in fields.items():
            if hasattr(issue, k):
                setattr(issue, k, v)
        issue.updated_at = datetime.datetime.utcnow().isoformat()
        return issue

    def delete_issue(self, board_id: int, issue_id: int) -> None:
        board = self.boards[board_id]
        board.issues.pop(issue_id, None)
        # remove from sprints if present
        for sprint in board.sprints.values():
            if issue_id in sprint.issues:
                sprint.issues.remove(issue_id)

    def list_issues(
        self,
        board_id: int,
        status: Optional[str] = None,
        assignee_id: Optional[int] = None,
        labels: Optional[List[str]] = None,
        sort_by_priority: bool = False,
    ) -> List[Issue]:
        issues = list(self.boards[board_id].issues.values())
        if status:
            issues = [i for i in issues if i.status == status]
        if assignee_id is not None:
            issues = [i for i in issues if i.assignee_id == assignee_id]
        if labels:
            issues = [i for i in issues if all(l in i.labels for l in labels)]
        if sort_by_priority:
            issues.sort(key=lambda i: i.priority)
        return issues

    # -- assignment, labels, comments
    def assign_issue(
        self, board_id: int, issue_id: int, user_id: Optional[int]
    ) -> Issue:
        return self.update_issue(board_id, issue_id, assignee_id=user_id)

    def add_label(self, board_id: int, issue_id: int, label: str) -> Issue:
        issue = self.get_issue(board_id, issue_id)
        if label not in issue.labels:
            issue.labels.append(label)
            issue.updated_at = datetime.datetime.utcnow().isoformat()
        return issue

    def remove_label(self, board_id: int, issue_id: int, label: str) -> Issue:
        issue = self.get_issue(board_id, issue_id)
        if label in issue.labels:
            issue.labels.remove(label)
            issue.updated_at = datetime.datetime.utcnow().isoformat()
        return issue

    def add_comment(
        self, board_id: int, issue_id: int, author_id: int, body: str
    ) -> Comment:
        issue = self.get_issue(board_id, issue_id)
        c = Comment(id=_next_id(), author_id=author_id, body=body)
        issue.comments.append(c)
        issue.updated_at = datetime.datetime.utcnow().isoformat()
        return c

    # -- workflow
    def move_issue(self, board_id: int, issue_id: int, new_status: str) -> Issue:
        return self.update_issue(board_id, issue_id, status=new_status)

    def prioritize_issue(self, board_id: int, issue_id: int, priority: int) -> Issue:
        return self.update_issue(board_id, issue_id, priority=priority)

    # -- sprints
    def create_sprint(self, board_id: int, name: str) -> Sprint:
        board = self.boards[board_id]
        s = Sprint(id=_next_id(), name=name)
        board.sprints[s.id] = s
        return s

    def add_issue_to_sprint(self, board_id: int, sprint_id: int, issue_id: int) -> None:
        board = self.boards[board_id]
        sprint = board.sprints[sprint_id]
        if issue_id not in sprint.issues and issue_id in board.issues:
            sprint.issues.append(issue_id)

    def remove_issue_from_sprint(
        self, board_id: int, sprint_id: int, issue_id: int
    ) -> None:
        board = self.boards[board_id]
        sprint = board.sprints[sprint_id]
        if issue_id in sprint.issues:
            sprint.issues.remove(issue_id)

    def start_sprint(self, board_id: int, sprint_id: int) -> Sprint:
        board = self.boards[board_id]
        sprint = board.sprints[sprint_id]
        sprint.active = True
        sprint.start_at = sprint.start_at or datetime.datetime.utcnow().isoformat()
        return sprint

    def close_sprint(self, board_id: int, sprint_id: int) -> Sprint:
        board = self.boards[board_id]
        sprint = board.sprints[sprint_id]
        sprint.active = False
        sprint.end_at = datetime.datetime.utcnow().isoformat()
        return sprint

    # -- search & export
    def search_issues(self, board_id: int, query: str) -> List[Issue]:
        q = query.lower()
        return [
            i
            for i in self.boards[board_id].issues.values()
            if q in i.title.lower() or q in i.description.lower()
        ]

    def export_board(self, board_id: int) -> str:
        board = self.boards[board_id]
        # convert dataclasses -> dict
        serializable = {
            "id": board.id,
            "name": board.name,
            "projects": board.projects,
            "issues": {iid: asdict(issue) for iid, issue in board.issues.items()},
            "sprints": {sid: asdict(s) for sid, s in board.sprints.items()},
        }
        return json.dumps(serializable, indent=2)

    def import_board(self, data: str) -> Board:
        payload = json.loads(data)
        board = Board(id=payload.get("id", _next_id()), name=payload["name"])
        board.projects = payload.get("projects", [])
        for iid, idata in payload.get("issues", {}).items():
            iid_int = int(iid)
            issue = Issue(
                id=iid_int,
                title=idata["title"],
                description=idata.get("description", ""),
                status=idata.get("status", "todo"),
                assignee_id=idata.get("assignee_id"),
                labels=idata.get("labels", []),
                priority=idata.get("priority", 100),
                comments=[Comment(**c) for c in idata.get("comments", [])],
                created_at=idata.get(
                    "created_at", datetime.datetime.utcnow().isoformat()
                ),
                updated_at=idata.get(
                    "updated_at", datetime.datetime.utcnow().isoformat()
                ),
            )
            board.issues[iid_int] = issue
        for sid, sdata in payload.get("sprints", {}).items():
            sid_int = int(sid)
            sprint = Sprint(
                id=sid_int,
                name=sdata["name"],
                start_at=sdata.get("start_at"),
                end_at=sdata.get("end_at"),
                issues=sdata.get("issues", []),
                active=sdata.get("active", False),
            )
            board.sprints[sid_int] = sprint
        self.boards[board.id] = board
        return board
