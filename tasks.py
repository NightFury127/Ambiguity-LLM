import random

def grade(task, known_info):
    correct = sum(1 for f in task["required_fields"] if f in known_info)
    total = len(task["required_fields"])
    raw = correct / total
    return round(0.1 + raw * 0.8, 2)

def get_tasks():
    return [
        {
            "id": "task_easy_1",
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
            "id": "task_easy_2",
            "name": "Order Food",
            "instruction": "Order some food",
            "required_fields": ["restaurant", "items", "delivery_address"],
            "solution": {
                "restaurant": random.choice(["Pizza Hut", "Dominos", "KFC"]),
                "items": random.choice(["2 pizzas", "1 burger combo", "3 wraps"]),
                "delivery_address": random.choice(["home", "office", "hostel"])
            },
            "grader": grade
        },
        {
            "id": "task_medium_1",
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
            "id": "task_medium_2",
            "name": "Book Cab",
            "instruction": "Book a cab for me",
            "required_fields": ["pickup_location", "destination", "time", "cab_type"],
            "solution": {
                "pickup_location": random.choice(["home", "airport", "office"]),
                "destination": random.choice(["airport", "station", "mall"]),
                "time": random.choice(["now", "in 30 mins", "tonight 8 PM"]),
                "cab_type": random.choice(["Mini", "Sedan", "SUV"])
            },
            "grader": grade
        },
        {
            "id": "task_hard_1",
            "name": "Plan Trip",
            "instruction": "Plan a trip for me",
            "required_fields": ["destination", "dates", "budget", "travelers"],
            "solution": {
                "destination": random.choice(["Goa", "Manali", "Kerala"]),
                "dates": random.choice(["next week", "next month"]),
                "budget": random.choice(["5000", "10000", "20000"]),
                "travelers": random.choice(["solo", "couple", "family of 4"])
            },
            "grader": grade
        },
        {
            "id": "task_hard_2",
            "name": "Organize Event",
            "instruction": "Help me organize an event",
            "required_fields": ["event_type", "date", "venue", "guests", "budget"],
            "solution": {
                "event_type": random.choice(["Birthday", "Conference", "Wedding"]),
                "date": random.choice(["this Saturday", "next Sunday", "April 25"]),
                "venue": random.choice(["hotel", "open ground", "banquet hall"]),
                "guests": random.choice(["50", "100", "200"]),
                "budget": random.choice(["50000", "100000", "200000"])
            },
            "grader": grade
        }
    ]

def get_random_task():
    return random.choice(get_tasks())