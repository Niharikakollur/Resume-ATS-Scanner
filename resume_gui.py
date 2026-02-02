import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# -------- PDF TEXT EXTRACT --------
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()


# -------- COMPANY RULES --------
company_rules = {
    "TCS": ["python", "sql", "communication"],
    "Infosys": ["java", "dsa", "projects"],
    "Google": ["projects", "github", "dsa", "internship"]
}

# -------- FUNCTIONS --------
def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    messagebox.showinfo("File Selected", file_path)

def scan_resume():
    if not file_path:
        messagebox.showerror("Error", "Please upload resume first")
        return

    company = company_var.get()
    text = extract_text_from_pdf(file_path)

    score = 0
    total_checks = 0
    report = ""

    # ----- Basic ATS Checks -----
    checks = {
        "Email": "@" in text,
        "Phone Number": any(char.isdigit() for char in text),
        "Skills Section": "skills" in text,
        "Projects Section": "projects" in text,
        "LinkedIn": "linkedin" in text,
        "GitHub": "github" in text,
        "Education": "education" in text,
    }

    for check, passed in checks.items():
        total_checks += 1
        if passed:
            score += 1
        else:
            report += f"❌ {check} missing\n"

    # ----- Company Skill Checks -----
    required_skills = company_rules.get(company, [])
    for skill in required_skills:
        total_checks += 1
        if skill in text:
            score += 1
        else:
            report += f"❌ Missing skill: {skill}\n"

    # ----- Score Calculation -----
    percentage = int((score / total_checks) * 100)

    # ----- Result -----
    if percentage >= 70:
        status = f"✅ Approved for {company}"
        color = "green"
    else:
        status = f"❌ Rejected for {company}"
        color = "red"

    final_msg = f"{status}\n\nATS Score: {percentage}%\n\nIssues:\n{report}"
    result_label.config(text=final_msg, fg=color)

"""def scan_resume():
    if not file_path:
        messagebox.showerror("Error", "Please upload resume first")
        return

    company = company_var.get()
    text = extract_text_from_pdf(file_path)

    required_skills = company_rules.get(company, [])
    missing = []

    for skill in required_skills:
        if skill not in text:
            missing.append(skill)

    if not missing:
        result_label.config(text=f"✅ Approved for {company}", fg="green")
    else:
        msg = f"❌ Rejected for {company}\nMissing:\n"
        for m in missing:
            msg += f"- {m}\n"
        result_label.config(text=msg, fg="red")
        """


# -------- GUI --------
root = tk.Tk()
root.title("Resume ATS Scanner")
root.geometry("500x400")

file_path = ""

title = tk.Label(root, text="Resume ATS Scanner", font=("Arial", 18, "bold"))
title.pack(pady=20)

upload_btn = tk.Button(root, text="Upload Resume", command=upload_file)
upload_btn.pack(pady=10)

company_var = tk.StringVar()
company_var.set("TCS")

company_menu = tk.OptionMenu(root, company_var, *company_rules.keys())
company_menu.pack(pady=10)

scan_btn = tk.Button(root, text="Scan Resume", command=scan_resume)
scan_btn.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()
