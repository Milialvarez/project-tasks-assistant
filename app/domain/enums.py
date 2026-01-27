import enum

# project role, a project only has one manager and can have zero or more members
class ProjectRole(enum.Enum):
    manager = "manager"
    member = "member"

# invitation status enum, when a manager of a project sends an invitation to a member of the system these are the availables status
class InvitationStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    expired = "expired"

# sprint status, when a sprint is created these are the available status
class SprintStatus(enum.Enum):
    planned = "planned"
    active = "active"
    completed = "completed"

# objective status, when an objective is defined for a project or an sprint these are the available status
class ObjectiveStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# task status enum, when a task is defined these are the available status, this helps to control the history of a task development
class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    blocked = "blocked"
    completed = "completed"
    reopened = "reopened"

# task blocker status, when a task is blocked by some reason, this are the available status for a blocker
class BlockerStatus(enum.Enum):
    active = "active"
    resolved = "resolved"
