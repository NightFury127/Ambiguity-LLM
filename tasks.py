import random

def grade(task, known_info):
    correct = sum(1 for f in task["required_fields"] if f in known_info)
    return round(correct / len(task["required_fields"]), 2)

def get_tasks():
    return [
        {
            "id": "task_easy",
            "name": "Schedule Meeting",
            "instruction": "Schedule a meeting tomorrow",
            "required_fields": ["time", "participants"],
            "solution": {
                "time": random.choice(["10 AM", "2 PM", "5 PM"]),
                "participants": random.choice(["Alice and Bob", "Team A"])
            },
            "grader": grade
        },
        {
            "id": "task_medium",
            "name": "Send Report",
            "instruction": "Send the report",
            "required_fields": ["report_type", "recipient", "format"],
            "solution": {
                "report_type": random.choice(["Weekly", "Monthly"]),
                "recipient": random.choice(["Manager", "Client"]),
                "format": random.choice(["PDF", "Email"])
            },
            "grader": grade
        },
        {
            "id": "task_hard",
            "name": "Plan Trip",
            "instruction": "Plan a trip",
            "required_fields": ["destination", "dates", "budget"],
            "solution": {
                "destination": random.choice(["Goa", "Manali", "Kerala"]),
                "dates": random.choice(["next week", "next month"]),
                "budget": random.choice(["5000", "10000", "20000"])
            },
            "grader": grade
        }
    ]

def get_random_task():
    return random.choice(get_tasks())