DATASET = [
    {
        "id": "inv_01_simple",
        "text": """СЧЁТ № 118 от 15.04.2024
Поставщик: ИП Сидоров А.В.
Заказчик: ООО «Вектор»

1. Тетрадь 48 л., 10 шт. x 35 руб.
2. Ручка шариковая, 20 шт. x 12 руб.
Итого к оплате: 590 руб.""",
        "expected": {
            "invoice_number": "118",
            "date": "2024-04-15",
            "vendor": "ИП Сидоров А.В.",
            "currency": "RUB",
            "items": [
                {"description": "Тетрадь 48 л.", "quantity": 10, "unit_price": 35},
                {"description": "Ручка шариковая", "quantity": 20, "unit_price": 12},
            ],
            "total": 590,
        },
    },
    {
        "id": "inv_02_date_words",
        "text": """Счёт на оплату № 07/24
от 2 января 2024 г.
Продавец: ООО «Северный ветер»

Монитор 24 дюйма, 3 шт. по 11 500 руб.

Итого: 34 500 руб.""",
        "expected": {
            "invoice_number": "07/24",
            "date": "2024-01-02",
            "vendor": "ООО «Северный ветер»",
            "currency": "RUB",
            "items": [
                {"description": "Монитор 24 дюйма", "quantity": 3, "unit_price": 11500},
            ],
            "total": 34500,
        },
    },
    {
        "id": "inv_03_discount",
        "text": """СЧЁТ № 2024-031 от 12.05.2024
Поставщик: ООО «Техносервис»
1. Роутер Wi-Fi, 4 шт. x 2 500 руб. = 10 000 руб.
2. Кабель Ethernet 5 м, 10 шт. x 150 руб. = 1 500 руб.
Сумма: 11 500 руб.
Скидка 10%: -1 150 руб.
К оплате: 10 350 руб.""",
        "expected": {
            "invoice_number": "2024-031",
            "date": "2024-05-12",
            "vendor": "ООО «Техносервис»",
            "currency": "RUB",
            "items": [
                {"description": "Роутер Wi-Fi", "quantity": 4, "unit_price": 2500},
                {"description": "Кабель Ethernet 5 м", "quantity": 10, "unit_price": 150},
            ],
            "total": 10350,
        },
    },
    {
        "id": "inv_04_vat",
        "text": """СЧЁТ № 45 от 01.06.2024
Поставщик: АО «Прогресс»
1. Услуги хостинга, 12 мес. x 1 000 руб. = 12 000 руб.
Итого без НДС: 12 000 руб.
НДС 20%: 2 400 руб.
Всего к оплате с НДС: 14 400 руб.""",
        "expected": {
            "invoice_number": "45",
            "date": "2024-06-01",
            "vendor": "АО «Прогресс»",
            "currency": "RUB",
            "items": [
                {"description": "Услуги хостинга", "quantity": 12, "unit_price": 1000},
            ],
            "total": 14400,
        },
    },
    {
        "id": "inv_05_usd_english",
        "text": """INVOICE No. US-2024-09
Date: March 9, 2024
From: Blue Sky Ltd.
Bill to: Ромашка LLC

Web design, 1 x $1,200.00
Logo design, 2 x $350.00

Total: $1,900.00""",
        "expected": {
            "invoice_number": "US-2024-09",
            "date": "2024-03-09",
            "vendor": "Blue Sky Ltd.",
            "currency": "USD",
            "items": [
                {"description": "Web design", "quantity": 1, "unit_price": 1200},
                {"description": "Logo design", "quantity": 2, "unit_price": 350},
            ],
            "total": 1900,
        },
    },
    {
        "id": "inv_06_decimals",
        "text": """Счёт № 310 от 20.07.2024
Поставщик: ООО «Электрокомплект»
Кабель ВВГ 3x2.5, 12,5 м x 80 руб.
Автомат 16А, 3 шт. x 245,50 руб.
Итого: 1 736,50 руб.""",
        "expected": {
            "invoice_number": "310",
            "date": "2024-07-20",
            "vendor": "ООО «Электрокомплект»",
            "currency": "RUB",
            "items": [
                {"description": "Кабель ВВГ 3x2.5", "quantity": 12.5, "unit_price": 80},
                {"description": "Автомат 16А", "quantity": 3, "unit_price": 245.5},
            ],
            "total": 1736.5,
        },
    },
    {
        "id": "inv_07_letters_in_number",
        "text": """СЧЁТ № СЧ-0042/Б
Дата выставления: 5 ноября 2023
Поставщик: ООО «Лучшие решения»

Стул офисный — 4 шт. — 2 500 руб./шт. — 10 000 руб.
Стол письменный — 1 шт. — 8 900 руб./шт. — 8 900 руб.
Всего: 18 900 руб.""",
        "expected": {
            "invoice_number": "СЧ-0042/Б",
            "date": "2023-11-05",
            "vendor": "ООО «Лучшие решения»",
            "currency": "RUB",
            "items": [
                {"description": "Стул офисный", "quantity": 4, "unit_price": 2500},
                {"description": "Стол письменный", "quantity": 1, "unit_price": 8900},
            ],
            "total": 18900,
        },
    },
    {
        "id": "inv_08_messy_scan",
        "text": """  С Ч Е Т   N 55
  от  07.11.2023 г.

 Пост авщик :   ООО  «Ветер»

 1) Краска белая 10л   2 шт  по 1 800 р
 2) Валик малярный   5шт  по 220 р

   ИТОГО :  4 700 р.""",
        "expected": {
            "invoice_number": "55",
            "date": "2023-11-07",
            "vendor": "ООО «Ветер»",
            "currency": "RUB",
            "items": [
                {"description": "Краска белая 10л", "quantity": 2, "unit_price": 1800},
                {"description": "Валик малярный", "quantity": 5, "unit_price": 220},
            ],
            "total": 4700,
        },
    },
    {
        "id": "inv_09_many_items",
        "text": """СЧЁТ № 900 от 30.08.2024
Поставщик: ООО «Канцмир»
1. Бумага А4, 10 пачек x 420 руб.
2. Папка-скоросшиватель, 50 шт. x 18 руб.
3. Степлер, 2 шт. x 310 руб.
4. Скобы № 24, 5 уп. x 45 руб.
5. Маркер, 12 шт. x 60 руб.
Итого: 6 665 руб.""",
        "expected": {
            "invoice_number": "900",
            "date": "2024-08-30",
            "vendor": "ООО «Канцмир»",
            "currency": "RUB",
            "items": [
                {"description": "Бумага А4", "quantity": 10, "unit_price": 420},
                {"description": "Папка-скоросшиватель", "quantity": 50, "unit_price": 18},
                {"description": "Степлер", "quantity": 2, "unit_price": 310},
                {"description": "Скобы № 24", "quantity": 5, "unit_price": 45},
                {"description": "Маркер", "quantity": 12, "unit_price": 60},
            ],
            "total": 6665,
        },
    },
    {
        "id": "inv_10_vat_included",
        "text": """Счёт № 12-К от 25.09.2024
Поставщик: ИП Козлова Е.Н.
Консультация, 3 ч. x 2 000 руб. = 6 000 руб.
Итого: 6 000 руб.
В том числе НДС 20%: 1 000 руб.""",
        "expected": {
            "invoice_number": "12-К",
            "date": "2024-09-25",
            "vendor": "ИП Козлова Е.Н.",
            "currency": "RUB",
            "items": [
                {"description": "Консультация", "quantity": 3, "unit_price": 2000},
            ],
            "total": 6000,
        },
    },
]