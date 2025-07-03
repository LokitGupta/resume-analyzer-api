from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import requests
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.json
    file_url = data.get('file_url')
    if not file_url:
        return jsonify({"error": "Missing file_url"}), 400

    try:
        response = requests.get(file_url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        text = ""
        for page in doc:
            text += page.get_text()

        score = 0
        recommendations = []

        if "Python" in text:
            score += 20
        else:
            recommendations.append("Add Python experience")

        if "Machine Learning" in text:
            score += 20
        else:
            recommendations.append("Mention ML skills")

        if "Internship" in text:
            score += 20
        else:
            recommendations.append("Include internships")

        return jsonify({
            "score": score,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
