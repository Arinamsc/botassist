import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from config import BOT_TOKEN, ANTHROPIC_API_KEY
from content import SECTIONS, TEMPLATES, AGENT_PROMPTS

# ──────────────────────────────────────────────
# ВЫЗОВ CLAUDE
# ──────────────────────────────────────────────

async def call_claude(system: str, user_message: str, max_tokens: int = 1500) -> str:
    """Единая функция для вызова Claude API."""
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user_message}],
            }
        )
    data = response.json()
    return data["content"][0]["text"]

# ──────────────────────────────────────────────
# МЕНЮ
# ──────────────────────────────────────────────

MAIN_KEYBOARD = [
    [InlineKeyboardButton("💼 Экономика", callback_data="menu_economy")],
    [InlineKeyboardButton("📚 База знаний", callback_data="menu_knowledge")],
    [InlineKeyboardButton("📄 Шаблоны", callback_data="menu_templates")],
    [InlineKeyboardButton("🎓 Обучающие материалы", callback_data="menu_learning")],
    [InlineKeyboardButton("❓ Помощь", callback_data="menu_help")],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Это AI-офис Штаб ЦД.\n\n"
        "Напиши мне что угодно — отвечу с контекстом студии.\n\n"
        "Или выбери раздел:",
        reply_markup=InlineKeyboardMarkup(MAIN_KEYBOARD)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n\n"
        "/start — главное меню\n"
        "/sales [задача] — пресейл-помощник\n"
        "/tone [текст] — проверка тона\n"
        "/sprint — шаблон плана на спринт\n"
        "/recap — шаблон рекапа встречи\n"
        "/glossary — глоссарий студии\n"
        "/help — список команд\n\n"
        "Или просто напиши вопрос — отвечу."
    )

# ──────────────────────────────────────────────
# AI-КОМАНДЫ
# ──────────────────────────────────────────────

async def tone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка тона сообщения."""
    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text(
            "Напиши текст после команды.\n\nПример:\n/tone ну короче мы решили переделать главную"
        )
        return
    msg = await update.message.reply_text("Проверяю тон...")
    try:
        result = await call_claude(AGENT_PROMPTS["tone"], text)
        await msg.edit_text(result)
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        await msg.edit_text("Что-то пошло не так. Попробуй ещё раз.")


async def sales_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sales-агент: помощь с пресейлом, аргументами, подбором услуг."""
    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text(
            "Опиши задачу клиента — подберу подход, услугу и аргументы.\n\n"
            "Пример:\n/sales Яндекс хотят обновить дизайн-систему, бюджет не называют"
        )
        return
    msg = await update.message.reply_text("Думаю...")
    try:
        result = await call_claude(AGENT_PROMPTS["sales"], text)
        await msg.edit_text(result)
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        await msg.edit_text("Что-то пошло не так. Попробуй ещё раз.")


async def free_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработка свободного текста. Роутинг по агентам:
    - если есть флаг агента в context.user_data — используем его
    - иначе — универсальный помощник с контекстом студии
    """
    text = update.message.text
    active_agent = context.user_data.get("active_agent", "assistant")
    system_prompt = AGENT_PROMPTS.get(active_agent, AGENT_PROMPTS["assistant"])

    msg = await update.message.reply_text("...")
    try:
        result = await call_claude(system_prompt, text)
        await msg.edit_text(result)
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        await msg.edit_text("Что-то пошло не так. Попробуй ещё раз.")

# ──────────────────────────────────────────────
# ШАБЛОННЫЕ КОМАНДЫ
# ──────────────────────────────────────────────

async def sprint_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["sprint"])

async def recap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["recap"])

async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["glossary"])

# ──────────────────────────────────────────────
# ОБРАБОТКА КНОПОК
# ──────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    routing = {
        "menu_economy":   show_economy,
        "menu_knowledge": show_knowledge,
        "menu_templates": show_templates,
        "menu_learning":  show_learning,
        "menu_help":      show_help,
    }
    if data in routing:
        await routing[data](query)
        return

    link_routing = {
        "econ_presale":  ("economy",   "presale"),
        "econ_current":  ("economy",   "current"),
        "econ_freelance":("economy",   "freelance"),
        "econ_debtor":   ("economy",   "debtor"),
        "know_intro":    ("knowledge", "intro"),
        "know_services": ("knowledge", "services"),
        "know_cases":    ("knowledge", "cases"),
        "know_kp":       ("knowledge", "kp"),
        "tmpl_estimate": ("templates", "estimate"),
    }
    if data in link_routing:
        section, key = link_routing[data]
        await send_link(query, section, key)
        return

    tmpl_routing = {
        "tmpl_sprint":   "sprint",
        "tmpl_recap":    "recap",
        "tmpl_contract": "contract",
        "tmpl_annex":    "annex",
        "learn_glossary":"glossary",
    }
    if data in tmpl_routing:
        await send_template(query, tmpl_routing[data])
        return

    if data == "tmpl_briefs":
        await show_briefs(query)
    elif data == "back_main":
        await query.edit_message_text(
            "Выбери раздел:",
            reply_markup=InlineKeyboardMarkup(MAIN_KEYBOARD)
        )
    elif data == "back_templates":
        await show_templates(query)
    elif data == "back_learning":
        await show_learning(query)

# ──────────────────────────────────────────────
# РАЗДЕЛЫ (без изменений логики, рефакторинг)
# ──────────────────────────────────────────────

def make_keyboard(buttons: list, back: str = "back_main") -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(label, callback_data=cb)] for label, cb in buttons]
    rows.append([InlineKeyboardButton("← Назад", callback_data=back)])
    return InlineKeyboardMarkup(rows)

async def show_economy(query):
    kb = make_keyboard([
        ("Экономика пресейлы",          "econ_presale"),
        ("Экономика текущие проекты",   "econ_current"),
        ("Калькулятор фриланса",        "econ_freelance"),
        ("Дебиторка",                   "econ_debtor"),
    ])
    await query.edit_message_text("💼 Экономика\n\nФинансовые инструменты студии:", reply_markup=kb)

async def show_knowledge(query):
    kb = make_keyboard([
        ("Презентация знакомство", "know_intro"),
        ("Услуги",                 "know_services"),
        ("Кейсы",                  "know_cases"),
        ("Библиотека КП",          "know_kp"),
    ])
    await query.edit_message_text("📚 База знаний ЦД\n\nМатериалы студии:", reply_markup=kb)

async def show_templates(query):
    kb = make_keyboard([
        ("План на спринт",   "tmpl_sprint"),
        ("Рекап",            "tmpl_recap"),
        ("Шаблон сметы",     "tmpl_estimate"),
        ("Брифы по услугам", "tmpl_briefs"),
        ("Договор",          "tmpl_contract"),
        ("Приложение",       "tmpl_annex"),
    ])
    await query.edit_message_text("📄 Шаблоны\n\nДокументы и планы:", reply_markup=kb)

async def show_learning(query):
    kb = make_keyboard([("📖 Глоссарий", "learn_glossary")])
    await query.edit_message_text("🎓 Обучающие материалы\n\nРаздел пополняется:", reply_markup=kb)

async def show_help(query):
    keyboard = [[InlineKeyboardButton("← Назад", callback_data="back_main")]]
    await query.edit_message_text(
        "❓ Помощь\n\n"
        "/start — главное меню\n"
        "/sales [задача] — пресейл-помощник\n"
        "/tone [текст] — проверка тона\n"
        "/sprint — шаблон плана на спринт\n"
        "/recap — шаблон рекапа встречи\n"
        "/glossary — глоссарий студии\n"
        "/help — список команд\n\n"
        "По вопросам — обращайся к администратору бота.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_briefs(query):
    keyboard = [[InlineKeyboardButton("← Назад к шаблонам", callback_data="back_templates")]]
    await query.edit_message_text(
        "📄 Брифы по услугам\n\nРаздел в разработке — материалы появятся скоро.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ──────────────────────────────────────────────
# ОТПРАВКА КОНТЕНТА
# ──────────────────────────────────────────────

async def send_link(query, section: str, key: str):
    item = SECTIONS[section][key]
    back_target = f"menu_{section}" if section != "templates" else "back_templates"
    keyboard = [[InlineKeyboardButton("← Назад", callback_data=back_target)]]
    await query.edit_message_text(
        f"{item['title']}\n\n{item['description']}\n\n🔗 {item['url']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_template(query, key: str):
    tmpl = TEMPLATES.get(key)
    back_target = "back_learning" if key == "glossary" else "back_templates"
    keyboard = [[InlineKeyboardButton("← Назад", callback_data=back_target)]]
    if not tmpl:
        await query.edit_message_text(
            "Шаблон в разработке — появится скоро.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    await query.edit_message_text(tmpl, reply_markup=InlineKeyboardMarkup(keyboard))

# ──────────────────────────────────────────────
# ЗАПУСК
# ──────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Шаблонные команды
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("help",     help_command))
    app.add_handler(CommandHandler("sprint",   sprint_command))
    app.add_handler(CommandHandler("recap",    recap_command))
    app.add_handler(CommandHandler("glossary", glossary_command))

    # AI-команды
    app.add_handler(CommandHandler("tone",  tone_command))
    app.add_handler(CommandHandler("sales", sales_command))

    # Кнопки меню
    app.add_handler(CallbackQueryHandler(button_handler))

    # Свободный текст — в конец, чтобы не перехватывал команды
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_message_handler))

    logger.info("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
