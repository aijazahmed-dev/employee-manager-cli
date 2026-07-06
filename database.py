from typing import Optional
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    filename="employee_manager.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Initialize the DatabaseManager with the SQLite database name.

    Args:
        db_name (str): Name of the SQLite database file.
    """
    def __init__(self, db_name: str = "employees.db") -> None:
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establish a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            logger.info("Database connection established.")
        except sqlite3.Error:
            logger.exception("Database connection failed.")
            raise

    def create_table(self):
        """
        Create the employees table if it does not already exist.

        Raises:
            ConnectionError: If the database is not connected.
            sqlite3.Error: If table creation fails.
        """
        if self.connection is None:
            raise ConnectionError("Database connection has not been established.")
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            joining_date TEXT NOT NULL
        );
        """

        try:
            if self.connection is None:
                raise ConnectionError("Database connection has not been established.")
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            logger.info("Employees table created successfully or already exists.")
        except sqlite3.Error as e:
            logger.exception(f"Failed to create table: {e}")
            raise

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed.")


if __name__ == "__main__":
    db = DatabaseManager()

    try:
        db.connect()
        db.create_table()
    except sqlite3.Error:
        logger.exception("Database initialization failed.")
    finally:
        db.close()