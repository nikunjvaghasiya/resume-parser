import json
from app.services.llm_service import parse_resume_with_openai, parse_resume_with_ollama

sample_text = """
John Doe
Software Engineer
Email: john@example.com
Phone: +1 555 123 4567
Skills: Python, AWS, FastAPI
"""

# print("Sending test prompt...")

# try:
#     result = parse_resume_with_openai(sample_text)
#     print("\n--- RESULT ---")
#     print(json.dumps(result, indent=2))
# except Exception as e:
#     print("\n--- ERROR ---")
#     print(str(e))

result = parse_resume_with_ollama(sample_text)
print(json.dumps(result, indent=2))
