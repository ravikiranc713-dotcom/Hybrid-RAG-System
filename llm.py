import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(query, context):
    prompt = f"""
You must answer ONLY from the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        model = "phi"
        
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 1024,
                "num_predict": 120
            }
        })

        return response.json()["response"]

    except Exception:
        return "Model failed to generate response"