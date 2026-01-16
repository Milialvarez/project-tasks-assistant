import enum

class ProjectRole(enum.Enum):
    manager = "manager"
    member = "member"

class InvitationStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    expired = "expired"

class SprintStatus(enum.Enum):
    planned = "planned"
    active = "active"
    completed = "completed"

class ObjectiveStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    blocked = "blocked"
    completed = "completed"
    reopened = "reopened"

class BlockerStatus(enum.Enum):
    active = "active"
    resolved = "resolved"
