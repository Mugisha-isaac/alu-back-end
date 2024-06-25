#!/usr/bin/python3
import requests
import sys
import os
import json

def get_user_info_and_export_to_json(userId):
    userInfoUrl = 'https://jsonplaceholder.typicode.com/users/{userId}'.format(userId=userId)
    userTasksInfoUrl = 'https://jsonplaceholder.typicode.com/users/{userId}/todos'.format(userId=userId)

    try:
        # Fetching user 
        userInfoResponse = requests.get(userInfoUrl)
        userInfoResponse.raise_for_status()

        # Fetching user tasks

        userTasksInfoResponse = requests.get(userTasksInfoUrl)
        userTasksInfoResponse.raise_for_status()

        if userInfoResponse.status_code == 200 and userTasksInfoResponse.status_code == 200:
            user = userInfoResponse.json() 
            tasks = userTasksInfoResponse.json()
            
            # Calculate Tasks Progress
            total_tasks = len(tasks)


            # Prepare JSON
            data = {
                str(userId): [{
                    "task": task['title'],
                    "completed": task['completed'],
                    "username": user['username']
                } for task in tasks]
            }

            # Export to JSON
            json_file = f"{userId}.json"
            with open(json_file, 'w') as file:
                file.write(json.dumps(data, indent=4))
            

            print(f"User info and tasks have been exported to {json_file}")            

        else: 
            print(f"Unexpected status code: {response.status_code}")

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <employeeId>".format(sys.argv[0]))
        sys.exit(1)
    else:
        userId = sys.argv[1]
        get_user_info_and_export_to_json(userId)