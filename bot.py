import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from config import BOT_TOKEN, ANTHROPIC_API_KEY
from content import SECTIONS, TEMPLATES

# ──────────────────────────────────────────────
# ТОН ОФ ВОЙС СТУДИИ
# ──────────────────────────────────────────────

TOV_PROMPT = """Ты редактор дизайн-студии ЦД. Твоя задача — привести текст в соответствие с тоном студии.

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

# ──────────────────────────────────────────────
# МЕНЮ
# ──────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💼 Экономика", callback_data="menu_economy")],
        [InlineKeyboardButton("📚 База знаний", callback_data="menu_knowledge")],
        [InlineKeyboardButton("📄 Шаблоны", callback_data="menu_templates")],
        [InlineKeyboardButton("🎓 Обучающие материалы", callback_data="menu_learning")],
        [InlineKeyboardButton("❓ Помощь", callback_data="menu_help")],
    ]
    await update.message.reply_text(
        "Привет! Это база знаний студии ЦД.\n\nВыбери раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n\n"
        "/start — главное меню\n"
        "/sprint — шаблон плана на спринт\n"
        "/recap — шаблон рекапа встречи\n"
        "/glossary — глоссарий студии\n"
        "/tone [текст] — проверка тона сообщения\n"
        "/help — список команд\n\n"
        "Или просто нажми кнопку в меню."
    )

async def sprint_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["sprint"])

async def recap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["recap"])

async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEMPLATES["glossary"])

# ──────────────────────────────────────────────
# ПРОВЕРКА ТОНА
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
                    "messages": [
                        {"role": "user", "content": text}
                    ],
                }
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

    if data == "menu_economy":
        await show_economy(query)
    elif data == "menu_knowledge":
        await show_knowledge(query)
    elif data == "menu_templates":
        await show_templates(query)
    elif data == "menu_learning":
        await show_learning(query)
    elif data == "menu_help":
        await show_help(query)

    elif data == "econ_presale":
        await send_link(query, "economy", "presale")
    elif data == "econ_current":
        await send_link(query, "economy", "current")
    elif data == "econ_freelance":
        await send_link(query, "economy", "freelance")
    elif data == "econ_debtor":
        await send_link(query, "economy", "debtor")

    elif data == "know_intro":
        await send_link(query, "knowledge", "intro")
    elif data == "know_services":
        await send_link(query, "knowledge", "services")
    elif data == "know_cases":
        await send_link(query, "knowledge", "cases")
    elif data == "know_kp":
        await send_link(query, "knowledge", "kp")

    elif data == "tmpl_sprint":
        await send_template(query, "sprint")
    elif data == "tmpl_recap":
        await send_template(query, "recap")
    elif data == "tmpl_estimate":
        await send_link(query, "templates", "estimate")
    elif data == "tmpl_briefs":
        await show_briefs(query)
    elif data == "tmpl_contract":
        await send_template(query, "contract")
    elif data == "tmpl_annex":
        await send_template(query, "annex")

    elif data == "learn_glossary":
        await send_template(query, "glossary")

    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton("💼 Экономика", callback_data="menu_economy")],
            [InlineKeyboardButton("📚 База знаний", callback_data="menu_knowledge")],
            [InlineKeyboardButton("📄 Шаблоны", callback_data="menu_templates")],
            [InlineKeyboardButton("🎓 Обучающие материалы", callback_data="menu_learning")],
            [InlineKeyboardButton("❓ Помощь", callback_data="menu_help")],
        ]
        await query.edit_message_text(
            "Выбери раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "back_templates":
        await show_templates(query)
    elif data == "back_learning":
        await show_learning(query)

# ──────────────────────────────────────────────
# РАЗДЕЛЫ
# ──────────────────────────────────────────────

async def show_economy(query):
    keyboard = [
        [InlineKeyboardButton("Экономика пресейлы", callback_data="econ_presale")],
        [InlineKeyboardButton("Экономика текущие проекты", callback_data="econ_current")],
        [InlineKeyboardButton("Калькулятор фриланса", callback_data="econ_freelance")],
        [InlineKeyboardButton("Дебиторка", callback_data="econ_debtor")],
        [InlineKeyboardButton("← Назад", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "💼 Экономика\n\nФинансовые инструменты студии:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_knowledge(query):
    keyboard = [
        [InlineKeyboardButton("Презентация знакомство", callback_data="know_intro")],
        [InlineKeyboardButton("Услуги", callback_data="know_services")],
        [InlineKeyboardButton("Кейсы", callback_data="know_cases")],
        [InlineKeyboardButton("Библиотека КП", callback_data="know_kp")],
        [InlineKeyboardButton("← Назад", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "📚 База знаний ЦД\n\nМатериалы студии:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_templates(query):
    keyboard = [
        [InlineKeyboardButton("План на спринт", callback_data="tmpl_sprint")],
        [InlineKeyboardButton("Рекап", callback_data="tmpl_recap")],
        [InlineKeyboardButton("Шаблон сметы", callback_data="tmpl_estimate")],
        [InlineKeyboardButton("Брифы по услугам", callback_data="tmpl_briefs")],
        [InlineKeyboardButton("Договор", callback_data="tmpl_contract")],
        [InlineKeyboardButton("Приложение", callback_data="tmpl_annex")],
        [InlineKeyboardButton("← Назад", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "📄 Шаблоны\n\nДокументы и планы:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_learning(query):
    keyboard = [
        [InlineKeyboardButton("📖 Глоссарий", callback_data="learn_glossary")],
        [InlineKeyboardButton("← Назад", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "🎓 Обучающие материалы\n\nРаздел пополняется:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_help(query):
    keyboard = [[InlineKeyboardButton("← Назад", callback_data="back_main")]]
    await query.edit_message_text(
        "❓ Помощь\n\n"
        "/start — главное меню\n"
        "/sprint — шаблон плана на спринт\n"
        "/recap — шаблон рекапа встречи\n"
        "/glossary — глоссарий студии\n"
        "/tone [текст] — проверка тона сообщения\n"
        "/help — список команд\n\n"
        "По вопросам — обращайся к администратору бота.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_briefs(query):
    keyboard = [
        [InlineKeyboardButton("← Назад к шаблонам", callback_data="back_templates")],
    ]
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

    await query.edit_message_text(
        tmpl,
        reply_markup=InlineKeyboardMarkup(keyboard)
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
