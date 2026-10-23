import os
from dotenv import load_dotenv
from openai import OpenAI
from schema import Invoice

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "openrouter/free"


def clean_json(raw: str) -> str:
    """Вырезает JSON из ответа: модели любят добавлять лишний текст вокруг."""
    start, end = raw.find("{"), raw.rfind("}")
    return raw[start:end + 1]


def extract(text: str) -> Invoice:
    schema = Invoice.model_json_schema()
    prompt = (
        "Извлеки данные из счёта и верни ТОЛЬКО JSON, без пояснений и без markdown.\n"
        f"Схема JSON: {schema}\n\n"
        f"Счёт:\n{text}"
    )
    reply = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    print("Ответила модель:", reply.model)
    raw = reply.choices[0].message.content or ""
    return Invoice.model_validate_json(clean_json(raw))


if __name__ == "__main__":
    SAMPLE = """СЧЁТ № 2024-117 от 3 марта 2024
Поставщик: ООО «Ромашка»
1. Бумага А4, 5 пачек x 450 руб.
2. Картридж HP, 2 шт x 3200 руб.
Итого: 8650 руб."""
    print(extract(SAMPLE).model_dump_json(indent=2, ensure_ascii=False))