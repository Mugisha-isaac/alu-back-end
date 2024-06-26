#!/usr/bin/python3
"""
Module: user_info_fetcher

This script fetches user information
and their task completion progress from
a placeholder API,
then prints a summary of completed tasks.

Usage:
    python3 user_info_fetcher.py <employee_id>

The script expects one argument:
    employee_id (int): The ID of the user whose
    information and tasks are to be fetched.

Example:
    python3 user_info_fetcher.py 1

Dependencies:
    - requests: To make HTTP requests to the API.

Exception Handling:
    - Handles HTTP errors during the API requests.
    - Validates that the provided employee_id is an integer.

Author:
    MUGISHA ISAAC
"""

import requests
import sys


def get_user_info(user_id):
    """
    Fetches user information and their tasks from a placeholder API, 
    then prints a summary of completed tasks.

    Args:
        user_id (int): The ID of the user whose information and tasks 
                       are to be fetched.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an 
                                       unsuccessful status code.
    """
    user_info_url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    user_tasks_info_url = (
        f'https://jsonplaceholder.typicode.com/users/{user_id}/todos'
    )

    try:
        # Fetching user information
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()

        # Fetching user tasks
        user_tasks_info_response = requests.get(user_tasks_info_url)
        user_tasks_info_response.raise_for_status()

        if (user_info_response.status_code == 200 and 
                user_tasks_info_response.status_code == 200):
            user = user_info_response.json()
            tasks = user_tasks_info_response.json()
            
            # Calculate Tasks Progress
            completed_tasks = [task for task in tasks if task['completed']]
            total_tasks = len(tasks)

            # Output formatted response
            print(
                f"Employee {user['name']} is done with tasks"
                f"({len(completed_tasks)}/{total_tasks}):"
            )
            for task in completed_tasks:
                print(f"\t{task['title']}")

        else: 
            print(
                f"Unexpected status code: {user_info_response.status_code} or "
                f"{user_tasks_info_response.status_code}"
            )

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")


if __name__ == '__main__':
    """
    Main entry point of the script.

    Validates the command line argument and calls the function to fetch 
    and display user information.

    Usage:
        python3 user_info_fetcher.py <employee_id>

    Example:
        python3 user_info_fetcher.py 1
    """
    # Check for the correct number of command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <employee_id>")
        sys.exit(1)
    else:
        try:
            # Validate and convert user_id from string to integer
            user_id = int(sys.argv[1])
            get_user_info(user_id)
        except ValueError:
            print("Invalid employee ID. Please provide a valid integer.")
            sys.exit(1)
