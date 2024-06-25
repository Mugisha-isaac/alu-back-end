#!/usr/bin/python3
import requests
import sys

def get_user_info(user_id):
    user_info_url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    user_tasks_info_url = f'https://jsonplaceholder.typicode.com/users/{user_id}/todos'

    try:
        # Fetching user information
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()

        # Fetching user tasks
        user_tasks_info_response = requests.get(user_tasks_info_url)
        user_tasks_info_response.raise_for_status()

        if user_info_response.status_code == 200 and user_tasks_info_response.status_code == 200:
            user = user_info_response.json()
            tasks = user_tasks_info_response.json()
            
            # Calculate Tasks Progress
            completed_tasks = [task for task in tasks if task['completed']]
            total_tasks = len(tasks)

            # Output formatted Response
            print(f"Employee {user['name']} is done with tasks({len(completed_tasks)}/{total_tasks}):")
            for task in completed_tasks:
                print(f"\t{task['title']}")

        else: 
            print(f"Unexpected status code: {user_info_response.status_code} or {user_tasks_info_response.status_code}")

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <employee_id>")
        sys.exit(1)
    else:
        try:
            user_id = int(sys.argv[1])
            get_user_info(user_id)
        except ValueError:
            print("Invalid employee ID. Please provide a valid integer.")
            sys.exit(1)