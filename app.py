from fastapi import FastAPI
import subprocess
import sys

app = FastAPI()

@app.get("/")
def run_inference():
    try:
        result = subprocess.run(
            [sys.executable, "inference.py"],  # 🔥 IMPORTANT FIX
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}