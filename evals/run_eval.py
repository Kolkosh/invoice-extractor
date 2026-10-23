import json
import re
import sys
from pathlib import Path

# добавляем папку src в пути поиска, чтобы найти extract.py и schema.py
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from extract import MODEL, PROMPT_VERSION, ask_model, parse_invoice
from schema import Invoice
from dataset import DATASET

CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

FIELDS = ["invoice_number", "date", "vendor", "currency", "items", "total"]
LABELS = {
    "invoice_number": "номер", "date": "дата", "vendor": "поставщ.",
    "currency": "валюта", "items": "позиции", "total": "итого",
}

# латинские буквы, похожие на русские: a -> а, e -> е, k -> к и так далее
LOOKALIKES = str.maketrans("abcehkmoptxy", "авсенкмортху")


def norm_id(s: str) -> str:
    """Для номеров: без регистра и пробелов, латиница-двойники -> кириллица."""
    return re.sub(r"\s+", "", s.lower()).translate(LOOKALIKES)


def norm_text(s: str) -> str:
    """Для названий: ещё и без кавычек и знаков препинания."""
    s = s.lower().replace("ё", "е")
    return re.sub(r"[^\w]|_", "", s).translate(LOOKALIKES)


def close(a: float, b: float) -> bool:
    return abs(a - b) < 0.01


def same_items(exp_items, got_items) -> bool:
    if len(exp_items) != len(got_items):
        return False
    for e, g in zip(exp_items, got_items):
        de, dg = norm_text(e.description), norm_text(g.description)
        if not (de in dg or dg in de):
            return False
        if not close(e.quantity, g.quantity) or not close(e.unit_price, g.unit_price):
            return False
    return True


def compare(exp: Invoice, got: Invoice) -> dict:
    return {
        "invoice_number": norm_id(exp.invoice_number) == norm_id(got.invoice_number),
        "date": exp.date.strip() == got.date.strip(),
        "vendor": norm_text(exp.vendor) == norm_text(got.vendor),
        "currency": exp.currency.strip().upper() == got.currency.strip().upper(),
        "items": same_items(exp.items, got.items),
        "total": close(exp.total, got.total),
    }


def show(value) -> str:
    if isinstance(value, list):
        return "; ".join(f"{i.description} x{i.quantity:g} по {i.unit_price:g}" for i in value)
    return str(value)


def get_raw(case_id: str, text: str):
    """Берёт ответ из кэша, а если его нет, спрашивает модель и сохраняет."""
    safe_model = re.sub(r"[^\w.-]", "_", MODEL)
    path = CACHE_DIR / f"{safe_model}__{PROMPT_VERSION}__{case_id}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["raw"], True
    raw, answered_by = ask_model(text, MODEL)
    if raw.strip():  # пустой ответ не кэшируем
        data = {"raw": raw, "answered_by": answered_by}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return raw, False


def main():
    print(f"Модель: {MODEL} | версия промпта: {PROMPT_VERSION}\n")
    rows = []  # (id документа, результаты проверок или None, подробности ошибок)
    stopped = False

    for case in DATASET:
        try:
            raw, cached = get_raw(case["id"], case["text"])
        except Exception as e:
            print(f"Запрос для {case['id']} не удался ({type(e).__name__}). Останавливаюсь.")
            print("Уже полученные ответы сохранены: запустите позже, продолжит с этого места.\n")
            stopped = True
            break
        print(f"[{'кэш' if cached else 'запрос'}] {case['id']}")

        exp = Invoice(**case["expected"])
        try:
            got = parse_invoice(raw)
        except Exception:
            preview = raw[:80].replace("\n", " ")
            rows.append((case["id"], None, {"формат": ("JSON по схеме", preview)}))
            continue

        checks = compare(exp, got)
        details = {
            f: (show(getattr(exp, f)), show(getattr(got, f)))
            for f, ok in checks.items() if not ok
        }
        rows.append((case["id"], checks, details))

    if not rows:
        return

    print("\n" + f"{'документ':<28}" + "".join(f"{LABELS[f]:<10}" for f in FIELDS))
    for case_id, checks, _ in rows:
        if checks is None:
            line = "ОШИБКА ФОРМАТА: ответ не разобрался как JSON по схеме"
        else:
            line = "".join(f"{('ok' if checks[f] else '--'):<10}" for f in FIELDS)
        print(f"{case_id:<28}{line}")

    n = len(rows)
    print("\nТочность по полям:")
    for f in FIELDS:
        right = sum(1 for _, c, _ in rows if c and c[f])
        print(f"  {LABELS[f]:<10}{right}/{n}  {right / n:.0%}")
    perfect = sum(1 for _, c, _ in rows if c and all(c.values()))
    print(f"\nДокументов без единой ошибки: {perfect} из {n} ({perfect / n:.0%})")
    if stopped:
        print(f"Проверено {n} из {len(DATASET)} документов (остальные ещё не получены).")

    if any(details for _, _, details in rows):
        print("\nГде ошиблись:")
        for case_id, _, details in rows:
            for f, (e, g) in details.items():
                print(f"  {case_id} / {f}\n     ожидали:  {e}\n     получили: {g}")


if __name__ == "__main__":
    main()