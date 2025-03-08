import telebot
import random
import os

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот по правильной сортировке мусора. Напиши что-нибудь!")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
@bot.message_handler(commands=['trash'])
def send_prre(message):
    bot.reply_to(message, "Ты знаешь как правильно сортировать мусор?🧐")
    bot.send_message(message, "Если да то хорошо, если нет то я тебе щас покажу😎")
@bot.message_handler(commands=['wel'])
def send_pre(message):
    """
    Handles the /wel command.  Defines the sort_waste function and local rules,
    then calls sort_waste with example inputs and sends the results to the user.
    """
    def sort_waste(waste_type, is_clean=True, local_rules=None):
        """
        Определяет, как правильно отсортировать отход, учитывая тип, чистоту и местные правила.

        Args:
            waste_type (str): Тип отхода (например, "plastic_bottle", "newspaper", "battery").
            is_clean (bool): Чистый ли отход (по умолчанию True).
            local_rules (dict, optional): Словарь с местными правилами сортировки.
                Ключи - частичные совпадения с waste_type (например, "plastic").
                Значения - инструкции по сортировке. Defaults to None.

        Returns:
            str: Инструкции по сортировке отхода.
        """

        waste_type = waste_type.lower()

        if local_rules:
            for rule_keyword, rule_instruction in local_rules.items():
                if rule_keyword in waste_type:
                    return rule_instruction

        if "plastic" in waste_type:
            if is_clean:
                return "Ополосните, снимите крышку и сдайте в контейнер для перерабатываемого пластика."
            else:
                return "К сожалению, грязный пластик нельзя переработать. Выбросите в контейнер для смешанных отходов."
        elif "paper" in waste_type:
            return "Удалите скобы и скрепки, сдайте в контейнер для перерабатываемой бумаги."
        elif "glass" in waste_type:
            return "Ополосните, снимите крышку и сдайте в контейнер для перерабатываемого стекла."
        elif "metal" in waste_type:
            return "Ополосните и сдайте в контейнер для перерабатываемого металла."
        elif "battery" in waste_type or "electronic" in waste_type:
            return "Сдайте в специальный пункт приема опасных отходов."
        elif "organic" in waste_type:
            return "Используйте компостный контейнер или биоразлагаемый пакет."
        else:
            return "Пожалуйста, уточните тип отхода и проверьте местные правила утилизации."

    local_rules_N = {
        "plastic_bag": "Пластиковые пакеты принимаются в специальном контейнере в супермаркете.",
        "pizza_box": "Коробки из-под пиццы, даже грязные, можно сдать в переработку (но лучше удалить остатки пиццы)."
    }

    results = []
    results.append(sort_waste("plastic_bag", local_rules=local_rules_N))
    results.append(sort_waste("pizza_box", local_rules=local_rules_N))
    results.append(sort_waste("glass_bottle"))
    results.append(sort_waste("dirty_plastic_container", is_clean=False))

    # Send the results back to the user in one message.
    response_text = "\n".join(results)
    bot.reply_to(message, response_text)

@bot.message_handler(commands=['weltrash'])
def send_pe(message):
    """
    Handles the /weltrash command.  Sends a random image from the mems/ directory.
    """
    try:
        file_list = os.listdir('mems')
        if file_list:
            img_name = random.choice(file_list)
            with open(os.path.join('mems', img_name), 'rb') as f:
                bot.send_photo(message.chat.id, f)
        else:
            bot.reply_to(message, "В папке 'mems' нет изображений.")
    except FileNotFoundError:
        bot.reply_to(message, "Папка 'mems' не найдена.")
    except Exception as e:
        print(f"Error sending meme: {e}")
        bot.reply_to(message, "Произошла ошибка при отправке мема.")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    """Handles the /bye command."""
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
