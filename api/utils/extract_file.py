import re


def extract_email_subject_message(content):
    email_pattern = r'Email:\s*(\S+@\S+\.\S+)'
    subject_pattern = r'Assunto:\s*(.*?)(?=\n|Mensagem:)'
    subject_pattern2 = r'Assunt o:\s*(.*?)(?=\n|Mensagem:)'
    message_pattern = r'Mensagem:\s*(.*)'

    email_match = re.search(email_pattern, content)
    subject_match = re.search(subject_pattern, content, re.DOTALL)
    if not subject_match:
        subject_match = re.search(subject_pattern2, content, re.DOTALL)
    message_match = re.search(message_pattern, content, re.DOTALL)

    email = email_match.group(1) if email_match else None
    subject = subject_match.group(1).strip() if subject_match else None
    message = message_match.group(1).strip() if message_match else None

    return email, subject, message