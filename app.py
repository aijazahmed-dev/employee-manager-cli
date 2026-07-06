import argparse
from tabulate import tabulate
from employee_service import EmployeeService
from employee import Employee
from database import DatabaseManager


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Employee Management System"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available commands"
    )

    # Add Employee Command
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new employee"
    )

    add_parser.add_argument(
        "--name",
        required=True,
        help="Employee full name"
    )

    add_parser.add_argument(
        "--email",
        required=True,
        help="Employee email"
    )

    add_parser.add_argument(
        "--department",
        required=True,
        help="Employee department"
    )

    add_parser.add_argument(
        "--position",
        required=True,
        help="Employee position"
    )

    add_parser.add_argument(
        "--salary",
        required=True,
        type=float,
        help="Employee salary"
    )

    add_parser.add_argument(
        "--joining-date",
        required=True,
        help="Joining date (YYYY-MM-DD)"
    )

    update_parser = subparsers.add_parser(
    "update",
    help="Update an existing employee"
    )

    update_parser.add_argument(
    "--id",
    type=int,
    required=True,
    help="Employee ID"
)

    update_parser.add_argument(
    "--name",
    required=True,
    help="Employee full name"
    )

    update_parser.add_argument(
    "--email",
    required=True,
    help="Employee email"
    )

    update_parser.add_argument(
    "--department",
    required=True,
    help="Employee department"
    )

    update_parser.add_argument(
    "--position",
    required=True,
    help="Employee position"
    )

    update_parser.add_argument(
    "--salary",
    type=float,
    required=True,
    help="Employee salary"
    )

    update_parser.add_argument(
    "--joining-date",
    required=True,
    help="Joining date (YYYY-MM-DD)"
    )

    delete_parser = subparsers.add_parser(
    "delete",
    help="Delete an employee"
    )

    delete_parser.add_argument(
    "--id",
    type=int,
    required=True,
    help="Employee ID"
    )

    subparsers.add_parser(
    "list",
    help="Display all employees"
    )

    search_parser = subparsers.add_parser(
    "search",
    help="Search employees by name or email"
    )

    search_parser.add_argument(
    "--keyword",
    required=True,
    help="Employee name or email"
    )

    return parser


def handle_add(service: EmployeeService, args) -> None:
    """Handle the add command."""

    employee = Employee(
        full_name=args.name,
        email=args.email,
        department=args.department,
        position=args.position,
        salary=args.salary,
        joining_date=args.joining_date,
    )

    service.add_employee(employee)

    print("✅ Employee added successfully.")


def handle_list(service: EmployeeService) -> None:
    """Display all employees."""

    employees = service.get_all_employees()

    if not employees:
        print("No employees found.")
        return

    table = [
        [
            employee.id,
            employee.full_name,
            employee.email,
            employee.department,
            employee.position,
            employee.salary,
            employee.joining_date,
        ]
        for employee in employees
    ]

    print(
        tabulate(
            table,
            headers=[
                "ID",
                "Full Name",
                "Email",
                "Department",
                "Position",
                "Salary",
                "Joining Date",
            ],
            tablefmt="grid",
        )
    )


def handle_search(service: EmployeeService, args) -> None:
    """Search employees by name or email."""

    employees = service.search_employee(args.keyword)

    if not employees:
        print("No matching employees found.")
        return

    table = [
        [
            employee.id,
            employee.full_name,
            employee.email,
            employee.department,
            employee.position,
            employee.salary,
            employee.joining_date,
        ]
        for employee in employees
    ]

    print(
        tabulate(
            table,
            headers=[
                "ID",
                "Full Name",
                "Email",
                "Department",
                "Position",
                "Salary",
                "Joining Date",
            ],
            tablefmt="grid",
        )
    )

def handle_update(service: EmployeeService, args) -> None:
    """Handle the update command."""

    employee = Employee(
        full_name=args.name,
        email=args.email,
        department=args.department,
        position=args.position,
        salary=args.salary,
        joining_date=args.joining_date,
    )

    updated = service.update_employee(args.id, employee)

    if updated:
        print("Employee updated successfully.")
    else:
        print("Employee not found.")


def handle_delete(service: EmployeeService, args) -> None:
    """Handle the delete command with confirmation."""

    confirm = input(
        f"Are you sure you want to delete employee ID {args.id}? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Delete operation cancelled.")
        return

    deleted = service.delete_employee(args.id)

    if deleted:
        print("Employee deleted successfully.")
    else:
        print("Employee not found.")

        

def main() -> None:
    """Application entry point."""

    db = DatabaseManager()

    try:
        db.connect()
        db.create_table()

        service = EmployeeService(db)

        parser = create_parser()
        args = parser.parse_args()

        if args.command == "add":
            handle_add(service, args)

        elif args.command == "list":
            handle_list(service)

        elif args.command == "search":
            handle_search(service, args)

        elif args.command == "update":
            handle_update(service, args)

        elif args.command == "delete":
            handle_delete(service, args)
        
    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()

