from env import AmbiguityEnv
from tasks import get_tasks
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
    missing = [f for f in obs.get("required_fields", []) if f not in obs.get("known_info", {})]
    
    prompt = f"""You are an AI agent that resolves ambiguous instructions by asking clarifying questions.

Task instruction: {obs.get("instruction")}
Required fields to complete this task: {obs.get("required_fields")}
Information already known: {obs.get("known_info")}
Still missing: {missing}

Rules:
- If ANY fields are missing, ask for ALL missing fields in ONE single question
- If ALL fields are known, execute the task
- Always return valid JSON only, no explanation

Return exactly one of:
{{"type": "ask", "content": "What is the <missing fields>?"}}
{{"type": "execute", "content": "Complete task with <summary of known info>"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a precise AI assistant. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.1
    )
    text = response.choices[0].message.content.strip()
    # strip markdown code blocks if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    try:
        return json.loads(text)
    except:
        if missing:
            return {"type": "ask", "content": "What is the " + ", ".join(f.replace("_", " ") for f in missing) + "?"}
        return {"type": "execute", "content": "Complete task"}

def run_task(task_def):
    env = AmbiguityEnv()
    env.task = task_def
    env.known_info = {}
    env.done = False
    env.history = []

    obs = {
        "instruction": task_def["instruction"],
        "known_info": env.known_info,
        "required_fields": task_def["required_fields"]
    }

    rewards = []
    log_start(task_def["name"], "ambiguity-env", MODEL_NAME)

    for step in range(1, 7):
        action = get_action_from_llm(obs)
        obs, reward, done, _ = env.step(action)
        rewards.append(reward)
        log_step(step, action, reward, done)
        if done:
            break

    score = min(max(round(sum(rewards) / len(rewards), 2), 0.1), 0.9)
    log_end(done, step, score, rewards)

def main():
    all_tasks = get_tasks()
    for task_def in all_tasks:
        run_task(task_def)

if __name__ == "__main__":
    main()