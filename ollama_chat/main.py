import argparse
import requests
from datetime import datetime, timezone
import os
import uuid
import json
import threading
import time
import platform
import hashlib

LOG_FILE = "ollama_chat_log.jsonl"


def log_interaction(session_id, prompt, response, model, metadata):
    eval_us = metadata.get("eval_duration", 0)
    total_us = metadata.get("total_duration", 0)
    tokens = metadata.get("eval_count", 0)
    eval_sec = round(eval_us / 1_000_000, 2)
    total_sec = round(total_us / 1_000_000, 2)
    tps = round(tokens / eval_sec, 2) if eval_sec else None

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "username": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "cwd": os.getcwd(),
        "shell": os.environ.get("SHELL", "unknown"),
        "os": platform.platform(),
        "model": model,
        "prompt": prompt,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:8],
        "response": response,
        "tokens_generated": tokens,
        "generation_time": f"{eval_sec}s",
        "total_request_time": f"{total_sec}s",
        "tokens_per_second": tps
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def spinner(stop_event):
    while not stop_event.is_set():
        for ch in "|/-\\":
            print(f"\r⏳ Thinking... {ch}", end="", flush=True)
            time.sleep(0.1)
    print("\r", end="", flush=True)


def chat_loop(model: str, session_id: str):
    print(f"🤖 Starting chat with model '{model}' | Type ':exit' to quit\n")

    while True:
        try:
            prompt = input("> ").strip()
            if prompt.lower() in (":exit", "exit", "quit"):
                print("\n🧠  Goodbye!\n")
                break

            stop_event = threading.Event()
            t = threading.Thread(target=spinner, args=(stop_event,))
            t.start()

            res = requests.post("http://localhost:11434/api/generate", json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })

            stop_event.set()
            t.join()

            data = res.json()
            response = data.get("response", "[No response]")

            print(f"\n[Response]\n{response}\n")
            log_interaction(session_id, prompt, response, model, data)

        except KeyboardInterrupt:
            print("\n🧠  Chat interrupted. Exiting...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break


def main():
    parser = argparse.ArgumentParser(description="Chat with an Ollama model.")
    parser.add_argument("--model", type=str,
                        default="mistral", help="Ollama model to use")
    parser.add_argument("--session", type=str, help="Optional session ID")
    args = parser.parse_args()

    session_id = args.session or str(uuid.uuid4())
    chat_loop(args.model, session_id)


if __name__ == "__main__":
    main()
