from fastapi import FastAPI
import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ambiguity-env"}

@app.get("/tasks")
def get_tasks_endpoint():
    from tasks import get_tasks
    tasks = get_tasks()
    return {
        "tasks": [
            {
                "id": t["id"],
                "name": t["name"],
                "instruction": t["instruction"],
                "required_fields": t["required_fields"],
                "has_grader": True
            }
            for t in tasks
        ]
    }

@app.post("/reset")
def reset():
    try:
        import importlib
        import inference
        importlib.reload(inference)
        inference.main()
        return {"output": "done"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()