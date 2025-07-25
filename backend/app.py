# app.py

from flask_cors import CORS
from flask import Flask, request, jsonify
from compare import calculate_similarity

app = Flask(__name__)
CORS(app)

# ✅ NEW: Function to compare lines and return True/False for each match
def compare_lines(code1, code2):
    lines1 = code1.splitlines()
    lines2 = code2.splitlines()

    max_len = max(len(lines1), len(lines2))

    # Pad shorter list with empty strings
    lines1 += [''] * (max_len - len(lines1))
    lines2 += [''] * (max_len - len(lines2))

    matches1 = []
    matches2 = []

    for l1, l2 in zip(lines1, lines2):
        if l1.strip() == l2.strip() and l1.strip() != '':
            matches1.append(True)
            matches2.append(True)
        else:
            matches1.append(False)
            matches2.append(False)

    return matches1, matches2

# Define a POST route to accept two code inputs
@app.route('/compare', methods=['POST'])
def compare_code():
    data = request.get_json()

    code1 = data.get("code1", "")
    code2 = data.get("code2", "")

    if not code1 or not code2:
        return jsonify({"error": "Both code1 and code2 are required"}), 400

    similarity = calculate_similarity(code1, code2)
    matches1, matches2 = compare_lines(code1, code2)

    # ✅ Return line matching info along with similarity
    return jsonify({
        "similarity_percent": similarity,
        "code1_line_matches": matches1,
        "code2_line_matches": matches2
    })

if __name__ == "__main__":
    app.run(debug=True)
