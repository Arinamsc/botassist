# Бот базы знаний студии ЦД

## Первый запуск

1. Создай виртуальное окружение:
```
python3.11 -m venv ~/cd_bot_env
```

2. Активируй:
```
source ~/cd_bot_env/bin/activate
```

3. Установи зависимости:
```
pip install python-telegram-bot==21.3
```

4. Вставь токен в config.py:
```python
BOT_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
```

5. Запусти:
```
python bot.py
```

## Каждый следующий запуск

```
source ~/cd_bot_env/bin/activate
cd ~/Downloads/cd_bot
python bot.py
```

## Команды бота

/start — главное меню
/sprint — шаблон плана на спринт
/recap — шаблон рекапа встречи
/glossary — глоссарий студии
/help — список команд

## Добавление контента

Все тексты и ссылки хранятся в content.py.

Чтобы добавить шаблон — найди нужный ключ в TEMPLATES и замени None на текст:
```python
"contract": """Текст договора здесь""",
```

## Структура файлов

```
cd_bot/
├── bot.py           — логика бота, меню, кнопки
├── content.py       — все ссылки и тексты шаблонов
├── config.py        — токен
├── requirements.txt
└── README.md
```
