import logging

import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import BOT_TOKEN, ANTHROPIC_API_KEY
from content import SECTIONS, TEMPLATES

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# ТОН ОФ ВОЙС СТУДИИ
# ──────────────────────────────────────────────

TOV_PROMPT = """Ты редактор дизайн-студии Pragmatica. Твоя задача — привести текст в соответствие с тоном студии.

Правила тона:
- Обращение на ты
- Без формализации и бюрократического языка
- Без жаргонов
- Чёткая структура — короткие блоки, не простыня текста
- Корректные дизайн-термины
- Никаких слов-паразитов: "безусловно", "важно отметить", "в целом", "стоит отметить", "на самом деле", "действительно"
- Никаких вводных конструкций ради объёма
- Текст звучит как живой человек, не как шаблон

Получи текст от пользователя и верни:
1. Исправленную версию
2. Коротко — что изменил и почему

Не добавляй лишних слов. Будь конкретным."""

HELP_TEXT = (
    "Доступные команды:\n\n"
    "/start — главное меню\n"
    "/sprint — шаблон плана на спринт\n"
    "/recap — шаблон рекапа встречи\n"
    "/glossary — глоссарий студии\n"
    "/tone [текст] — проверка тона сообщения\n"
    "/help — список команд\n\n"
    "Или просто нажми кнопку в меню."
)

# ──────────────────────────────────────────────
# КЛАВИАТУРЫ (строятся автоматически из SECTIONS)
# ──────────────────────────────────────────────

def main_menu_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(f"{s['emoji']} {s['title']}", callback_data=f"sec:{key}")]
        for key, s in SECTIONS.items()
    ]
    rows.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    return InlineKeyboardMarkup(rows)


def section_keyboard(section_key: str) -> InlineKeyboardMarkup:
    section = SECTIONS[section_key]
    rows = [
        [InlineKeyboardButton(item["title"], callback_data=f"item:{section_key}:{item['key']}")]
        for item in section["items"]
    ]
    rows.append([InlineKeyboardButton("← Назад", callback_data="home")])
    return InlineKeyboardMarkup(rows)


def back_to_section_keyboard(section_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("← Назад", callback_data=f"sec:{section_key}")]])


def back_home_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("← Назад", callback_data="home")]])


def find_item(section_key: str, item_key: str):
    for item in SECTIONS.get(section_key, {}).get("items", []):
        if item["key"] == item_key:
            return item
    return None

# ──────────────────────────────────────────────
# КОМАНДЫ
# ──────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Это база знаний студии Pragmatica.\n\nВыбери раздел:",
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def sprint_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["sprint"])


async def recap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["recap"])


async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["glossary"])

# ──────────────────────────────────────────────
# ПРОВЕРКА ТОНА (Claude API)
# ──────────────────────────────────────────────

async def tone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else ""

    if not text:
        await update.message.reply_text(
            "Напиши текст после команды.\n\nПример:\n/tone ну короче мы решили переделать главную"
        )
        return

    await update.message.reply_text("Проверяю тон...")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1000,
                    "system": TOV_PROMPT,
                    "messages": [{"role": "user", "content": text}],
                },
            )
        data = response.json()
        result = data["content"][0]["text"]
        await update.message.reply_text(result)

    except Exception as e:
        logger.error(f"Claude API error: {e}")
        await update.message.reply_text("Что-то пошло не так. Попробуй ещё раз.")

# ──────────────────────────────────────────────
# ОБРАБОТКА КНОПОК
# ──────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Главное меню
    if data == "home":
        await query.edit_message_text("Выбери раздел:", reply_markup=main_menu_keyboard())
        return

    # Помощь
    if data == "help":
        await query.edit_message_text(HELP_TEXT, reply_markup=back_home_keyboard())
        return

    # Открыть раздел
    if data.startswith("sec:"):
        section_key = data.split(":", 1)[1]
        section = SECTIONS.get(section_key)
        if not section:
            await query.edit_message_text("Раздел не найден.", reply_markup=main_menu_keyboard())
            return
        await query.edit_message_text(
            f"{section['emoji']} {section['title']}\n\nВыбери материал:",
            reply_markup=section_keyboard(section_key),
        )
        return

    # Открыть пункт раздела
    if data.startswith("item:"):
        _, section_key, item_key = data.split(":", 2)
        await send_item(query, section_key, item_key)
        return

# ──────────────────────────────────────────────
# ОТПРАВКА ПУНКТА
# ──────────────────────────────────────────────

async def send_item(query, section_key: str, item_key: str):
    item = find_item(section_key, item_key)
    keyboard = back_to_section_keyboard(section_key)

    if item is None:
        await query.edit_message_text("Не нашёл этот пункт.", reply_markup=keyboard)
        return

    # 1. Шаблон (текст в чат), опционально со ссылкой на полную версию
    if item.get("template"):
        text = TEMPLATES.get(item["template"]) or "Шаблон в разработке — появится скоро."
        if item.get("url"):
            text += f"\n\n🔗 Полная версия: {item['url']}"
        await query.edit_message_text(text, reply_markup=keyboard, disable_web_page_preview=True)
        return

    # 2. Заглушка — материал в процессе сбора
    if item.get("status") == "wip":
        await query.edit_message_text(
            f"{item['title']}\n\nВ процессе — материал скоро появится.",
            reply_markup=keyboard,
        )
        return

    # 3. Ссылка
    description = item.get("description", "")
    await query.edit_message_text(
        f"{item['title']}\n\n{description}\n\n🔗 {item['url']}",
        reply_markup=keyboard,
    )

# ──────────────────────────────────────────────
# ЗАПУСК
# ──────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sprint", sprint_command))
    app.add_handler(CommandHandler("recap", recap_command))
    app.add_handler(CommandHandler("glossary", glossary_command))
    app.add_handler(CommandHandler("tone", tone_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
