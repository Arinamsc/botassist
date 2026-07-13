# -*- coding: utf-8 -*-
"""
Контент бота базы знаний студии ЦД.

Структура data-driven: bot.py строит меню автоматически из SECTIONS.
Чтобы добавить раздел или пункт — правь ТОЛЬКО этот файл, трогать bot.py не нужно.

Типы пунктов:
  ссылка   → {"key", "title", "description", "url"}
  шаблон   → {"key", "title", "template": "<ключ из TEMPLATES>"}   # можно доп. "url"
  заглушка → {"key", "title", "status": "wip"}                      # материал в процессе сбора
"""

# ──────────────────────────────────────────────
# РАЗДЕЛЫ (9 разделов, порядок = порядок в меню)
# ──────────────────────────────────────────────

SECTIONS = {

    "bizdev": {
        "title": "BizDev",
        "emoji": "📈",
        "items": [
            {
                "key": "market",
                "title": "Захват рынка",
                "description": "Таблица по захвату рынка.",
                "url": "https://docs.google.com/spreadsheets/d/1MKQ_c2JrPgHRw3ot36EGj_XJM9uj_5JrblYkmbGmPk8/edit?gid=63307687#gid=63307687",
            },
        ],
    },

    "sales": {
        "title": "Sales PG",
        "emoji": "🤝",
        "items": [
            {
                "key": "process",
                "title": "Сейлз-процесс",
                "description": "Доска сейлз-процесса студии.",
                "url": "https://www.figma.com/board/9SoaOjBrvr7tGv9aNE5zVk/%D0%A1%D0%B5%D0%B9%D0%BB%D0%B7?node-id=759-1879&t=zqtLtpvTV7fSOI4f-1",
            },
            {
                "key": "presale",
                "title": "Оценки: пресейлы",
                "description": "Таблица для расчёта экономики на этапе пресейла.",
                "url": "https://docs.google.com/spreadsheets/d/1DeCajMQYGUIhe2B3-h2yGIkIagoPeQrxMtWkhXCByHE/edit?gid=0#gid=0",
            },
            {
                "key": "freelance_calc",
                "title": "Оценки: калькулятор фрилов",
                "description": "Калькулятор ставок и дохода фрилансера.",
                "url": "https://docs.google.com/spreadsheets/d/1BzqNVRx4hteidVhDqpN6-QfyHNc-5JTPbD05tSazS9U/edit?gid=0#gid=0",
            },
            {
                "key": "estimate",
                "title": "Шаблон клиентских смет",
                "description": "Смета с разбивкой по ролям, часам и спринтам.",
                "url": "https://docs.google.com/spreadsheets/d/1shkbX0jWsoCiQRdResR0PUIeurYOBAG1KUyd01gE270/edit?hl=ru&gid=0#gid=0",
            },
            {
                "key": "strategy",
                "title": "Стратегия пресейла",
                "description": "Figma-шаблон стратегии пресейла.",
                "url": "https://www.figma.com/design/iGsYp20zar0kQBbyH3haic/%D0%9F%D1%80%D0%B5%D1%81%D0%B5%D0%B9%D0%BB-%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD?node-id=212-145&t=FayIM25ScTMTTdx6-1",
            },
            {
                "key": "approach",
                "title": "Подход к пресейлу",
                "description": "Презентация подхода к пресейлу.",
                "url": "https://www.figma.com/board/9SoaOjBrvr7tGv9aNE5zVk/%D0%A1%D0%B5%D0%B9%D0%BB%D0%B7?node-id=1209-2594&t=zqtLtpvTV7fSOI4f-1",
            },
            {
                "key": "intro_deck",
                "title": "Презентация-знакомство",
                "description": "Презентация студии для первого знакомства с клиентом.",
                "url": "https://www.figma.com/proto/PXDtIQuRrjTHie94Nk55gI/%D0%9F%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F-%D0%B7%D0%BD%D0%B0%D0%BA%D0%BE%D0%BC%D1%81%D1%82%D0%B2%D0%BE?node-id=2842-4309&node-type=frame&viewport=948%2C91%2C0.13&t=QhJBZO2IhxN156Tb-1&scaling=contain&content-scaling=fixed&starting-point-node-id=2842%3A4309&page-id=2764%3A3629",
            },
            {
                "key": "amocrm",
                "title": "amoCRM",
                "description": "Воронка лидов в amoCRM.",
                "url": "https://anpamopragmaticadesign.amocrm.ru/leads/pipeline/8556902/?skip_filter=Y",
            },
            {
                "key": "amocrm_funnel",
                "title": "Описанная воронка amoCRM",
                "description": "Схема воронки amoCRM в FigJam.",
                "url": "https://www.figma.com/board/9SoaOjBrvr7tGv9aNE5zVk/%D0%A1%D0%B5%D0%B9%D0%BB%D0%B7?node-id=640-1770&t=zqtLtpvTV7fSOI4f-1",
            },
            {
                "key": "amocrm_guide",
                "title": "Памятка по amoCRM",
                "description": "Памятка по работе с amoCRM.",
                "url": "https://buildin.ai/d4d0859d-312a-47ad-a7cc-803491028b50",
            },
        ],
    },

    "cd": {
        "title": "ЦД",
        "emoji": "🏢",
        "items": [
            {
                "key": "cases",
                "title": "Библиотека кейсов",
                "description": "Портфолио выполненных проектов.",
                "url": "https://www.figma.com/design/SnmhVKp3AFHtN9nB9Ufuk6/%D0%9A%D0%B5%D0%B9%D1%81%D1%8B?node-id=0-1&t=NX3GemH2It4neA7W-1",
            },
            {
                "key": "kp",
                "title": "Библиотека КП",
                "description": "Библиотека коммерческих предложений студии.",
                "url": "https://www.figma.com/design/80S0828fD06Mh3dwD45lHT/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0-%D0%9A%D0%9F?node-id=0-1&t=r9Y2VoHr8xHWx3XJ-1",
            },
            {
                "key": "hq",
                "title": "Штаб ЦД",
                "description": "Главный штаб студии в Figma.",
                "url": "https://www.figma.com/design/3gC4bTtzxP4Q8LoqT3kMEQ/%D0%A8%D1%82%D0%B0%D0%B1?node-id=570-5019&t=3CNwCpNZ0Y4h7TSQ-1",
            },
        ],
    },

    "finance": {
        "title": "Финансы",
        "emoji": "💰",
        "items": [
            {
                "key": "debtor",
                "title": "Дебиторка",
                "description": "Контроль дебиторской задолженности.",
                "url": "https://docs.google.com/spreadsheets/d/1pDXJgn2kFMPmkjqdPBbpyi3iu02FNZfwm6ZR1ds_gDQ/edit?gid=585126509#gid=585126509",
            },
            {
                "key": "economics",
                "title": "Экономика текущих проектов",
                "description": "Отслеживание экономики по текущим проектам.",
                "url": "https://docs.google.com/spreadsheets/d/1yifwXvt4QGXGR0wG7myKU_aP0C9e5QNa_iFiwopaSt8/edit?gid=1031234586#gid=1031234586",
            },
            {
                "key": "pricing",
                "title": "Вилки по услугам",
                "description": "Вилки по стоимости услуг студии.",
                "url": "https://docs.google.com/spreadsheets/d/16UizMsUfcA-eZJSyBD2q1LRpnrMd8dB6AyjjMQ4IHIE/edit?usp=sharing",
            },
            {
                "key": "freelance_plan",
                "title": "План по фрилансерам",
                "description": "План по фрилансерам.",
                "url": "https://docs.google.com/spreadsheets/d/15J1MvvyAUVf67mAlDJuPgznvcPFk56ZQ1WJP5kM2v2U/edit?gid=1086776065#gid=1086776065",
            },
        ],
    },

    "resources": {
        "title": "Ресурсы",
        "emoji": "🧰",
        "items": [
            {
                "key": "guru",
                "title": "Гуру (Resource Guru)",
                "description": "Дашборд ресурсного планирования.",
                "url": "https://app.resourceguruapp.com/hi/pragmatica/dashboard",
            },
            {
                "key": "guru_guide",
                "title": "Памятка по гуру",
                "description": "Памятка по работе с Resource Guru.",
                "url": "https://www.buildin.ai/share/10793609-a24e-464f-b4f1-626d6c33dc7a?code=3NWJRJ",
            },
            {
                "key": "freelance_guide",
                "title": "Памятка по работе с фрилами",
                "description": "Памятка по работе с фрилансерами.",
                "url": "https://buildin.ai/share/45b23153-642c-4fcd-8aa4-2f68db1268b0?code=7Z1G72",
            },
        ],
    },

    "documents": {
        "title": "Документы",
        "emoji": "📄",
        "items": [
            {"key": "docs_yandex", "title": "Памятка по документам (Яндекс)", "status": "wip"},
            {"key": "docs_vk", "title": "Памятка по документам (ВК)", "status": "wip"},
            {"key": "docs_templates", "title": "Договор, приложения, акт, НДА, карточки ИП/ООО", "status": "wip"},
        ],
    },

    "other": {
        "title": "Другое",
        "emoji": "⚙️",
        "items": [
            # Доступы — потенциально чувствительное. НЕ храним логины/пароли текстом.
            # Когда появится ссылка на защищённое хранилище — заменить status на url.
            {"key": "access", "title": "Доступы к инструментам", "status": "wip"},
        ],
    },

    "project": {
        "title": "Проектное",
        "emoji": "📋",
        "items": [
            {
                "key": "project_card",
                "title": "Карточка проекта",
                "description": "Шаблон карточки проекта в BuildIn.",
                "url": "https://www.buildin.ai/404b6210-5f3a-4af6-98ab-675196312c02",
            },
            {"key": "recap", "title": "Шаблон рекапа", "template": "recap"},
            {"key": "sprint", "title": "Шаблон плана на спринт", "template": "sprint"},
            {
                "key": "glossary",
                "title": "Глоссарий",
                "template": "glossary",
                "url": "https://buildin.ai/ca89ccc1-1429-4401-8d75-915fb1184f78",
            },
        ],
    },

    "marketing": {
        "title": "Маркетинг",
        "emoji": "📣",
        "items": [
            {"key": "site_main", "title": "pragmatica.design — Main", "description": "Главный сайт студии.", "url": "https://www.pragmatica.design/"},
            {"key": "site_outstaff", "title": "pragmatica.design — Outstaff", "description": "Лендинг outstaff.", "url": "https://www.pragmatica.design/outstaff"},
            {"key": "site_support", "title": "pragmatica.design — Design Support", "description": "Лендинг design support.", "url": "https://www.pragmatica.design/design-support"},
            {"key": "site_special", "title": "pragmatica.design — Special Projects", "description": "Лендинг спецпроектов.", "url": "https://www.pragmatica.design/supermegagigaprojects"},
            {"key": "site_rnd", "title": "pragmatica.design — R&D", "description": "Лендинг R&D.", "url": "https://www.pragmatica.design/rnd"},
            {"key": "site_lookandfeel", "title": "collectiveee.com — Look and Feel", "description": "Лендинг Look and Feel.", "url": "https://www.collectiveee.com/lookandfeel"},
            {"key": "site_bigpractice", "title": "collectiveee.com — Большая практика", "description": "Лендинг «Большая практика».", "url": "https://www.collectiveee.com/big-practice"},
        ],
    },

}

# ──────────────────────────────────────────────
# ШАБЛОНЫ (текст прямо в чат)
# ──────────────────────────────────────────────

SPRINT_TEMPLATE = """⚡️ Планы на спринт [№]

🎯Цель: [одно предложение – что главное на этой неделе]

📌 Что нужно от вас для старта (если ничего не ждем, то убираем этот пункт)
→ пункт 1
→ пункт 2

📅 Задачи:
→ описание задачи
→ описание задачи
→ описание задачи
→ описание задачи
→ описание задачи

если в рамках спринта есть встречи, то их можно дополнительно выделять (например, через 🗣) и обязательно фиксировать время и кратко адженду.

💡 Выходные материалы спринта [артефакты, которые передаем в рамках спринта, например, паспорт проекта или доски с коцепциями и т.д.]
→ пункт 1 
→ пункт 1
→ пункт 1

Вопросы и пожелания — пишите в любое время)"""

RECAP_TEMPLATE = """📝 Рекап встречи [Дата]
🎥 Запись встречи: [ссылка]

💬 Основные комментарии

[Тема 1, например: страница, сценарий, участок концепции]
→ [комментарий]
→ [комментарий]

[Тема 2, например: цвета]
→ [комментарий]
→ [комментарий]

[Тема 3]
→ [комментарий]

✅ Следующие шаги

→ [задача]
→ [задача]

Остаёмся на связи, спасибо)"""

GLOSSARY_TEXT = """📖 Глоссарий студии ЦД

─────────────────────
ПРОЕКТНЫЙ ПРОЦЕСС

Пресейл — этап до старта проекта: оценка задачи, подготовка сметы и КП, согласование условий сотрудничества.

Бриф — документ с описанием задачи от клиента. Заполняется до старта проекта и фиксирует цели, аудиторию, ограничения и ожидания по результату.

Спринт — фиксированный рабочий период (обычно 1–2 недели), в рамках которого команда выполняет согласованный объём задач и передаёт артефакты.

Паспорт проекта — внутренний документ с описанием задачи, скоупом, командой, требованиями и ожиданиями по дизайну. Упаковывается в первый спринт.

Рекап — краткое резюме встречи или звонка: основные решения, комментарии и следующие шаги. Отправляется клиенту после встречи.

Скоуп — объём работ по проекту. Фиксируется в договоре и паспорте проекта.

Буфер — резерв часов на непредвиденные правки и доработки. Закладывается в смету отдельной строкой.

─────────────────────
ДОКУМЕНТЫ

Смета — расчёт стоимости проекта с разбивкой по ролям, часам и спринтам. Срок действия — 30 дней с даты отправки.

КП (коммерческое предложение) — документ для клиента с описанием услуги, подхода, команды и стоимости.

Rate card — фиксированные ставки для конкретного клиента, закреплённые в договоре. Могут отличаться от базовых ставок студии.

─────────────────────
ФОРМАТЫ РАБОТЫ

TM (Time & Material) — модель оплаты по фактически затраченным часам и ставкам.

Retainer — модель с фиксированным объёмом часов в месяц и постоянной командой. Подходит для долгосрочного сотрудничества.

─────────────────────
АРТЕФАКТЫ

Бенчмаркинг — визуальный анализ конкурентов и рынка. Один из выходных материалов первого спринта.

Референсы — примеры визуальных решений, которые задают направление для дизайна.

One pager — компактная презентация на 1–3 слайда для быстрого согласования концепции, палитры или решения.

Флоу согласований — договорённость с клиентом о том, кто принимает решения, сколько раундов правок включено и в каком формате фиксируются решения.

─────────────────────
УСЛУГИ СТУДИИ

UX-аудит — экспертная диагностика продукта: анализ пользовательских сценариев, выявление барьеров, юзабилити-проблем и точек потери конверсии. Чек: 300К–800К.

Visual R&D — оценка визуального стиля продукта: насколько он единый, современный и подходит бренду. Результат — отчёт, мудборды, референсы и прототип нового стиля. Чек: 300К–1.5М.

UX Update — коррекция или обновление продуктовой и/или UX-логики при сохранении существующего стиля. Чек: 1–3М.

UI Update — создание или обновление визуального слоя продукта при сохранении продуктовой логики. Новый дизайн-язык, UI kit, иконография. Чек: 1–3М.

Product Design — проектирование цифрового продукта от исследований до финальных макетов: UX, UI, дизайн-система. Чек: 2–5М.

Web Design — проектирование и дизайн продуктовых сайтов: корпоративные сайты, лендинги, сервисные порталы. Чек: 1–3М.

Product Design + App Dev — полный цикл от проектирования до работающего продукта. Чек: 5–30М.

Web Design + Web Dev — проектирование, дизайн и разработка сайтов и веб-сервисов. Чек: 3–15М.

Продуктовая поддержка — выделенный дизайнер или команда на постоянной основе: итеративные улучшения, новые фичи, A/B-тесты, поддержка дизайн-системы. Чек: 300К–1М/мес."""

TEMPLATES = {
    "sprint": SPRINT_TEMPLATE,
    "recap": RECAP_TEMPLATE,
    "glossary": GLOSSARY_TEXT,
}
