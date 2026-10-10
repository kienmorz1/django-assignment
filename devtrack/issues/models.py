from django.db import models
from abc import ABC, abstractmethod
from typing import override
from datetime import datetime
# Create your models here.

class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass
    
    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }
    
class Reporter(BaseEntity):
    def __init__(self,id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team
    
    @override
    def validate(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.team:
            raise ValueError("Team cannot be empty")
        if "@" not in self.email:
            raise ValueError("Email must contain '@' symbol")

class Issue(BaseEntity):
    _PRIORITIES = ["low", "medium", "high","critical"]
    _STATUSES = ["open", "in_progress", "closed"]

    def __init__(self, id, title, description, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.reporter_id = reporter_id
        self.status = "open"
        self.created_at = str(datetime.now())
    
    @override
    def validate(self):
        if not isinstance(self.id, int):
            raise ValueError("ID must be an integer")
        if not self.title:
            raise ValueError("Title cannot be empty")
        if not self.description:
            raise ValueError("Description cannot be empty")
        if not self.priority:
            raise ValueError("Priority cannot be empty")
        if self.priority not in self._PRIORITIES:
            raise ValueError("Invalid priority")
        if not self.reporter_id:
            raise ValueError("Reporter ID cannot be empty")
    
    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"[LOW] {self.title} — can be addressed later"
