from tasks import get_random_task, grade

class AmbiguityEnv:
    def __init__(self):
        self.task = None
        self.known_info = {}
        self.done = False
        self.history = []

    def reset(self):
        self.task = get_random_task()
        self.known_info = {}
        self.done = False
        self.history = []
        return {
            "instruction": self.task["instruction"],
            "known_info": self.known_info,
            "required_fields": self.task["required_fields"]
        }

    def step(self, action):
        reward = 0.1
        done = False
        if not hasattr(self, "history"):
            self.history = []

        if action["type"] == "ask":
            question = action["content"].lower()
            useful = False
            if question in self.history:
                reward = 0.1
            for field in self.task["required_fields"]:
                field_text = field.replace("_", " ")
                if (field in question or field_text in question) and field not in self.known_info:
                    self.known_info[field] = self.task["solution"][field]
                    useful = True
            if useful:
                reward = grade(self.task, self.known_info)
            self.history.append(question)

        elif action["type"] == "execute":
            done = True
            reward = grade(self.task, self.known_info)

        self.done = done
        # clamp strictly between 0.1 and 0.9
        reward = min(max(round(reward, 2), 0.1), 0.9)
        return {
            "instruction": self.task["instruction"],
            "known_info": self.known_info,
            "required_fields": self.task["required_fields"]
        }, reward, done, {}

    def state(self):
        return {
            "task": self.task,
            "known_info": self.known_info
        }