# 🧠 ollama-chat

A simple, terminal-based CLI chat app for Ollama models (like `mistral`), with built-in metadata logging.

Supports:
- Chatting with any local Ollama model
- Logs prompts, responses, and useful metadata (`tokens/sec`, `duration`, `prompt hash`, etc.)
- Session tracking
- Clean output with a loading spinner

---

## 🔧 Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running locally
- A local model (e.g., `mistral`) already pulled via:

```bash
ollama pull mistral
```

---

## 🚀 Installation

Clone the repo and install it locally:

```bash
git clone https://github.com/yourusername/ollama-chat.git
cd ollama-chat
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```

---

## 💬 Usage

Start chatting with a model:

```bash
ollama-chat --model mistral
```

Optional: Add a session ID for tracking:

```bash
ollama-chat --model mistral --session morning_debug
```

---

## 🧾 Log Output

All interactions are logged to:

```text
ollama_chat_log.jsonl
```

Each log entry includes:
- Timestamp
- Prompt + Response
- Model name
- Prompt hash
- Token count
- Duration info
- Tokens per second
- Username, working directory, shell, OS

---

## 📟 Real-Time Log Viewer (Optional)

Install `jq` to stream pretty logs:

```bash
# macOS
brew install jq

# Ubuntu (WSL/Linux)
sudo apt install jq
```

Then run:

```bash
tail -f ollama_chat_log.jsonl | jq -r '"\n[" + .timestamp + "]\n🗣️ " + .prompt + "\n🧠 " + .response + "\n---"'
```

OR

```bash
tail -f ollama_chat_log.jsonl | jq '{timestamp, session_id, username, shell, os, model, prompt_hash, tokens_generated, generation_time, total_request_time, prompt, response}'
```

---

## 🧪 Testing

Test basic functionality:

```bash
ollama-chat --model mistral --session test
```

Make sure `ollama_chat_log.jsonl` is created and includes output after a prompt.

---

## 🗑 .gitignore

Recommended `.gitignore`:

```
*.jsonl
*.pyc
__pycache__/
*.egg-info/
.venv/
```

---

## 📄 License

MIT – do whatever you want. Just don't prompt-inject me.
