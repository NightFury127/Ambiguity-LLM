from tasks import get_random_task


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
        reward = 0
        done = False

        # initialize history if not present
        if not hasattr(self, "history"):
            self.history = []

        if action["type"] == "ask":
            question = action["content"].lower()
            useful = False

            # ❌ repetition penalty
            if question in self.history:
                reward -= 0.2

            for field in self.task["required_fields"]:
                field_text = field.replace("_", " ")

                if (field in question or field_text in question) and field not in self.known_info:
                    self.known_info[field] = self.task["solution"][field]
                    reward += 0.3
                    useful = True

            # ❌ useless question penalty
            if not useful:
                reward -= 0.1

            self.history.append(question)

        elif action["type"] == "execute":
            done = True

            correct_fields = sum(
                1 for f in self.task["required_fields"]
                if f in self.known_info
            )

            completeness_score = correct_fields / len(self.task["required_fields"])

            reward += completeness_score * 0.7

            # ✅ bonus for full completion
            if completeness_score == 1.0:
                reward += 0.3
            else:
                reward -= 0.2  # ❌ penalty for incomplete execution

        return {
            "instruction": self.task["instruction"],
            "known_info": self.known_info,
            "required_fields": self.task["required_fields"]
        }, min(max(reward, 0), 1), done, {}

    def state(self):
        return {
            "task": self.task,
            "known_info": self.known_info
        }