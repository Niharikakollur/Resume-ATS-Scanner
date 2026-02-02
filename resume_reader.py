import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            text += page.extract_text()

    return text


# Test the function
pdf_file = input("Enter path of your resume PDF: ")
resume_text = extract_text_from_pdf(pdf_file)

print("\n----- Extracted Resume Text -----\n")
print(resume_text)

print("\n----- Resume Analysis -----\n")

text = resume_text.lower()

# Checks
if "@" in text:
    print("✅ Email found")
else:
    print("❌ Email missing")

if any(char.isdigit() for char in text):
    print("✅ Phone number found")
else:
    print("❌ Phone number missing")

if "skills" in text:
    print("✅ Skills section found")
else:
    print("❌ Skills section missing")

if "projects" in text:
    print("✅ Projects section found")
else:
    print("❌ Projects section missing")

if "linkedin" in text:
    print("✅ LinkedIn found")
else:
    print("❌ LinkedIn missing")

if "github" in text:
    print("✅ GitHub found")
else:
    print("❌ GitHub missing")
    
    print("\n----- Company Selection -----\n")

company_rules = {
    "TCS": ["python", "sql", "communication"],
    "Infosys": ["java", "dsa", "projects"],
    "Google": ["projects", "github", "dsa", "internship"]
}

company = input("Select company (TCS / Infosys / Google): ")

required_skills = company_rules.get(company, [])
score = 0
missing = []

for skill in required_skills:
    if skill in text:
        score += 1
    else:
        missing.append(skill)

print("\n----- ATS Result -----\n")

if score == len(required_skills):
    print(f"✅ Approved for {company}")
else:
    print(f"❌ Rejected for {company}")
    print("Missing skills:")
    for m in missing:
        print("-", m)


