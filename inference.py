from env import AmbiguityEnv
from tasks import get_random_task
from openai import OpenAI
import os
import json

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}")

def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")

def get_action_from_llm(obs):
    prompt = f"""You are an AI agent resolving ambiguous tasks.
Current observation: {json.dumps(obs)}
You must return a JSON object with exactly this format:
- If information is missing: {{"type": "ask", "content": "your question here"}}
- If you have all info: {{"type": "execute", "content": "Complete task"}}
Return only valid JSON, no explanation."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.1
    )
    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except:
        required = obs.get("required_fields", [])
        known = obs.get("known_info", {})
        missing = [f for f in required if f not in known]
        if missing:
            return {"type": "ask", "content": "What is the " + ", ".join(missing) + "?"}
        return {"type": "execute", "content": "Complete task"}

def main():
    env = AmbiguityEnv()
    obs = env.reset()
    rewards = []

    log_start(env.task["name"], "ambiguity-env", MODEL_NAME)

    for step in range(1, 7):
        action = get_action_from_llm(obs)
        obs, reward, done, _ = env.step(action)
        rewards.append(reward)
        log_step(step, action, reward, done)
        if done:
            break

    score = min(max(round(sum(rewards) / len(rewards), 2), 0.1), 0.9)
    log_end(done, step, score, rewards)

if __name__ == "__main__":
    main()