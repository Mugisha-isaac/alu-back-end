#!/usr/bin/python3
import json
import os
import requests
import sys


def get_user_info_and_export_to_json(user_id):
    user_info_url = "https://jsonplaceholder.typicode.com/users/{user_id}".format(
        user_id=user_id
    )
    user_tasks_info_url = (
        "https://jsonplaceholder.typicode.com/users/{user_id}/todos".format(
            user_id=user_id
        )
    )

    try:
        # Fetching user information
        user_info_response = requests.get(user_info_url)
        user_info_response.raise_for_status()

        # Fetching user tasks
        user_tasks_info_response = requests.get(user_tasks_info_url)
        user_tasks_info_response.raise_for_status()

        if (
            user_info_response.status_code == 200
            and user_tasks_info_response.status_code == 200
        ):
            user = user_info_response.json()
            tasks = user_tasks_info_response.json()

            # Prepare JSON data
            data = {
                str(user_id): [
                    {
                        "task": task["title"],
                        "completed": task["completed"],
                        "username": user["username"],
                    }
                    for task in tasks
                ]
            }

            # Export to JSON
            json_file = f"{user_id}.json"
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print(f"User info and tasks have been exported to {json_file}")
        else:
            print(
                f"Unexpected status code: {user_info_response.status_code} or {user_tasks_info_response.status_code}"
            )

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <employee_id>")
        sys.exit(1)
    else:
        try:
            user_id = int(sys.argv[1])
            get_user_info_and_export_to_json(user_id)
        except ValueError:
            print("Invalid employee ID. Please provide a valid integer.")
            sys.exit(1)
