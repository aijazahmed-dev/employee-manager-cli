import logging
import sqlite3
from typing import List
import csv

from database import DatabaseManager
from employee import Employee

logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def add_employee(self, employee: Employee) -> None:
        query = """
        INSERT INTO employees
        (full_name, email, department, position, salary, joining_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        try:
            if self.database.connection is None:
                raise ConnectionError("Database connection has not been established.")

            cursor = self.database.connection.cursor()

            cursor.execute(
                query,
                (
                    employee.full_name,
                    employee.email,
                    employee.department,
                    employee.position,
                    employee.salary,
                    employee.joining_date,
                ),
            )

            self.database.connection.commit()
            logger.info("Employee added successfully.")

        except sqlite3.Error:
            logger.exception("Failed to add employee.")
            raise

    def get_all_employees(self) -> List[Employee]:
        query = "SELECT * FROM employees"

        try:
            if self.database.connection is None:
                raise ConnectionError("Database connection has not been established.")

            cursor = self.database.connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            return [
                Employee(
                    id=row[0],
                    full_name=row[1],
                    email=row[2],
                    department=row[3],
                    position=row[4],
                    salary=row[5],
                    joining_date=row[6],
                )
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception("Failed to retrieve employees.")
            raise

    def search_employee(self, search_term: str) -> List[Employee]:
        query = """
        SELECT *
        FROM employees
        WHERE full_name LIKE ?
        OR email LIKE ?
        """

        try:
            if self.database.connection is None:
                raise ConnectionError("Database connection has not been established.")

            cursor = self.database.connection.cursor()

            cursor.execute(
                query,
                (f"%{search_term}%", f"%{search_term}%"),
            )

            rows = cursor.fetchall()

            return [
                Employee(
                    id=row[0],
                    full_name=row[1],
                    email=row[2],
                    department=row[3],
                    position=row[4],
                    salary=row[5],
                    joining_date=row[6],
                )
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception("Search failed.")
            raise

    def update_employee(self, employee_id: int, employee: Employee) -> bool:
        query = """
        UPDATE employees
        SET
            full_name=?,
            email=?,
            department=?,
            position=?,
            salary=?,
            joining_date=?
        WHERE id=?
        """

        try:
            if self.database.connection is None:
                raise ConnectionError("Database connection has not been established.")

            cursor = self.database.connection.cursor()

            cursor.execute(
                query,
                (
                    employee.full_name,
                    employee.email,
                    employee.department,
                    employee.position,
                    employee.salary,
                    employee.joining_date,
                    employee_id,
                ),
            )

            self.database.connection.commit()

            logger.info("Employee updated.")

            return cursor.rowcount > 0

        except sqlite3.Error:
            logger.exception("Update failed.")
            raise

    def delete_employee(self, employee_id: int) -> bool:
        query = "DELETE FROM employees WHERE id=?"

        try:
            if self.database.connection is None:
                raise ConnectionError("Database connection has not been established.")

            cursor = self.database.connection.cursor()
            cursor.execute(query, (employee_id,))
            self.database.connection.commit()

            logger.info("Employee deleted.")

            return cursor.rowcount > 0

        except sqlite3.Error:
            logger.exception("Delete failed.")
            raise

    def export_to_csv(self, file_path: str) -> None:
        """Export all employees to a CSV file."""

        employees = self.get_all_employees()

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Header
                writer.writerow([
                    "ID",
                    "Full Name",
                    "Email",
                    "Department",
                    "Position",
                    "Salary",
                    "Joining Date"
                ])

                # Data rows
                for emp in employees:
                    writer.writerow([
                        emp.id,
                        emp.full_name,
                        emp.email,
                        emp.department,
                        emp.position,
                        emp.salary,
                        emp.joining_date
                    ])

            logger.info("Employees exported to CSV successfully.")

        except Exception as e:
            logger.exception(f"Failed to export employees to CSV: {e}")
            raise