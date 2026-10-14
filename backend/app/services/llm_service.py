import ollama
from fastapi import HTTPException

def generate_answer(prompt: str) -> str:
    # Send the prompt to the local Llama model.
    try:
        response = ollama.chat(
            model = 'llama3.2:3b',
            messages= [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"]

        return answer

    except ollama.ResponseError:
        raise HTTPException(
            status_code=503,
            detail="LLM service is currently unavailable"
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the LLM service"
        )
    