import os
from dotenv import load_dotenv
from openai import OpenAI
from schema import Invoice

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Фиксируем конкретную модель, чтобы замеры были сравнимы
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
# Меняйте при каждой правке промпта: кэш замеров привязан к версии
PROMPT_VERSION = "v1"


def clean_json(raw: str) -> str:
    """Вырезает JSON из ответа: модели любят добавлять лишний текст вокруг."""
    start, end = raw.find("{"), raw.rfind("}")
    return raw[start:end + 1]


def ask_model(text: str, model: str = MODEL) -> tuple[str, str]:
    """Один запрос к модели. Возвращает (сырой ответ, имя ответившей модели)."""
    schema = Invoice.model_json_schema()
    prompt = (
        "Извлеки данные из счёта и верни ТОЛЬКО JSON, без пояснений и без markdown.\n"
        f"Схема JSON: {schema}\n\n"
        f"Счёт:\n{text}"
    )
    reply = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return reply.choices[0].message.content or "", reply.model


def parse_invoice(raw: str) -> Invoice:
    """Превращает сырой ответ в проверенный объект Invoice (или бросает ошибку)."""
    return Invoice.model_validate_json(clean_json(raw))


def extract(text: str, model: str = MODEL) -> Invoice:
    raw, answered_by = ask_model(text, model)
    print("Ответила модель:", answered_by)
    return parse_invoice(raw)


if __name__ == "__main__":
    SAMPLE = """СЧЁТ № 2024-117 от 3 марта 2024
Поставщик: ООО «Ромашка»
1. Бумага А4, 5 пачек x 450 руб.
2. Картридж HP, 2 шт x 3200 руб.
Итого: 8650 руб."""
    print(extract(SAMPLE).model_dump_json(indent=2, ensure_ascii=False))