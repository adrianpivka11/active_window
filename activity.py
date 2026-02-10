"""Activity represent PC application and time intervals when was active."""
from datetime import timedelta
import json
import re
from typing import Any

from time_tracking.active_window.time_entry import TimeEntry


class Activity():

    def __init__(self, window_title: str) -> None:
        """Activity init.

        Args:
            window_title (str): Application name.
        """
        self.window_title = window_title
        self.time_entries: list[TimeEntry] = []

    def add_time_entry(self, time_entry: TimeEntry) -> None:
        """Add time entry.

        Args:
            time_entry (TimeEntry): Time entry
        """
        self.time_entries.append(time_entry)

    def get_time_spent(self) -> timedelta:
        """Compute time spent.

        Returns:
            timedelta: Overall time spent.
        """
        time_spent = timedelta()
        for time_entry in self.time_entries:
            time_spent += time_entry.end_time - time_entry.start_time
        return time_spent

    def serialize(self) -> dict[str, Any]:
        """Serialize activity to dictionary.

        Returns:
            dict[str, Any]: Serialized activity.
        """
        pattern = r' - | \| '
        return {
            'window_title' : self.window_title,
            'window_category': re.split(pattern, str(self.window_title))[-1],
            'time_entries' : [time_entry.serialize() for time_entry in self.time_entries],
            'time_spent' : self.get_time_spent().total_seconds()
        }

    def to_json(self) -> str:
        """Serialize activity to JSON.

        Returns:
            str: Serialized json formatted str.
        """
        return json.dumps(self.serialize())
