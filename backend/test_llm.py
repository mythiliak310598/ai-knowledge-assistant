from app.services.llm_service import generate_answer


prompt = """
    Explain node js in two sentences.
"""

answer = generate_answer(prompt)

print(answer)