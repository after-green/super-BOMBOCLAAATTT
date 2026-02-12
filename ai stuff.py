from enum import Enum
from datetime import datetime


# -------------------
# ENUMS
# -------------------

class TaskStatus(Enum):
    NIEUW = "nieuw"
    BEZIG = "bezig"
    AFGEROND = "afgerond"


class ProjectStatus(Enum):
    OPEN = "open"
    GESLOTEN = "gesloten"


class Priority(Enum):
    LAAG = "laag"
    NORMAAL = "normaal"
    HOOG = "hoog"


# -------------------
# TASK
# -------------------

class Task:

    def __init__(self, title: str, priority: Priority, description: str = ""):
        if not title or not title.strip():
            raise ValueError("Titel mag niet leeg zijn.")

        self._title = title
        self._description = description
        self._priority = priority
        self._status = TaskStatus.NIEUW
        self._created_at = datetime.now()
        self._completed_at = None

    @property
    def title(self):
        return self._title

    @property
    def status(self):
        return self._status

    @property
    def is_completed(self):
        return self._status == TaskStatus.AFGEROND

    def start(self):
        if self._status != TaskStatus.NIEUW:
            raise ValueError("Alleen NIEUW kan naar BEZIG.")
        self._status = TaskStatus.BEZIG

    def complete(self):
        if self._status != TaskStatus.BEZIG:
            raise ValueError("Alleen BEZIG kan naar AFGEROND.")
        self._status = TaskStatus.AFGEROND
        self._completed_at = datetime.now()

    def __repr__(self):
        return f"<Task {self._title} ({self._status.value})>"
    

# -------------------
# PROJECT
# -------------------

class Project:

    def __init__(self, name: str, description: str = ""):
        if not name or not name.strip():
            raise ValueError("Projectnaam mag niet leeg zijn.")

        self._name = name
        self._description = description
        self._status = ProjectStatus.OPEN
        self._tasks = []

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def task_count(self):
        return len(self._tasks)

    def add_task(self, task: Task):
        if self._status == ProjectStatus.GESLOTEN:
            raise ValueError("Geen taken mogelijk in een gesloten project.")

        if any(t.title.lower() == task.title.lower() for t in self._tasks):
            raise ValueError("Taaktitel moet uniek zijn binnen het project.")

        self._tasks.append(task)

    def close(self):
        if not all(task.is_completed for task in self._tasks):
            raise ValueError("Niet alle taken zijn afgerond.")
        self._status = ProjectStatus.GESLOTEN

    def remove_task(self, task_title: str):
        for task in self._tasks:
            if task.title == task_title:
                if not task.is_completed:
                    raise ValueError("Alleen afgeronde taken mogen verwijderd worden.")
                self._tasks.remove(task)
                return
        raise ValueError("Taak niet gevonden.")

    def get_tasks(self):
        return list(self._tasks)

    def __repr__(self):
        return f"<Project {self._name} ({self._status.value}) - {self.task_count} taken>"


# -------------------
# PROJECT SERVICE
# -------------------

class ProjectService:

    def __init__(self):
        self._projects = []

    def create_project(self, name: str, description: str = ""):
        if any(p.name.lower() == name.lower() for p in self._projects):
            raise ValueError("Projectnaam moet uniek zijn.")
        project = Project(name, description)
        self._projects.append(project)
        return project

    def get_projects(self):
        return list(self._projects)


# -------------------
# SIMPLE DEMO (Iteration 1)
# -------------------

if __name__ == "__main__":

    service = ProjectService()

    # Create project
    project = service.create_project("Demo Project", "Test project")

    # Create task
    task1 = Task("Task 1", Priority.HOOG)
    project.add_task(task1)

    # Change status
    task1.start()
    task1.complete()

    # Close project
    project.close()

    print(project)
