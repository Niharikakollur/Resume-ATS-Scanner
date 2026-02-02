from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

company_rules = {
    "TCS": ["python", "sql", "communication"],
    "Infosys": ["java", "dsa", "projects"],
    "Google": ["projects", "github", "dsa", "internship"]
}

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        pdf = request.files["resume"]
        company = request.form["company"]

        text = extract_text_from_pdf(pdf)

        score = 0
        total = 0
        report = ""

        checks = {
            "Email": "@" in text,
            "Phone": any(c.isdigit() for c in text),
            "Skills": "skills" in text,
            "Projects": "projects" in text,
            "LinkedIn": "linkedin" in text,
            "GitHub": "github" in text,
        }

        for c, ok in checks.items():
            total += 1
            if ok:
                score += 1
            else:
                report += f"{c} missing<br>"

        for skill in company_rules[company]:
            total += 1
            if skill in text:
                score += 1
            else:
                report += f"{skill} missing<br>"

        percent = int((score / total) * 100)

        if percent >= 70:
            status = "Approved"
        else:
            status = "Rejected"

        result = f"""
        <h3>{status} for {company}</h3>
        <h4>ATS Score: {percent}%</h4>
        <p>{report}</p>
        """

    return render_template("index.html", result=result, companies=company_rules.keys())


if __name__ == "__main__":
    app.run(debug=True)
