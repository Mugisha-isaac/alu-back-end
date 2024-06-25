#!/usr/bin/python3
import os
import requests
import sys

def get_user_info_and_export_to_csv(user_id):
    user_info_url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    user_tasks_info_url = f'https://jsonplaceholder.typicode.com/users/{user_id}/todos'

    try:
        # Fetch user information
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()

        # Fetch user tasks
        user_tasks_info_response = requests.get(user_tasks_info_url)
        user_tasks_info_response.raise_for_status()

        if user_info_response.status_code == 200 and user_tasks_info_response.status_code == 200:
            user = user_info_response.json()
            tasks = user_tasks_info_response.json()
            
            # Prepare CSV data
            csv_file = f"{user_id}.csv"
            field_names = ['USER_ID', 'USERNAME', 'TASK_COMPLETED_STATUS', 'TASK_TITLE']
            with open(csv_file, mode='w', encoding='utf-8') as file:
                file.write(','.join(field_names) + '\n')
                for task in tasks:
                    file.write(f"{user_id},{user['username']},{task['completed']},{task['title']}\n")

            print(f"User info and tasks have been exported to {csv_file}")
        else:
            print(f"Unexpected status code: {user_info_response.status_code} or {user_tasks_info_response.status_code}")

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <employee_id>")
        sys.exit(1)
    else:
        try:
            user_id = int(sys.argv[1])
            get_user_info_and_export_to_csv(user_id)
        except ValueError:
            print("Invalid employee ID. Please provide a valid integer.")
            sys.exit(1)