#!/usr/bin/python3
import requests
import json


def get_all_users_tasks_and_export_to_json():
    users_info_url = "https://jsonplaceholder.typicode.com/users"

    try:
        # Fetch all users
        users_info_response = requests.get(users_info_url)
        users_info_response.raise_for_status()

        if users_info_response.status_code == 200:
            users = users_info_response.json()
            data = {}

            # Iterate over each user to fetch their tasks
            for user in users:
                user_id = user["id"]
                user_tasks_info_url = (
                    f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"
                )

                user_tasks_response = requests.get(user_tasks_info_url)
                user_tasks_response.raise_for_status()

                if user_tasks_response.status_code == 200:
                    tasks = user_tasks_response.json()

                    # Prepare user's task data
                    data[str(user_id)] = [
                        {
                            "task": task["title"],
                            "completed": task["completed"],
                            "username": user["username"],
                        }
                        for task in tasks
                    ]

            # Export to JSON
            json_file = "todo_all_employees.json"
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print(f"All users' info and tasks have been exported to {json_file}")

        else:
            print(f"Unexpected status code: {users_info_response.status_code}")

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    get_all_users_tasks_and_export_to_json()
