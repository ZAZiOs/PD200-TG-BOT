import logging
import hashlib
import random
import os
import json
from aiogram_broadcaster import TextBroadcaster #Требует установки.
from aiogram import Bot, Dispatcher, executor, types #Требует установки.
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, \
    InlineKeyboardMarkup, InlineKeyboardButton
API_TOKEN = '5119758921:AAER4wLBOY6bbEChecbjGyTzqcP4vYMQ_WA'

#переменные для удобной работы с ботом
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
adminlist = [1010473369, 1547423409, 840744443, 1245222468] #ZAZiOs, Babloment, KrutosX, Calamity
database = 'data.json'


## Функции:

#добавление правды
def AddingTruth():
    return 'Правда'

#добавление действия
def AddingAction():
    return 'Действие'

#объявления
def ShoutOuting(message: types.Message):
    async def shoutFX(message: types.Message):
        with open(database, "r", encoding= "utf-8") as f:
            print(f)
            content = json.load(f)
            print(content)
        for id in content["ids"]:
            print(id)
            await message.answer(id, 'test')
        return "Успех!"

#Рандом для правды
def truthFX():
    with open('Truth.txt', 'r', encoding="utf-8") as truthNR:
        truthNS = truthNR.read()
        truthLS = truthNS.split("\n")
        truth = random.choice(truthLS)
    return 'Правда - ' + truth

#Рандом для действия
def actionFX():
    with open('Action.txt', 'r', encoding="utf-8") as actionNR:
        actionNS = actionNR.read()
        actionLS = actionNS.split("\n")
        action = random.choice(actionLS)
    return 'Действие - ' + action

#Рандом среди правд и действий
def randomFX():
    with open('Truth.txt', 'r', encoding="utf-8") as truthNR: #Записываем файл но он не прочитан ещё, NON-READ
        truthNS = truthNR.read() #Зачитываем файл, но он буквально считывается с энтерами, Не подходит NON-SPLIT
        truthLS = truthNS.split("\n") #Разделяем все ентеры на список аля ['пидор','пизда'] LIST
        truth = ('Правда - ' + random.choice(truthLS))
    with open('Action.txt', 'r', encoding="utf-8") as actionNR: 
        actionNS = actionNR.read()
        actionLS = actionNS.split("\n")
        action = ('Действие - ' + random.choice(actionLS))
    randomR = random.choice([action, truth]) #Выбираем со списка случайное значение
    return randomR


## Основные команды


#Старт, с клавиатурой об оповещениях

@dp.message_handler(commands=['start', 'help',])
async def send_welcome(message: types.Message):
    print("start: ", message.from_user.id)
    if message.from_user.id in adminlist:
        keyboard_markup = types.InlineKeyboardMarkup()
        NotifyEnable = types.InlineKeyboardButton('Включить оповещения об обновлениях', callback_data= 'AddNotify')
        NotifyDisable = types.InlineKeyboardButton('Выключить оповещения об обновлениях', callback_data= 'RemNotify')
        Notify = InlineKeyboardMarkup(row_width=1).add(NotifyEnable, NotifyDisable)
        await message.reply(
"""Бот для игры в <b>Правда или Действие</b> в котором подготовлено свыше двухста различных действий и правд!
Я периодически дополняю правды или действия так чтобы в бота было интереснее играть. Если у вас есть идеи, пишите мне в лс @ZAZiOs
Список команд:
Случайно: /r /random
Только правда: /t /truth
Только действие: /a /action

Теперь <b>ваша</b> правда или действие может попасть к нам в бота!
<i>Для этого заполните форму: https://forms.gle/euLw44oaVGMo311B6</i>

Нашли баг? Пишите: @ZAZiOs
<i>Бот написан используя aiogram, помощь с прогингом @KrutosX</i>""", parse_mode=types.ParseMode.HTML, reply_markup=Notify)
    else:
        await message.answer(f"""<b>Произошла ошибка!</b>
Ошибка: Вас нет в списке администраторов!""", parse_mode=types.ParseMode.HTML)

#Обработка запросов с клавиатуры об оповещениях.

@dp.callback_query_handler(text='AddNotify')
async def AddNotifys(message: types.Message):
    with open(database, "r", encoding= "utf-8") as f:
        content = json.load(f)
    if message.from_user.id in content["ids"]:
        await message.answer("Вы уже в рассылке")
    else:
        content["ids"].append(message.from_user.id)
        with open(database, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
        await message.answer("Вы успешно записаны в рассылку.")

@dp.callback_query_handler(text='RemNotify')
async def RemNotifys(message: types.Message):
    with open(database, "r", encoding= "utf-8") as f:
        content = json.load(f)
    if not message.from_user.id in content["ids"]:
        await message.answer("Вас нет в рассылке")
    else:
        index = content["ids"].index(message.from_user.id)
        content["ids"].pop(index)
        with open(database, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
            
        await message.answer("Вы успешно исключены из рассылки.")

#Админ-панель

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    print("admin: ", message.from_user.id)
    keyboard_markup = types.InlineKeyboardMarkup()
    AddTruth = types.InlineKeyboardButton('Добавить правду', callback_data= 'add_truth')
    AddAction = types.InlineKeyboardButton('Добавить действие', callback_data= 'add_action')
    ShoutOut = types.InlineKeyboardButton('Сделать объявление', callback_data= 'shoutout')
    Admin_kb = InlineKeyboardMarkup(row_width=2).add(AddTruth, AddAction, ShoutOut)
    if message.from_user.id in adminlist:
        await message.answer(f"Добро пожаловать, <b>id{message.from_user.id}</b>, выберите действие", reply_markup=Admin_kb, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(f"""<b>Произошла ошибка!</b>
Ошибка: Вас нет в списке администраторов!""", parse_mode=types.ParseMode.HTML)

#Ответы клавиатуры админ панели

@dp.callback_query_handler(text='add_truth') 
@dp.callback_query_handler(text='add_action') 
@dp.callback_query_handler(text='shoutout')
async def admin_kb_handler(query: types.CallbackQuery):
    answer_data = query.data
    print(answer_data)
    await query.answer(f'{answer_data!r}')
    async def admin_kb_result(message: types.Message):
        print(answer_data + 2)
        if answer_data == 'add_truth':
            result = AddingTruth() 
        elif answer_data == 'add_action':
            result = AddingAction()
        elif answer_data == 'shoutout':
            result = ShoutOuting()
        else:
            result = 'Ошибка'
            print("Ошибка")
        await dp.bot.send_message(message.from_user.id, result)


## Вывод правд/действий командами:


@dp.message_handler(commands=['truth', 't'])
async def cmd_truth(message: types.Message):
    print("truth: ", message.from_user.id)
    await message.reply(truthFX())

@dp.message_handler(commands=['action', 'a'])
async def cmd_action(message: types.Message):
    print("action: ", message.from_user.id)
    await message.reply(actionFX())

@dp.message_handler(commands=['random', 'r'])
async def cmd_random(message: types.Message): 
    print("random: ", message.from_user.id)
    await message.reply(randomFX())


## Inline вывод: (кнопки которые появляются при попытке отметить бота (@PD200_bot))


@dp.inline_handler()
async def inline_truth(inline_query: InlineQuery):
    Ttext = truthFX() #Генерируем текст и записываем его в переменную
    input_content = InputTextMessageContent(Ttext) #Сокращение
    result_id: str = hashlib.md5(Ttext.encode()).hexdigest() #декодировка
    Titem = InlineQueryResultArticle(
        id=result_id,
        title=f'Правда',
        input_message_content=input_content,
    )
    Atext = actionFX()
    input_content = InputTextMessageContent(Atext)
    result_id: str = hashlib.md5(Atext.encode()).hexdigest()
    Aitem = InlineQueryResultArticle(
        id=result_id,
        title=f'Действие',
        input_message_content=input_content,
    )
    Rtext = randomFX()
    input_content = InputTextMessageContent(Rtext)
    result_id: str = hashlib.md5(Rtext.encode()).hexdigest()
    Ritem = InlineQueryResultArticle(
        id=result_id,
        title=f'Случайно',
        input_message_content=input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[Titem, Aitem, Ritem], cache_time=1)

#Остальной мусор по приколу

@dp.message_handler(commands=['завидуй'])
async def zavist(message: types.Message):
    print("завидуй: ", message.from_user.id)
    await message.answer("Завидую...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
