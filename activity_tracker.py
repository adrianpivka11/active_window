"""Activity tracker maintain list of all activities."""
from typing import Protocol, Any, Optional
import datetime
import logging
from collections import namedtuple

from pyopenproject.model.user import User
from pyopenproject.model.project import Project

from time_tracking.active_window.activity import Activity
from time_tracking.active_window.time_entry import TimeEntry
from time_tracking.active_window import get_active_window_title

logger = logging.getLogger(__name__)

IdName = namedtuple('IdName', ['id', 'name'])


class Output(Protocol):

    def sink(self, activities: dict[str, Any]) -> None:
        """Sink activities."""
        ...

class ActivityTracker():
    """Activity tracker maintain list of all activities."""
    def __init__(self, user: User) -> None:
        """Activity tracker init.

        Args:
            user (User): User.
        """
        self.user = IdName(user.id, user.name)
        self.project: Optional[IdName] = None
        self.activities: dict[str, Activity] = {}
        logger.info("Activity tracker created for user: %s", self.user.name)

    def _create_activity(self, active_app: str) -> Activity:
        """Creats activity.

        Args:
            active_app (str): Name of active app.

        Returns:
            Activity: Activity class.
        """
        activity = Activity(active_app)
        current_time = datetime.datetime.now()
        activity.add_time_entry(TimeEntry(current_time, current_time))
        return activity

    def start_activity_track(self, project: Project) -> None:
        """Start of activity tracking.

        Args:
            project (Project): Project that user are going to work on.
        """
        self.project = IdName(project.id, project.name)
        active_app = get_active_window_title()
        if active_app in self.activities:
            logger.warning("Activities should be empty: %s", self.serialize())
        self.activities[active_app] = self._create_activity(active_app)
        logger.info("Start of activity tracking for project: %s.", self.project.name)

    def tick(self) -> None:
        """Creates record based on active app."""
        if self.activities:
            active_app = get_active_window_title()
            current_time = datetime.datetime.now()
            logger.debug("Activity tracking tick. Active app: %s.", active_app)
            if active_app in self.activities:
                if self.activities[active_app].time_entries:
                    self.activities[active_app].time_entries[-1].end_time = current_time
                else:
                    logger.warning("Activity without time entry! %s", self.serialize())
            else:
                self.activities[active_app] = self._create_activity(active_app)
        else:
            logger.warning("Tick before start activity tracking!")

    def stop_activity_track(self, out: Output) -> None:
        """End of activity tracking.

        Args:
            out (Output): Object that sinks activities.
        """
        try:
            if self.activities:
                self.tick()
                out.sink(self.serialize())
        finally:
            self.clear_activities()
            logger.info("Stop of activity tracking for project: %s.",
                         self.project.name if self.project else "None")
            self.project = None

    def clear_activities(self) -> None:
        """Clear tracked activities."""
        logger.info("Clear tracked activities for project: %s.",
                     self.project.name if self.project else "None")
        self.activities.clear()

    def serialize(self) -> dict[str, Any]:
        """Serialize activities to dictionary.

        Returns:
            dict[str, Any]: Serialized activities.
        """
        return {
            "user_id": self.user.id,
            "user_name": self.user.name,
            "project_id": self.project.id if self.project else "None",
            "project_name": self.project.name if self.project else "None",
            "activities": [activity.serialize() for activity in self.activities.values()]
        }
