import json
from typing import Any
from typing_extensions import Self
import logging
import datetime

import psycopg2

logger = logging.getLogger(__name__)


class PostgreSQLSink():
    def __init__(
            self, dbname: str, user: str, password: str, host: str, port: str
        ) -> None:
        """PostgreSQP sink init.

        Args:
            dbname (str): Database name.
            user (str): User name.
            password (str): User's password
            host (str): Database host.
            port (str): Database port.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self) -> Self:
        """Enter "with".

        Returns:
            Self: Self object.
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        """Exit "with"."""
        if exc_type:
            logger.error(
                "Exception %s occurred with value %s, during inserting records to PostgreSQL database!",
                exc_type, exc_value)
        self.close()
        return True

    def connect(self) -> None:
        """Connect to PostgreSQL database."""
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        logger.info("Connected to PostgreSQL database. Name: %s, url: %s:%s.",
                     self.dbname, self.host, self.port)

    def close(self) -> None:
        """Close connection to PostgreSQL database."""
        if self.connection:
            self.connection.close()
            logger.info("Connection to PostgreSQL DB closed. Name: %s, url: %s:%s.",
                         self.dbname, self.host, self.port)

    def sink(self, activities: dict[str, Any]) -> None:
        """Sink activities.

        Args:
            activities (dict[str, Any]): Activities to be inserted into PostgreSQL database.
        """
        if self.connection:
            cursor = self.connection.cursor()
            user_id = activities["user_id"]
            user_name = activities["user_name"]
            project_id = activities["project_id"]
            project_name = activities["project_name"]
            for activity in activities["activities"]:
                category = activity["window_category"]
                window_title = activity["window_title"]
                time_spent = activity["time_spent"]
                time_entries = json.dumps(activity["time_entries"])

                # Insert into PostgreSQL table
                insert_query = """
                INSERT INTO records (
                    user_id,
                    user_name,
                    project_id,
                    project_name,
                    date_time,
                    category,
                    window_title,
                    time_spent,
                    time_entries
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (
                    user_id, user_name, project_id, project_name,
                    # activity["time_entries"][0]["start_time"]
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    category, window_title, time_spent, time_entries
                ))

            self.connection.commit()
            cursor.close()
            logger.info("Successfully inserted %s records to PostgreSQL database.", len(activities["activities"]))
        else:
            logger.error("Trying insert %s records, but no connection to PostgreSQL database!",
                          len(activities["activities"]))
