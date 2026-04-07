from fastapi import FastAPI
import subprocess
import sys
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/reset")
def reset():
    try:
        result = subprocess.run(
            [sys.executable, "inference.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return {"output": result.stdout.strip()}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()