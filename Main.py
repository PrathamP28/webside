import ollama
import os
import json

# ===== CONFIG =====
DEFAULT_PATH = os.path.join(os.getcwd(), "workspace")

# ===== ENSURE WORKSPACE EXISTS =====
os.makedirs(DEFAULT_PATH, exist_ok=True)

# ===== SECURITY FUNCTION =====
def safe_path(path):
    full_path = os.path.abspath(os.path.join(DEFAULT_PATH, path))

    # Prevent going outside workspace
    if not full_path.startswith(os.path.abspath(DEFAULT_PATH)):
        raise Exception("❌ Access denied خارج workspace")

    return full_path

# ===== FILE FUNCTION WITH IF =====
def create_file_if_not_exists(path, content=""):
    try:
        full_path = safe_path(path)

        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w") as f:
                f.write(content)

            return f"✅ File created: {full_path}"
        else:
            return f"⚠️ File already exists: {full_path}"

    except Exception as e:
        return str(e)

# ===== SYSTEM PROMPT =====
SYSTEM_PROMPT = """
You are a smart AI assistant.

Rules:
1. Normal questions → reply normally
2. If user wants to create file → reply ONLY in JSON

Format:
{
  "action": "CREATE_FILE",
  "path": "folder/file.txt",
  "content": "text"
}

Do NOT mix text and JSON.
"""

# ===== MAIN LOOP =====
print("🤖 AI Started (Chat + Safe File Control)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response['message']['content']
    print("\nAI:", reply)

    # ===== TRY ACTION =====
    try:
        data = json.loads(reply)

        if data.get("action") == "CREATE_FILE":
            result = create_file_if_not_exists(
                data["path"],
                data.get("content", "")
            )
            print(result)

    except:
        # Normal chat → nothing to execute
        pass
