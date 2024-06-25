#!/usr/bin/python3
import requests
import os
import json

def get_all_users_tasks_and_export_to_json():
    usersInfoUrl = 'https://jsonplaceholder.typicode.com/users'

    try:
        # Fetching user 
        usersInfoResponse = requests.get(usersInfoUrl)
        usersInfoResponse.raise_for_status()

        if usersInfoResponse.status_code == 200:
            users = usersInfoResponse.json() 
            data = {}

            for user in users:
                userId = user['id']
                userTasksInfoUrl = 'https://jsonplaceholder.typicode.com/users/{userId}/todos'.format(userId=userId)
                userTasksInfoResponse = requests.get(userTasksInfoUrl)
                userTasksInfoResponse.raise_for_status()

                if userTasksInfoResponse.status_code == 200:
                    tasks = userTasksInfoResponse.json()

                    # Prepare JSON
                    data[str(userId)] = [{
                        "task": task['title'],
                        "completed": task['completed'],
                        "username": user['username']
                    } for task in tasks]    

                    # Export to JSON

                    json_file = "todo_all_employees.json"
                    with open(json_file, 'w') as file:
                        file.write(json.dumps(data, indent=4))  

                    print(f" User {user['username']} info and his/her tasks have been exported to {json_file}")  

        else: 
            print(f"Unexpected status code: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")


if __name__ == '__main__':

    get_all_users_tasks_and_export_to_json()