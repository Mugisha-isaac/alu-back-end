#!/usr/bin/python3
"""
Module: user_data_exporter

This script fetches user information and their tasks from a placeholder API and exports the data to a CSV file.

Usage:
    python3 user_data_exporter.py <employee_id>

The script expects one argument:
    employee_id (int): The ID of the user whose information and tasks are to be fetched.

Example:
    python3 user_data_exporter.py 1

Dependencies:
    - requests: To make HTTP requests to the API.

Exception Handling:
    - Handles HTTP errors during the API requests.
    - Validates that the provided employee_id is an integer.

Author:
    MUGISHA ISAAC
"""

import os
import requests
import sys


def get_user_info_and_export_to_csv(user_id):
    """
    Fetches user information and their tasks from a placeholder API, then exports the data to a CSV file.

    Args:
        user_id (int): The ID of the user whose information and tasks are to be fetched.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    # Define URLs to fetch user information and tasks
    user_info_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    user_tasks_info_url = f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"

    try:
        # Fetch user information
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()

        # Fetch user tasks
        user_tasks_info_response = requests.get(user_tasks_info_url)
        user_tasks_info_response.raise_for_status()

        if (
            user_info_response.status_code == 200
            and user_tasks_info_response.status_code == 200
        ):
            # Parse JSON responses
            user = user_info_response.json()
            tasks = user_tasks_info_response.json()

            # Prepare CSV data
            csv_file = f"{user_id}.csv"
            field_names = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
            with open(csv_file, mode="w", encoding="utf-8") as file:
                file.write(",".join(field_names) + "\n")
                for task in tasks:
                    # Write task data to CSV
                    file.write(
                        f"{user_id},{user['username']},{task['completed']},{task['title']}\n"
                    )

            print(f"User info and tasks have been exported to {csv_file}")
        else:
            print(
                f"Unexpected status code: {user_info_response.status_code} or {user_tasks_info_response.status_code}"
            )

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    """
    Main entry point of the script.

    Validates the command line argument and calls the function to fetch and export user information.

    Usage:
        python3 user_data_exporter.py <employee_id>

    Example:
        python3 user_data_exporter.py 1
    """
    # Check for the correct number of command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <employee_id>")
        sys.exit(1)
    else:
        try:
            # Validate and convert user_id from string to integer
            user_id = int(sys.argv[1])
            get_user_info_and_export_to_csv(user_id)
        except ValueError:
            print("Invalid employee ID. Please provide a valid integer.")
            sys.exit(1)
