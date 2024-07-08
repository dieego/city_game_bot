import telebot
import cities
import main

cities_set=set()
bed_letter=set()
bed_cities=set()
# токен бота
bot = telebot.TeleBot("6628480103:AAEDGbtbIymdR0GHY7tNUYHes8y32YAouXk")
letter_next_word=''
#первый запуск цикла
first_start=True
#режим игры
game_mode=False

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "И тебе привет!")
    if "start" in message.text.lower() and not main.game_mode:
        bot.send_message(message.from_user.id, 'Привет, это игра в города c компьютером!\n'
                                               'Введите "старт" для начала игры"')
    if "старт" in message.text.lower() and not main.game_mode:
        bot.send_message(message.from_user.id, "Привет, это игра в города c компьютером!\n"
                                               "Из множества городов удалены города которые оканчиваются на неправильные буквы -\n"
                                               "ь,ы. Если ты их введёшь - то нужно будет повторить ввод!"
                                               "Введите город для начала игры!\n")
        main.cities_set = {city['name'].lower() for city in cities.cities}
        main.bed_letter = {city[-1] for city in main.cities_set}.difference({city[0] for city in main.cities_set})
        main.bed_cities = {city for city in main.cities_set if city[-1] in main.bed_letter}
        main.cities_set = {city for city in main.cities_set if not city[-1] in main.bed_letter}
        main.letter_next_word = ''
        # слово - ход компьютера
        computer_word = ''
        # первый запуск цикла
        main.first_start=True
        main.game_mode = True
    if "стоп" in message.text.lower() and main.game_mode:
        bot.send_message(message.from_user.id,'Введена строка "стоп" - конец игры\n'
                                              'Победитель: компьютер!!!\n'
                                              'Для новой игры введите "старт"')
        main.game_mode=False
    if message.text.lower() in main.cities_set and main.game_mode:
        if message.text.lower().startswith(main.letter_next_word) or main.first_start:
            main.cities_set.discard(message.text.lower())
            # получаем первую буква для следующего слова для компьютера
            main.letter_next_word = message.text.lower()[-1]
            # генерируем множество городов для хода компьютера
            comp_set = {city for city in main.cities_set if city.startswith(main.letter_next_word)}
            # в множестве городов для хода компьютера есть записи
            if comp_set:
                # удаляем случайный город из множества и сохраняем его в переменной comp_move
                comp_move = comp_set.pop()
                # удаляем город из множества городов
                main.cities_set.discard(comp_move)
                # выводим ход компьютера
                bot.send_message(message.from_user.id,f'Ход компьютера:{comp_move.capitalize()}. Вам город на "{comp_move[-1].upper()}"\n'
                                                      f'Или введите "стоп" для завершения игры')
                # получаем первую буква для следующего слова для игрока
                main.letter_next_word = comp_move[-1]
            else:
                bot.send_message(message.from_user.id,'Вы победитель. Поздравляю!!!\n'
                                                      'Для новой игры введите "старт"')
                main.game_mode = False
        else:
            bot.send_message(message.from_user.id,'Город начинается не с той буквы.\n'
                                                  'Компьютер выйграл!!!\n'
                                                  'Для новой игры введите "старт"')
            main.game_mode = False
    elif message.text.lower() in main.bed_cities and main.game_mode:
        bot.send_message(message.from_user.id, 'Вы ввели город оканчивающийся на "ь,ы".\n'
                                               'Повторите ввод')
    elif message.text.lower() not in main.cities_set and main.game_mode and "старт" not in message.text.lower():
        bot.send_message(message.from_user.id,'Такого города нет в списке городов.\n'
                                              'Компьютер выйграл!!!\n'
                                              'Для новой игры введите "старт"')
        main.game_mode = False






bot.polling(none_stop=True, interval=0)
