from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    file = request.files.get('resume')
    if not file:
        return jsonify({'error': 'No resume uploaded'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.save(tmp.name)
            doc = fitz.open(tmp.name)
            text = ""
            for page in doc:
                text += page.get_text()

        # Basic analysis
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
            recommendations.append("Include any internships")

        score = min(score, 100)

        return jsonify({
            "score": score,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
