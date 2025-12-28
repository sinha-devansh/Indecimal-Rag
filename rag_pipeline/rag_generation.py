import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b-instruct"


MAX_CHARS_PER_CHUNK = 1200  # hard cap to control latency


def build_rag_prompt(query, retrieved_chunks):
    context_blocks = []

    for i, r in enumerate(retrieved_chunks, 1):
        text = r["chunk"]["text"][:MAX_CHARS_PER_CHUNK]

        context_blocks.append(
            f"""--- Chunk {i} ---\n
{text}"""
        )

    context_text = "\n\n".join(context_blocks)

    return f"""
You are an AI assistant for a construction marketplace.

STRICT RULES (must follow exactly):
- Use ONLY the information explicitly stated in the context.
- Do NOT infer, interpret, generalize, or add missing details.
- If the question asks "how", list the mechanisms explicitly stated in the context without explaining why they work.
- If the answer is NOT explicitly present, reply EXACTLY with:
  "The provided documents do not contain this information."

FORMAT RULES:
- If the answer contains multiple actions or mechanisms:
  - Present them as a concise bullet list.
- Use short, factual statements only.
- Do NOT merge multiple mechanisms into a single sentence.

====================
CONTEXT
====================
{context_text}

====================
QUESTION
====================
{query}

====================
ANSWER
====================
""".strip()


def run_rag(query, retrieved_results, max_chunks=3):
    used = retrieved_results[:max_chunks]
    prompt = build_rag_prompt(query, used)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.0,
                "num_predict": 120,
                "num_ctx": 2048
            }
        },
        timeout=120
    )

    response.raise_for_status()

    answer = ""

    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        if "response" in data:
            answer += data["response"]

    answer = answer.strip()


    if not answer:
        answer = "The provided documents do not contain this information."

    return answer, [r["chunk"] for r in used]
