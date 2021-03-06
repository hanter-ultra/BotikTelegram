import telebot, ctypes, requests, urllib.request, cv2, random
from os import system as s
import platform as pf
from pyautogui import screenshot as scr
from os.path import abspath as pat
from time import time
from config import TOKEN, chat_id_1, chat_id_2
import wiki
from news import parse_news_abh, parse_news_word
from web_search import  web_search_google
from music import  parse_music


bot = telebot.TeleBot(TOKEN)

adress = ''
need_format = False

requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_2}&text=Online")


def sender(id, text):
    bot.send_message(id, text)

def send_photo(id, image):
    bot.send_photo(id, image)



@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!'
                                      '\nВ этом замечательном ботике реализованы функции с помощью общения'
                                      '\nТы можешь узнать:'
                                      '\n\n"Какие новости" - и он отправит мировые новости'
                                      '\n\n"Какие новости в Абхазии" - отправит Абхазские новости'
                                      '\n\n"Найди в гугл (твой запрос без скобок)" - отправит несколько страниц из поиска'
                                      '\n\n"Отправь музыку" - отправит название ссылку на скачивание'
                                      '\n\n\nТакже есть функции:'
                                      '\n\n/ping - узнать пинг'
                                      '\n\n/my_id - узнать id'
                                      '\n\n/autoformat - ты отправляешь документ Python и бот форматирует документ по стандарту pip8'
                                      '\n\n\nПользуйся на здоровье!!!'
                                      '\nTeam из одного человека - Ботик©')


@bot.message_handler(commands=['ping'])
def ping(message):
    st = message.date.real
    sender(message.chat.id, f'Твой пинг: {round(time()-st+42, 2)}')


@bot.message_handler(commands=['my_id'])
def my_id(message):
    sender(message.chat.id, message.chat.id)


@bot.message_handler(commands=['photo'])
def screen(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        try:
            scr('screenshot.jpeg')
            file = open('screenshot.jpeg', 'rb')
            send_photo(message.chat.id, file)
            file.close()
            s('del screenshot.jpeg')
        except:
            sender(message.chat.id, 'Error!')


@bot.message_handler(commands=['wallpaper'])
def desk(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        msg = bot.send_message(message.chat.id, 'Пришли мне фото или ссылку на фото')
        bot.register_next_step_handler(msg, loader)

@bot.message_handler(content_types=['photo', 'text'], func = lambda message: ((message.photo) or (message.text and ('http' in message.text.lower()))))
def loader(message):
    if message.photo:
        img = bot.get_file(message.photo[-1].file_id)
        path = bot.download_file(img.file_path)
        with open('wall.jpg', 'wb') as file:
            file.write(path)
        file.close()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpg'), 0)
        sender(message.chat.id, 'Обои успешно установлены!')
    elif 'http' in message.text.lower():
        try:
            img = urllib.request.urlopen(message.text).read()
            with open('wall.jpg', 'wb') as file:
                file.write(img)
            file.close()
            ctypes.windll.user32.SystemParametersInfoW(20, 0, pat('wall.jpg'), 0)
            sender(message.chat.id, 'Обои успешно установлены!')
        except:
            sender(message.chat.id, 'По этой ссылке установить изображение невозможно. Прими мои соболезнования(')
    else:
        sender(message.chat.id, 'Что-то пошло не так...')


@bot.message_handler(commands=['autoformat'])
def to_format(message):
    need_format = True
    msg = bot.send_message(message.chat.id, 'Пришли мне Python документ и я сделаю из него конфет')
    bot.register_next_step_handler(msg, formater)


@bot.message_handler(content_types = ['document'], func = lambda need_format: ((need_format == True) and (message.document)))
def formater(message):
    if message.document:
        if message.document.file_name.endswith('.py'):
            doc = bot.get_file(message.document.file_id)
            path = bot.download_file(doc.file_path)

            with open(f'loaded{message.chat.id}.py', 'wb') as file:
                file.write(path)
            file.close()
            sender(message.chat.id, 'Файл загружен! Идет обработка...')

            s(f'yapf -i loaded{message.chat.id}.py')
            sender(message.chat.id, 'Держи свой конфет!)')

            file = open(f'loaded{message.chat.id}.py', 'rb')
            bot.send_document(message.chat.id, file)
            file.close()
            s(f'del loaded{message.chat.id}.py')
        else:
            sender(message.chat.id, 'Отправь документ Python. Другой вид я не форматирую.')
        need_format = False
    else:
        sender(message.chat.id, 'Что-то пошло не так(')
    need_format = False


@bot.message_handler(commands=['ip', 'ip_address'])
def ip_address(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        response = requests.get('http://jsonip.com/').json()
        sender(message.chat.id, f'IP Адрес: {response["ip"]}')


@bot.message_handler(commands=['spec', 'specifications'])
def spec(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        msg = f"Имя компьютера: {pf.node()}\nПроцессор: {pf.processor()}\nСистема: {pf.system()} {pf.release()}"
        sender(message.chat.id, msg)


@bot.message_handler(commands=['camera', 'cam'])
def camera(message):
    if message.chat.id == chat_id_1 or message.chat.id == chat_id_2:
        cap = cv2.VideoCapture(0)

        for i in range(30):
            cap.read()

        ret, frame = cap.read()

        cv2.imwrite('cam.jpg', frame)
        cap.release()

        with open('cam.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)

        s('del cam.jpg')




@bot.message_handler(content_types=['text'])
def saw(message):
    id = message.chat.id
    msg = message.text

    if msg == 'Привет' or msg =='Приветик' or msg == 'Приветствую' or msg == 'И тебе привет' or msg == 'Здаров' or msg == 'Мир тебе, путник':
        answer = ['И тебе привет', 'Привет', 'Приветик', 'Здаров', 'Мир тебе, путник!']
        sender(id, random.choice(answer))

    if msg == 'Как дела?' or msg == 'Что нового?' or msg == 'Как ты?' or msg == 'Как дела' or msg == 'Что нового' or msg == 'Как ты':
        a = ['Все хорошо', 'Отлично', 'Работаю', 'Делаю свои дела)', 'Думаю что все хорошо)']
        sender(id, random.choice(a))

    if msg == 'Какие новости в мире' or msg == 'Какие новости' or msg == 'Что происходит в мире':
        parse_news_word(message)

    if msg == 'Какие новости в Абхазии' or msg == 'Новости в Абхазии' or msg == 'Что происходит в Абхазии':
        parse_news_abh(message)

    if 'Найди в гугл' in msg or 'Поищи в гугл' in msg:
        web_search_google(message)

    if msg == 'Музыка' or msg == 'Музон' or msg == 'Отправь музыку':
        parse_music(message)

    # if 'Найди в ютуб' in msg or 'Поищи в ютуб' in msg:
    #     adress = msg.replace('Найди в ютуб', '').strip()
    #     adress = adress.replace('Поищи в ютуб', '').strip()
    #     text = msg.replace(adress, '').strip()
    #     web_search_youtube(message)

    if msg == 'Поиск в википедии' or msg == 'Найди в википедии':
        adress = msg.replace('Поиск в википедии', '').strip()
        adress = adress.replace('Найди в википедии', '').strip()
        text = msg.replace(adress, '').strip()
        rezult, urlrez = wiki.search_wiki(text)
        bot.send_message(message.chat.id, rezult + urlrez)


    else:
        if message.chat.id != chat_id_1 and message.chat.id != chat_id_2:
            bot.send_message(chat_id_2, f'Пользователь с именем: {message.from_user.first_name} {message.from_user.last_name}\nid-пользователя: {message.from_user.id}\nСсылка: @{message.from_user.username}\nОтправил сообщение:\n\n{msg}')


# Поиск в википедии
def wikipedia(context, message):
    bot.send_message(message.chat.id, "Идет поиск в википедии...")
    context.user_data[str(random.randint(1000000,9999999))] = (" ".join(context.args))
    rezult, urlrez = wiki.search_wiki(" ".join(context.args))
    bot.send_message(message.chat.id, rezult + urlrez)



print('Ботик запущен')
bot.polling(none_stop = True, interval = 0)