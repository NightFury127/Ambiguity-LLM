from fastapi import FastAPI
import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/reset")
def reset():
    try:
        import importlib
        import inference
        importlib.reload(inference)  # reload so env vars are re-read each time
        inference.main()
        return {"output": "done"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()