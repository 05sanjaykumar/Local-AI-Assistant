from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
MEMORY_FILE = "./data/user_memory.json"

# Load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {"user_id": None, "conversation_history": []}

# Save memory to file
def save_memory(data):
    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Delete memory file
def delete_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        return True
    return False

# Route to get memory
@app.route("/memory", methods=["GET"])
def get_memory():
    memory = load_memory()
    return jsonify(memory)

# Route to update memory
@app.route("/memory", methods=["POST"])
def update_memory():
    data = request.json
    memory = load_memory()
    memory["conversation_history"].append(data)
    save_memory(memory)
    return jsonify({"message": "Memory updated."})

# Route to delete memory
@app.route("/memory", methods=["DELETE"])
def clear_memory():
    if delete_memory():
        return jsonify({"message": "Memory cleared."})
    return jsonify({"message": "No memory to delete."}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
