from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "8742729664:AAHKmoy1S2mSOuYM06DQJMW651EAi32FFHs"
URL = f"https://api.telegram.org/bot8742729664:AAHKmoy1S2mSOuYM06DQJMW651EAi32FFHs"

user_states = {}
user_stats = {}


def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        data["reply_markup"] = reply_markup

    requests.post(
        f"{URL}/sendMessage",
        json=data,
        timeout=10
    )


def set_main_keyboard(chat_id, buttons):
    keyboard = {
        "keyboard": [[{"text": button}] for button in buttons],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return keyboard


def init_user(chat_id):
    if chat_id not in user_states:
        user_states[chat_id] = "S1"
    if chat_id not in user_stats:
        user_stats[chat_id] = {
            "решимость": 0,
            "восприятие": 0,
            "Стив": 0,
            "Рей": 0
        }


def apply_stats(chat_id, changes):
    init_user(chat_id)
    for stat_name, value in changes.items():
        user_stats[chat_id][stat_name] += value


def get_s1_text():
    return """# S1 — Ты уже здесь
 
Ты просыпаешься резко.
 
Как будто тебя выдернули из чего-то.
 
…
 
Сначала — звук.
 
Глухой. Ритмичный.
 
Слишком ровный.
 
Слишком… чужой.
 
Секунда.
 
Вторая.
 
И только потом приходит понимание —
 
поезд.
 
…
 
Свет тусклый.
 
Тёплый.
 
Но в нём нет уюта.
 
Он будто липнет к коже, как воспоминание, которое ты пыталась не трогать.
 
Ты медленно поворачиваешь голову к окну.
 
Темнота.
 
Не ночь.
 
Не тоннель.
 
Просто… отсутствие.
 
Как будто за стеклом ничего не существует.
 
Ни огней. Ни отражений.
 
Ничего.
 
…
 
И в этот момент —
 
мысль.
 
Та самая.
 
От которой ты бежала.
 
Она возвращается не словами.
 
Ощущением.
 
Сжатым дыханием.
 
Знанием, что ты снова оставила всё как есть.
 
Потому что так проще.
 
Потому что так безопаснее.
 
Потому что так… привычно.
 
…
 
Ты резко отворачиваешься от окна.
 
Хватит.
 
Ты просто хотела отдохнуть.
 
Не думать.
 
Не возвращаться к этому.
 
…
 
Ты смотришь вперёд.
 
И в этот момент —
 
свет мигает.
 
Раз.
 
…
 
В дальнем конце вагона кто-то сидит.
 
Мужчина.
 
Он смотрит прямо на тебя.
 
Не моргая.
 
Слишком спокойно.
 
Слишком… долго.
  
Ты уверена — его там не было.
 
Ты бы заметила.
 
Ты бы точно заметила.
 
Свет гаснет и зажигается вновь.
  
Он ближе.
 
На несколько рядов.
 
Твоё дыхание сбивается.
 
Но ты не двигаешься.
 
Не показываешь.
 
Не успеваешь даже подумать.
  
Свет.
 
Миг.
  
Ещё ближе.
 
Через одно сиденье.
 
Теперь это уже не кажется случайностью.
 
Он не просто смотрит.
 
Он будто ждёт.
 
Будто знает.
 
Сердце бьёт в горле.
 
Но ты сидишь.
 
Не двигаешься.
 
Замираешь.
  
Свет снова гаснет.
  
И—
  
— БУ.
 
Рядом с тобой кто-то резко наклоняется.
 
Ты вздрагиваешь.
 
Сердце срывается.
 
Но—
 
это не он.
 
Парень.
 
Совсем другой.
 
Живой.
 
Реальный.
 
Он отстраняется, с лёгкой усмешкой.
 
— Прости. Не удержался.
 
Ты возвращаешь взгляд к сиденьям впереди.
 
Того мужчины —
 
нет.
 
Как будто его никогда не было.
 
…
 
Ты всё ещё держишься за сердце.
 
А он смотрит на тебя внимательно, изучающе."""
    

def get_s2_intro_kto_ty_takoy():
    return """Ты сжимаешь пальцы, стараясь держать голос ровным:
 
— Кто ты такой?
 
Парень чуть склоняет голову.
 
Будто ожидал именно этого.
 
— Друг, союзник… или будущий враг.
 
Лёгкая усмешка.
 
— Обычно сначала задают другой вопрос."""
    

def get_s2_intro_chto_proiskhodit():
    return """— Что здесь происходит?
 
Слишком резко.
 
Он не отвечает сразу.
 
Смотрит.
 
Как будто примеряет тебя к чему-то.
 
— Наконец-то правильный вопрос.
 
Пауза.
 
— Но ты задаёшь его не тогда."""
    

def get_s2_intro_promolchat():
    return """Ты отворачиваешься.
 
Смотришь в окно.
 
Пустота.
 
Делаешь вид, что его нет.
 
…
 
Он тихо усмехается.
 
— Да.
 
Так проще.
 
Пауза.
 
— Пока не станет поздно."""
    

def get_s2_common_text():
    return """Он откидывается на спинку сиденья, не отводя от тебя взгляда.
 
— Ты ещё не поняла.
 
Как будто это важно.
 
Как будто это — неизбежно.
 
…
 
Ты не успеваешь ответить.
 
Дверь в вагон открывается.
 
Без звука.
 
Просто —
 
сдвигается.
 
И внутрь заходит ещё один.
 
Другой.
 
Выше.
 
Собранный.
 
Спокойный.
 
Он сначала смотрит на парня перед тобой.
 
— Ты опять всех пугаешь, Стив.
 
Стив тихо усмехается.
 
— Не смог удержаться.
 
Кивает в сторону прохода между сиденьями.
 
— Оно уже было здесь.
 
…
 
Ты автоматически смотришь туда.
 
Пусто.
 
Но ощущение —
 
обратное.
 
Будто там секунду назад что-то было.
 
Второй парень резко переводит взгляд туда же.
 
Чётко.
 
Собранно.
 
— Тогда тем более не нужно было сюда заходить.
 
Тон спокойный.
 
Но в нём нет мягкости.
 
Стив чуть пожимает плечами.
 
— Не мог упустить момент.
 
Пауза.
 
— Оно редко подходит так близко."""
    

def send_s1(chat_id):
    keyboard = set_main_keyboard(chat_id, [
        "Кто ты такой?",
        "что происходит?",
        "Промолчать",
        "Игнорировать"
    ])
    send_message(chat_id, get_s1_text(), reply_markup=keyboard)
    user_states[chat_id] = "S1"


def send_s2_from_kto(chat_id):
    send_message(chat_id, get_s2_intro_kto_ty_takoy())
    keyboard = set_main_keyboard(chat_id, [
        "О чем вы?",
        "Осмотреться",
        "Игнор"
    ])
    send_message(chat_id, get_s2_common_text(), reply_markup=keyboard)
    user_states[chat_id] = "S2"


def send_s2_from_chto(chat_id):
    send_message(chat_id, get_s2_intro_chto_proiskhodit())
    keyboard = set_main_keyboard(chat_id, [
        "О чем вы?",
        "Осмотреться",
        "Игнор"
    ])
    send_message(chat_id, get_s2_common_text(), reply_markup=keyboard)
    user_states[chat_id] = "S2"


def send_s2_from_promolchat(chat_id):
    send_message(chat_id, get_s2_intro_promolchat())
    keyboard = set_main_keyboard(chat_id, [
        "О чем вы?",
        "Осмотреться",
        "Игнор"
    ])
    send_message(chat_id, get_s2_common_text(), reply_markup=keyboard)
    user_states[chat_id] = "S2"


def send_s2_from_ignore(chat_id):
    keyboard = set_main_keyboard(chat_id, [
        "О чем вы?",
        "Осмотреться",
        "Игнор"
    ])
    send_message(chat_id, get_s2_common_text(), reply_markup=keyboard)
    user_states[chat_id] = "S2"


@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return "no data", 200

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        init_user(chat_id)

        if text == "/start":
            user_stats[chat_id] = {
                "решимость": 0,
                "восприятие": 0,
                "Стив": 0,
                "Рей": 0
            }
            send_s1(chat_id)

        elif user_states.get(chat_id) == "S1":
            if text == "Кто ты такой?":
                apply_stats(chat_id, {
                    "решимость": 1,
                    "Стив": 1
                })
                send_s2_from_kto(chat_id)

            elif text == "что происходит?":
                apply_stats(chat_id, {
                    "решимость": 1,
                    "восприятие": 1,
                    "Рей": 1
                })
                send_s2_from_chto(chat_id)

            elif text == "Промолчать":
                apply_stats(chat_id, {
                    "решимость": -1
                })
                send_s2_from_promolchat(chat_id)

            elif text == "Игнорировать":
                apply_stats(chat_id, {
                    "восприятие": -1,
                    "Рей": -1
                })
                send_s2_from_ignore(chat_id)

            else:
                send_message(chat_id, "Выбери один из вариантов на кнопках.")

        elif user_states.get(chat_id) == "S2":
            if text == "О чем вы?":
                apply_stats(chat_id, {
                    "решимость": 1,
                    "Рей": 1
                })
                send_message(chat_id, "S3_О чем вы")

            elif text == "Осмотреться":
                apply_stats(chat_id, {
                    "восприятие": 1,
                    "Стив": 1
                })
                send_message(chat_id, "S3_Осмотреться")

            elif text == "Игнор":
                apply_stats(chat_id, {
                    "восприятие": -1,
                    "Рей": -2
                })
                send_message(chat_id, "S3_Игнор")

            else:
                send_message(chat_id, "Выбери один из вариантов на кнопках.")
