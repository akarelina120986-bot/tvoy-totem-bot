import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

QUESTIONS = [
    (
        "1. Представь: в твоей жизни начинается новый этап.\n\n"
        "Что тебе сейчас нужнее всего?",
        [
            ("А — Внутренняя сила", "А"),
            ("Б — Безопасность", "Б"),
            ("В — Понять путь", "В"),
            ("Г — Свобода", "Г"),
            ("Д — Новые возможности", "Д"),
        ],
    ),
    (
        "2. Что ты делаешь, когда сталкиваешься с серьёзным препятствием?",
        [
            ("А — Иду навстречу", "А"),
            ("Б — Наблюдаю", "Б"),
            ("В — Ищу другой путь", "В"),
            ("Г — Ухожу", "Г"),
            ("Д — Меняюсь", "Д"),
        ],
    ),
    (
        "3. Что ты сейчас хочешь изменить в себе?",
        [
            ("А — Уверенность", "А"),
            ("Б — Чувствовать людей", "Б"),
            ("В — Отпустить прошлое", "В"),
            ("Г — Проявляться ярче", "Г"),
            ("Д — Беречь себя", "Д"),
        ],
    ),
    (
        "4. Какая фраза откликается сильнее?",
        [
            ("А — Знаю, чего стою", "А"),
            ("Б — Чувствую больше", "Б"),
            ("В — Отпустить старое", "В"),
            ("Г — Свои правила", "Г"),
            ("Д — Доверять жизни", "Д"),
        ],
    ),
    (
        "5. Что для тебя сейчас важнее?",
        [
            ("А — Сила", "А"),
            ("Б — Мудрость", "Б"),
            ("В — Свобода", "В"),
            ("Г — Трансформация", "Г"),
            ("Д — Гармония", "Д"),
        ],
    ),
    (
        "6. Представь, что у тебя появилась способность. Что выбираешь?",
        [
            ("А — Видеть скрытое", "А"),
            ("Б — Стать сильнее", "Б"),
            ("В — Чувствовать опасность", "В"),
            ("Г — Адаптироваться", "Г"),
            ("Д — Влиять на пространство", "Д"),
        ],
    ),
    (
        "7. Каким ты хочешь видеть своё ближайшее будущее?",
        [
            ("А — Занять своё место", "А"),
            ("Б — Понять себя", "Б"),
            ("В — Свой путь", "В"),
            ("Г — Полностью измениться", "Г"),
            ("Д — Выйти на новый уровень", "Д"),
        ],
    ),
]

TOTEMS = {
    "А": ("🐆 Пантера", "внутренняя сила, независимость, уверенность и магнетизм"),
    "Б": ("🐻 Медведь", "защита, устойчивость, безопасность и внутренняя опора"),
    "В": ("🐺 Волк", "свобода, верность себе, интуиция и собственный путь"),
    "Г": ("🦊 Лиса", "гибкость, находчивость, адаптация и нестандартные решения"),
    "Д": ("🐦‍⬛ Ворон", "глубина, интуиция, тайна и перемены"),
    "Е": ("🐉 Дракон", "масштаб, сила, трансформация и новый уровень"),
    "Ж": ("🦌 Олень", "мягкость, гармония, чувствительность и бережность"),
    "З": ("🦉 Сова", "мудрость, наблюдательность и проницательность"),
    "И": ("🐍 Змея", "обновление, освобождение от старого и трансформация"),
    "К": ("🐅 Тигр", "смелость, решительность, действие и страсть"),
    "Л": ("🦁 Лев", "лидерство, достоинство, уверенность и проявленность"),
}

SCORING = {
    1: {
        "А": ["А", "К", "Л"],
        "Б": ["Б", "Ж"],
        "В": ["З", "В"],
        "Г": ["В", "Г", "А"],
        "Д": ["Г", "Е", "Д"],
    },
    2: {
        "А": ["К", "Л", "А"],
        "Б": ["З", "Д", "Г"],
        "В": ["Г", "И", "Д"],
        "Г": ["В", "Ж"],
        "Д": ["И", "Е", "Д"],
    },
    3: {
        "А": ["К", "Л", "А"],
        "Б": ["З", "Д", "В"],
        "В": ["И", "Д", "Е"],
        "Г": ["Л", "А", "Е"],
        "Д": ["Ж", "Б", "З"],
    },
    4: {
        "А": ["Л", "А"],
        "Б": ["З", "Д"],
        "В": ["И", "Д", "Е"],
        "Г": ["В", "Г", "А"],
        "Д": ["Ж", "Б"],
    },
    5: {
        "А": ["А", "К", "Л"],
        "Б": ["З", "Д"],
        "В": ["В", "Г"],
        "Г": ["И", "Д", "Е"],
        "Д": ["Ж", "Б"],
    },
    6: {
        "А": ["З", "Д", "И"],
        "Б": ["Б", "А", "К"],
        "В": ["В", "З", "И"],
        "Г": ["Г", "В", "И"],
        "Д": ["Е", "Л", "А"],
    },
    7: {
        "А": ["Л", "А", "Б"],
        "Б": ["З", "Д"],
        "В": ["В", "Г"],
        "Г": ["И", "Е", "Д"],
        "Д": ["Е", "Л", "К"],
    },
}


def keyboard_for_question(number):
    buttons = []

    for text, value in QUESTIONS[number - 1][1]:
        buttons.append([
            InlineKeyboardButton(
                text,
                callback_data=f"q{number}:{value}"
            )
        ])

    return InlineKeyboardMarkup(buttons)


def keyboard_for_totems():
    rows = []

    for key, (name, _) in TOTEMS.items():
        rows.append([
            InlineKeyboardButton(
                name,
                callback_data=f"t:{key}"
            )
        ])

    return InlineKeyboardMarkup(rows)


def calculate_result(answers):
    scores = {key: 0 for key in TOTEMS}

    for question_number in range(1, 8):
        answer = answers.get(question_number)

        if not answer:
            continue

        for totem in SCORING[question_number][answer]:
            scores[totem] += 1

    max_score = max(scores.values())

    leaders = [
        key for key, value in scores.items()
        if value == max_score
    ]

    selected = answers.get(8)

    if selected in leaders:
        return selected, scores

    return leaders[0], scores


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    text = (
        "🐾 КАКОЙ ТОТЕМ ТЕБЕ НУЖЕН СЕЙЧАС?\n\n"
        "Пройди небольшой тест из 8 вопросов и узнай, "
        "какой образ может откликаться тебе именно сейчас.\n\n"
        "Отвечай интуитивно — долго не раздумывай.\n\n"
        "Готова? ✨"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🐾 НАЧАТЬ ТЕСТ",
                callback_data="start_test"
            )
        ]
    ])

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "start_test":
        context.user_data["answers"] = {}
        context.user_data["question"] = 1

        await query.edit_message_text(
            QUESTIONS[0][0],
            reply_markup=keyboard_for_question(1)
        )

        return

    if data.startswith("q"):
        question_number = int(
            data[1:].split(":")[0]
        )

        answer = data.split(":")[1]

        answers = context.user_data.setdefault(
            "answers",
            {}
        )

        answers[question_number] = answer

        if question_number < 7:
            next_question = question_number + 1

            context.user_data["question"] = next_question

            await query.edit_message_text(
                QUESTIONS[next_question - 1][0],
                reply_markup=keyboard_for_question(
                    next_question
                )
            )

            return

        context.user_data["question"] = 8

        await query.edit_message_text(
            "8. И последний вопрос.\n\n"
            "Какой образ сейчас притягивает тебя сильнее всего?\n\n"
            "Не анализируй. Выбери тот, к которому "
            "потянуло первым. 🖤",
            reply_markup=keyboard_for_totems()
        )

        return

    if data.startswith("t:"):
        selected = data.split(":")[1]

        answers = context.user_data.setdefault(
            "answers",
            {}
        )

        answers[8] = selected

        result_key, scores = calculate_result(answers)

        result_name, qualities = TOTEMS[result_key]

        selected_name, selected_qualities = TOTEMS[selected]

        text = (
            f"✨ ТВОЙ ТОТЕМ — {selected_name}\n\n"
            f"По твоим ответам сейчас особенно сильно "
            f"звучит тема {qualities}.\n\n"
            f"{selected_name} — это про "
            f"{selected_qualities}.\n\n"
        )

        if result_key == selected:
            text += (
                "И самое интересное — твои ответы привели "
                "именно к тому образу, который ты выбрала "
                "интуитивно в последнем вопросе. 🖤\n\n"
            )
        else:
            text += (
                f"При этом твой интуитивный выбор — "
                f"{selected_name}. Именно он может быть тем "
                "образом, который сейчас особенно притягивает "
                "тебя. 🖤\n\n"
            )

        text += (
            "Если хочешь иметь свой тотем рядом, у меня есть "
            "готовые свечи с образами животных.\n\n"
            "🐾 Хочешь посмотреть свою свечу?"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🐾 ПОКАЗАТЬ МОЙ ТОТЕМ",
                    callback_data=f"show:{selected}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 ПРОЙТИ ЕЩЁ РАЗ",
                    callback_data="start_test"
                )
            ]
        ])

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )

        return

    if data.startswith("show:"):
        selected = data.split(":")[1]

        name, qualities = TOTEMS[selected]

        text = (
            f"{name}\n\n"
            f"Твой тотем — {name}.\n"
            f"Его ключевые качества: {qualities}.\n\n"
            "🕯️ У меня есть готовые свечи с тотемами.\n"
            "Если хочешь узнать наличие и актуальную цену, "
            "напиши мне в Telegram."
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "💬 НАПИСАТЬ МНЕ",
                    url="https://t.me/chydo27"
                )
            ],
            [
                InlineKeyboardButton(
                    "🕯️ ПРИГЛАШЕНИЕ В МАСТЕРСКУЮ",
                    url="https://t.me/chydorydom"
                )
            ]
        ])

        await query.edit_message_text(
            text,
            reply_markup=keyboard
        )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🐾 Нажми /start, чтобы пройти тест на свой тотем."
    )


def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Бот запущен...")

    webhook_url = os.getenv("RENDER_EXTERNAL_URL")

    if not webhook_url:
        raise RuntimeError(
            "Не найден адрес RENDER_EXTERNAL_URL"
        )

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "10000")),
        url_path="telegram",
        webhook_url=f"{webhook_url}/telegram",
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
