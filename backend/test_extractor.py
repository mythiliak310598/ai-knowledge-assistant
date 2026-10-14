from app.utils.text_extractor import extract_text


file_path = 'uploads/03_Leave_Attendance_and_Benefits_Policy.docx'
text = extract_text(file_path)
print(text)