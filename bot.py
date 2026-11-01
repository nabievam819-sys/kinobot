import asyncio
import os
import random
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# ==============================
# 1. НАСТРОЙКИ БОТА
# ==============================

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: добавь BOT_TOKEN в файл .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==============================
# 2. ГЛАВНОЕ МЕНЮ
# ==============================

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⭐ Топ фильмов")],
        [KeyboardButton(text="🔍 Найти по коду")],
        [KeyboardButton(text="🎲 Случайный фильм")],
        [KeyboardButton(text="🎭 Жанры")],
        [KeyboardButton(text="❤️ Избранное")],
        [KeyboardButton(text="ℹ️ Помощь")]
    ],
    resize_keyboard=True
)

# ==============================
# 3. КАТАЛОГ ФИЛЬМОВ
# Коды от 1000 до 1050
# ==============================

movies = {
    1000: {"title": "Интерстеллар", "year": 2014, "genre": "Фантастика, драма", "description": "Путешествие через космос в поисках нового дома.", "rating": 8.7},
    1001: {"title": "Начало", "year": 2010, "genre": "Фантастика, триллер", "description": "История о проникновении в человеческие сны.", "rating": 8.8},
    1002: {"title": "Матрица", "year": 1999, "genre": "Фантастика, боевик", "description": "Мир оказывается искусственной реальностью.", "rating": 8.7},
    1003: {"title": "Зелёная миля", "year": 1999, "genre": "Драма, фэнтези", "description": "История необычного заключённого.", "rating": 9.1},
    1004: {"title": "Побег из Шоушенка", "year": 1994, "genre": "Драма", "description": "История надежды и свободы.", "rating": 9.3},
    1005: {"title": "1+1", "year": 2011, "genre": "Комедия, драма", "description": "Необычная дружба двух разных людей.", "rating": 8.8},
    1006: {"title": "Титаник", "year": 1997, "genre": "Мелодрама", "description": "История любви на борту легендарного корабля.", "rating": 7.9},
    1007: {"title": "Аватар", "year": 2009, "genre": "Фантастика", "description": "Путешествие на планету Пандора.", "rating": 7.9},
    1008: {"title": "Гладиатор", "year": 2000, "genre": "Боевик, драма", "description": "История римского генерала.", "rating": 8.5},
    1009: {"title": "Форрест Гамп", "year": 1994, "genre": "Драма", "description": "Необычная жизнь простого человека.", "rating": 8.8},
    1010: {"title": "Король Лев", "year": 1994, "genre": "Мультфильм", "description": "История львёнка Симбы.", "rating": 8.5},
    1011: {"title": "Джокер", "year": 2019, "genre": "Драма, триллер", "description": "История превращения человека в Джокера.", "rating": 8.4},
    1012: {"title": "Тёмный рыцарь", "year": 2008, "genre": "Боевик", "description": "Бэтмен против Джокера.", "rating": 9.0},
    1013: {"title": "Паразиты", "year": 2019, "genre": "Триллер", "description": "Две семьи с разной жизнью.", "rating": 8.5},
    1014: {"title": "Дюна", "year": 2021, "genre": "Фантастика", "description": "Борьба за планету Арракис.", "rating": 8.0},
    1015: {"title": "Властелин колец", "year": 2001, "genre": "Фэнтези", "description": "Путешествие ради уничтожения кольца.", "rating": 8.9},
    1016: {"title": "Гарри Поттер и философский камень", "year": 2001, "genre": "Фэнтези", "description": "Первый год Гарри в школе магии.", "rating": 7.6},
    1017: {"title": "Пираты Карибского моря", "year": 2003, "genre": "Приключения", "description": "Приключения капитана Джека Воробья.", "rating": 8.1},
    1018: {"title": "Один дома", "year": 1990, "genre": "Комедия", "description": "Мальчик защищает дом от грабителей.", "rating": 7.7},
    1019: {"title": "Назад в будущее", "year": 1985, "genre": "Фантастика", "description": "Путешествие во времени.", "rating": 8.5},
    1020: {"title": "Терминатор 2", "year": 1991, "genre": "Фантастика, боевик", "description": "Борьба за будущее человечества.", "rating": 8.6},
    1021: {"title": "Человек-паук: Нет пути домой", "year": 2021, "genre": "Фантастика", "description": "Питер Паркер встречает неожиданных гостей.", "rating": 8.2},
    1022: {"title": "Железный человек", "year": 2008, "genre": "Боевик", "description": "История создания брони Железного человека.", "rating": 7.9},
    1023: {"title": "Мстители: Финал", "year": 2019, "genre": "Фантастика, боевик", "description": "Последняя битва с Таносом.", "rating": 8.4},
    1024: {"title": "ВАЛЛ-И", "year": 2008, "genre": "Мультфильм", "description": "Робот ищет жизнь среди руин Земли.", "rating": 8.4},
    1025: {"title": "Вверх", "year": 2009, "genre": "Мультфильм", "description": "Путешествие дома на воздушных шарах.", "rating": 8.3},
    1026: {"title": "Тайна Коко", "year": 2017, "genre": "Мультфильм", "description": "Мальчик открывает мир музыки и семьи.", "rating": 8.4},
    1027: {"title": "Холодное сердце", "year": 2013, "genre": "Мультфильм", "description": "История сестёр Эльзы и Анны.", "rating": 7.4},
    1028: {"title": "Шрек", "year": 2001, "genre": "Мультфильм, комедия", "description": "Огр отправляется спасать принцессу.", "rating": 7.9},
    1029: {"title": "Как приручить дракона", "year": 2010, "genre": "Мультфильм", "description": "Дружба мальчика и дракона.", "rating": 8.1},
    1030: {"title": "Пятый элемент", "year": 1997, "genre": "Фантастика", "description": "Спасение Земли от космической угрозы.", "rating": 7.6},
    1031: {"title": "Леон", "year": 1994, "genre": "Криминал, драма", "description": "История дружбы киллера и девочки.", "rating": 8.5},
    1032: {"title": "Достучаться до небес", "year": 1997, "genre": "Драма, комедия", "description": "Двое друзей отправляются к морю.", "rating": 7.8},
    1033: {"title": "Остров проклятых", "year": 2010, "genre": "Детектив, триллер", "description": "Расследование в психиатрической больнице.", "rating": 8.2},
    1034: {"title": "Престиж", "year": 2006, "genre": "Триллер, драма", "description": "Соперничество двух иллюзионистов.", "rating": 8.5},
    1035: {"title": "Сияние", "year": 1980, "genre": "Ужасы", "description": "Семья оказывается в загадочном отеле.", "rating": 8.4},
    1036: {"title": "Заклятие", "year": 2013, "genre": "Ужасы", "description": "Паранормальное расследование семьи.", "rating": 7.5},
    1037: {"title": "Тихое место", "year": 2018, "genre": "Ужасы, триллер", "description": "Семья пытается выжить в мире тишины.", "rating": 7.5},
    1038: {"title": "Пила", "year": 2004, "genre": "Ужасы, триллер", "description": "Люди оказываются в смертельной игре.", "rating": 7.6},
    1039: {"title": "Оно", "year": 2017, "genre": "Ужасы", "description": "Дети сталкиваются с таинственным злом.", "rating": 7.3},
    1040: {"title": "Достать ножи", "year": 2019, "genre": "Детектив, комедия", "description": "Детектив расследует загадочную смерть.", "rating": 7.9},
    1041: {"title": "Семь", "year": 1995, "genre": "Детектив, триллер", "description": "Два детектива ищут серийного убийцу.", "rating": 8.6},
    1042: {"title": "Исчезнувшая", "year": 2014, "genre": "Триллер, детектив", "description": "Загадочное исчезновение женщины.", "rating": 8.1},
    1043: {"title": "Красотка", "year": 1990, "genre": "Мелодрама, комедия", "description": "Необычная история любви.", "rating": 7.1},
    1044: {"title": "Дневник памяти", "year": 2004, "genre": "Мелодрама", "description": "История любви длиною в жизнь.", "rating": 7.8},
    1045: {"title": "Ла-Ла Ленд", "year": 2016, "genre": "Мюзикл, мелодрама", "description": "Музыкант и актриса ищут свою мечту.", "rating": 8.0},
    1046: {"title": "Бойцовский клуб", "year": 1999, "genre": "Драма, триллер", "description": "Загадочный клуб меняет жизнь героя.", "rating": 8.8},
    1047: {"title": "Одержимость", "year": 2014, "genre": "Драма, музыка", "description": "Барабанщик стремится стать великим музыкантом.", "rating": 8.5},
    1048: {"title": "Грань будущего", "year": 2014, "genre": "Фантастика, боевик", "description": "Солдат снова переживает один день.", "rating": 7.9},
    1049: {"title": "Марсианин", "year": 2015, "genre": "Фантастика, приключения", "description": "Астронавт пытается выжить на Марсе.", "rating": 8.0},
    1050: {"title": "Поймай меня, если сможешь", "year": 2002, "genre": "Криминал, драма", "description": "История мошенника и агента ФБР.", "rating": 8.1}
}

# ==============================
# 4. ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ
# ==============================

favorites = {}
user_ratings = {}

# ==============================
# 5. КАРТОЧКА ФИЛЬМА
# ==============================

def movie_card(code):
    movie = movies[code]

    return (
        f"🎬 {movie['title']}\n\n"
        f"🔢 Код: {code}\n"
        f"📅 Год: {movie['year']}\n"
        f"🎭 Жанр: {movie['genre']}\n"
        f"⭐ Рейтинг каталога: {movie['rating']}/10\n\n"
        f"📝 {movie['description']}\n\n"
        f"Чтобы сохранить фильм: /save {code}\n"
        f"Чтобы оценить: /rate {code} 10\n\n"
        "🍿 Приятного просмотра!"
    )

# ==============================
# 6. КОМАНДА START
# ==============================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"🍿 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в KinoBot!\n"
        "Твой личный помощник в мире кино.\n\n"
        "🔍 Ищи фильмы по кодам.\n"
        "⭐ Смотри популярные фильмы.\n"
        "❤️ Сохраняй любимые.\n"
        "🎲 Получай случайные рекомендации.\n\n"
        "Выбирай действие в меню 👇",
        reply_markup=keyboard
    )

# ==============================
# 7. КОМАНДА HELP
# ==============================

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📚 КОМАНДЫ KINOBOT\n\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/top — топ фильмов\n"
        "/random — случайный фильм\n"
        "/genres — жанры\n"
        "/favorites — избранное\n"
        "/save 1000 — сохранить фильм\n"
        "/rate 1000 10 — оценить фильм\n\n"
        "🔍 Просто отправь номер от 1000 до 1050."
    )

# ==============================
# 8. ПОИСК ПО КОДУ
# ==============================

@dp.message(Command("find"))
async def find_command(message: types.Message):
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Напиши, например: /find 1000")
        return

    code = int(parts[1])
    await find_movie(message, code)


async def find_movie(message: types.Message, code: int):
    if code in movies:
        await message.answer(movie_card(code))
    else:
        await message.answer(
            "❌ Фильм не найден.\n"
            "Попробуй код от 1000 до 1050."
        )

# ==============================
# 9. ТОП ФИЛЬМОВ
# ==============================

@dp.message(Command("top"))
async def top_movies(message: types.Message):
    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    result = "⭐ ТОП ФИЛЬМОВ KINOBOT\n\n"

    for code, movie in sorted_movies[:10]:
        result += (
            f"🎬 {movie['title']}\n"
            f"🔢 Код: {code} | ⭐ {movie['rating']}/10\n\n"
        )

    await message.answer(result)

# ==============================
# 10. СЛУЧАЙНЫЙ ФИЛЬМ
# ==============================

@dp.message(Command("random"))
async def random_movie(message: types.Message):
    code = random.choice(list(movies.keys()))
    await message.answer(movie_card(code))

# ==============================
# 11. ЖАНРЫ
# ==============================

@dp.message(Command("genres"))
async def genres(message: types.Message):
    genre_list = sorted({
        genre.strip()
        for movie in movies.values()
        for genre in movie["genre"].split(",")
    })

    result = "🎭 ЖАНРЫ KINOBOT\n\n"

    for genre in genre_list:
        result += f"• {genre}\n"

    result += "\nОтправь код фильма, чтобы посмотреть его."

    await message.answer(result)

# ==============================
# 12. ИЗБРАННОЕ
# ==============================

@dp.message(Command("favorites"))
async def show_favorites(message: types.Message):
    user_id = message.from_user.id
    saved = favorites.get(user_id, [])

    if not saved:
        await message.answer(
            "❤️ Избранное пока пустое.\n"
            "Напиши /save 1000, чтобы сохранить фильм."
        )
        return

    result = "❤️ ТВОЁ ИЗБРАННОЕ\n\n"

    for code in saved:
        result += f"🎬 {movies[code]['title']} — код {code}\n"

    await message.answer(result)

@dp.message(Command("save"))
async def save_movie(message: types.Message):
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Напиши, например: /save 1000")
        return

    code = int(parts[1])

    if code not in movies:
        await message.answer("❌ Фильм не найден.")
        return

    user_id = message.from_user.id
    favorites.setdefault(user_id, [])

    if code in favorites[user_id]:
        await message.answer("Фильм уже в избранном ❤️")
    else:
        favorites[user_id].append(code)
        await message.answer(
            f"❤️ {movies[code]['title']} сохранён!"
        )

# ==============================
# 13. ОЦЕНКА ФИЛЬМА
# ==============================

@dp.message(Command("rate"))
async def rate_movie(message: types.Message):
    parts = message.text.split()

    if (
        len(parts) != 3
        or not parts[1].isdigit()
        or not parts[2].isdigit()
    ):
        await message.answer(
            "Напиши, например: /rate 1000 10\n"
            "Оценка должна быть от 1 до 10."
        )
        return

    code = int(parts[1])
    rating = int(parts[2])

    if code not in movies:
        await message.answer("❌ Фильм не найден.")
        return

    if not 1 <= rating <= 10:
        await message.answer("Оценка должна быть от 1 до 10.")
        return

    user_id = message.from_user.id
    user_ratings.setdefault(code, {})
    user_ratings[code][user_id] = rating

    await message.answer(
        f"⭐ Ты поставил фильму "
        f"«{movies[code]['title']}» оценку {rating}/10. Спасибо!"
    )

# ==============================
# 14. ОБРАБОТКА КНОПОК И ТЕКСТА
# ==============================

@dp.message()
async def handle_message(message: types.Message):
    text = (message.text or "").strip()
    lower = text.lower()

    if text.isdigit():
        await find_movie(message, int(text))

    elif lower == "⭐ топ фильмов".lower():
        await top_movies(message)

    elif lower == "🔍 найти по коду".lower():
        await message.answer(
            "🔍 Введи код фильма от 1000 до 1050."
        )

    elif lower == "🎲 случайный фильм".lower():
        await random_movie(message)

    elif lower == "🎭 жанры".lower():
        await genres(message)

    elif lower == "❤️ избранное".lower():
        await show_favorites(message)

    elif lower == "ℹ️ помощь".lower():
        await help_command(message)

    elif "привет" in lower:
        await message.answer(
            "Привет! 👋 Добро пожаловать в KinoBot! 🍿"
        )

    elif "спасибо" in lower:
        await message.answer(
            "Всегда пожалуйста! ❤️ Приятного просмотра!"
        )

    else:
        await message.answer(
            "🤔 Я пока не понял сообщение.\n"
            "Отправь код фильма или нажми /help."
        )

# ==============================
# 15. ЗАПУСК БОТА
# ==============================

async def main():
    try:
        print("KinoBot запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
