#!/usr/bin/python3
import requests
import sys

def get_user_info(userId):
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
            completed_tasks = [task for task in tasks if task['completed'] == True]
            total_tasks = len(tasks)

            # Output formatted Response
            print(f"Employee {user['name']} is done with tasks({len(completed_tasks)}/{total_tasks}):")
            for task in completed_tasks:
                print(f"\t {task['title']}")

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
        get_user_info(userId)