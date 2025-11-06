from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import tempfile
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests from your Live Preview

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "")

    if not code or not language:
        return jsonify({"error": "Missing code or language"}), 400

    try:
        if language == "python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
                temp_file.write(code)
                temp_file.flush()
                result = subprocess.run(["python", temp_file.name], capture_output=True, text=True)
                output = result.stdout or result.stderr
            os.remove(temp_file.name)

        elif language == "cpp":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as temp_file:
                temp_file.write(code)
                temp_file.flush()
                exe_file = temp_file.name.replace(".cpp", ".exe")
                compile_result = subprocess.run(["g++", temp_file.name, "-o", exe_file], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    output = compile_result.stderr
                else:
                    run_result = subprocess.run([exe_file], capture_output=True, text=True)
                    output = run_result.stdout or run_result.stderr
                os.remove(temp_file.name)
                if os.path.exists(exe_file):
                    os.remove(exe_file)
        else:
            return jsonify({"error": "Unsupported language"}), 400

        return jsonify({"output": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
