import random


def get_random_task():
    tasks = [
        {
            "instruction": "Plan a trip",
            "required_fields": ["destination", "dates", "budget"],
            "solution": {
                "destination": random.choice(["Goa", "Manali", "Kerala"]),
                "dates": random.choice(["next week", "next month", "December"]),
                "budget": random.choice(["5000", "10000", "20000"])
            }
        },
        {
            "instruction": "Send a report",
            "required_fields": ["report_type", "recipient", "format"],
            "solution": {
                "report_type": random.choice(["Weekly", "Monthly", "Annual"]),
                "recipient": random.choice(["Manager", "Client", "Team Lead"]),
                "format": random.choice(["PDF", "Email", "Presentation"])
            }
        },
        {
            "instruction": "Schedule a meeting",
            "required_fields": ["time", "participants"],
            "solution": {
                "time": random.choice(["10 AM", "2 PM", "5 PM"]),
                "participants": random.choice(["Alice and Bob", "Team A", "Project group"])
            }
        }
    ]

    return random.choice(tasks)