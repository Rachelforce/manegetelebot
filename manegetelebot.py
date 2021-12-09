from telebot import TeleBot, types

token = '5088010288:AAE9O-yPmUPUiKNH_7WCTNPATUQduEKxVO0'
bot = TeleBot(token)
user_state = {}


class Answer:
    def __init__(self, text, state):
        self.text = text
        self.state = state


class State:
    def __init__(self, answers, phrase):
        self.answers = answers
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for el in self.answers:
            self.keyboard.add(el)
        self.phrase = phrase

    def process_state(self, user):
        bot.send_message(user, self.phrase, reply_markup=self.keyboard)


class ButtonState(State):
    def check_answer(self, user, answer):
        if answer in self.answers.keys():
            if self.answers[answer].text != "":
                bot.send_message(user, self.answers[answer].text, reply_markup=self.keyboard)
            user_state[user] = self.answers[answer].state


class TextState(State):
    def __init__(self, answers, phrase, true_answer):
        super().__init__(answers, phrase)
        self.true_answer = true_answer

    def check_answer(self, user, answer):
        if answer in self.answers.keys():
            bot.send_message(user, self.answers[answer].text, reply_markup=self.keyboard)
            user_state[user] = self.answers[answer].state
        elif answer == self.true_answer:
            bot.send_message(user, "✅ Верно")
            user_state[user] += 1
        else:
            bot.send_message(user, "❌ Не верно")


n_states = 9
states = list(range(n_states))
states[0] = ButtonState(
    {
        "🧩 Начать квест": Answer("", 1),
        "🎧 Прослушать аудиогид по выставке": Answer(
            "https://izi.travel/en/browse/76ad97a7-3969-4427-a0c7-08b20490d65f?lang=ru",
            0),
        "🎵 Послушать саундтрек к выставке": Answer("https://batagov.lnk.to/pokoiiradost", 0),
    },
    "📋 Вы в главном меню"
)

states[1] = ButtonState(
    {
        "➡️Далее": Answer("Начали!", 2),
        "✖️Выход": Answer("✖️Выход", 0)
    },
    "Вы начали квест ознакомитесь со статьей (https://telegra.ph/Mezhmuzejnyj-vystavochnyj-proekt-Pokoj-i-Radost-12-09)."
)

states[2] = ButtonState(
    {
        "Ответ 1": Answer("❌ Не верно", 2),
        "Ответ 2": Answer("✅ Верно!", 3),
        "Ответ 3": Answer("❌ Не Верно!", 2),
        "✖️Выход": Answer("✖️Выход", 0)
    },
    "Выбрать 3 картины (выбор ребят), по ним краткая информация и вопросы к каждой. Нужно выбрать верный вариант"
)

states[3] = TextState(
    {"✖️Выход": Answer("✖️Выход", 0)},
    "Загадана какая-то картина и нужно найти ее и отправить ответ: автор, название картины. ответ - 123",
    "123"
)

states[4] = TextState(
    {"✖️Выход": Answer("✖️Выход", 0)},
    "Статья про жанры (коротко) и нужно посчитать количество натюрмортов и пейзажей. 48",
    "48"
)

states[5] = ButtonState(
    {"➡️Далее": Answer("Продлжим!", 6)},
    "Ура! Ты на пол пути! Поднимайся наверх.\nПока идешь послушай: \nhttps://batagov.lnk.to/pokoiiradost"
)

states[6] = TextState(
    {"✖️Выход": Answer("✖️Выход", 0)},
    "Вопрос с правильным ответом 1",
    "1"
)

states[7] = ButtonState({
    "Ответ 1": Answer("❌ Не верно", 7),
    "Ответ 2": Answer("✅ Верно!", 8),
    "Ответ 3": Answer("❌ Не Верно!", 7),
    "✖️Выход": Answer("✖️Выход", 0)
},
    "Еще один вопрос с выбором."
)

states[8] = ButtonState(
    {"УРА❗": Answer("УРА❗", 0)},
    "УРА! Ты победил!"
)


@bot.message_handler(commands=["start"])
def start_game(message):
    user = message.chat.id
    user_state[user] = 0
    bot.send_message(user, "Добро пожаловать в телеграм бот от манежа! (текст 1)", reply_markup=states[0].keyboard)


@bot.message_handler(content_types=["text"])
def user_answer(message):
    user = message.chat.id
    answer = message.text
    if user not in user_state:
        user_state[user] = 0
    states[user_state[user]].check_answer(user, answer)
    states[user_state[user]].process_state(user)
    print(states[user_state[user]])

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass
