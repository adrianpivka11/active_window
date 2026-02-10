"""Time Entry - functionality"""
import json
import datetime


class TimeEntry():
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime) -> None:
        self.start_time = start_time
        self.end_time = end_time

    def total_time(self) -> datetime.timedelta:
        """Calculate the total time for the time entry."""
        return self.end_time - self.start_time

    def serialize(self) -> dict[str, str]:
        """Serialize the TimeEntry to dictionary."""
        return {
            'start_time' : self.start_time.strftime("%Y-%m-%d %H:%M:%S%Z%z"),
            'end_time' : self.end_time.strftime("%Y-%m-%d %H:%M:%S%Z%z")
        }

    def to_json(self) -> str:
        """Serialize the TimeEntry to JSON string."""
        return json.dumps(self.serialize())
