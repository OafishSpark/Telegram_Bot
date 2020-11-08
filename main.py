import telebot

tokenfile = open("tokenfile.txt", "r")

TOKEN = tokenfile.readline()

bot = telebot.TeleBot (TOKEN)

@bot.message_handler (commands = ['start'])
def start_handler (message):

# здесь создаём несколько базовых кнопок (создатель не успел разобраться, как сделать другие)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = telebot.types.KeyboardButton('/all')
    itembtn2 = telebot.types.KeyboardButton('/help')
    markup.add(itembtn1, itembtn2)
    bot.send_message (message.from_user.id, f"Привет, {message.from_user.first_name}! Нажми на /help чтобы узнать, на что способно моё творение!", reply_markup = markup)

# для нового пользователя создаётся документ, в котором будет храниться вся информация о задачах 

    tdlist = open (f'todolist_{message.from_user.id}.txt', 'a')
    tdlist.close ()

# оно так страшно выглядит, потому что создатель не разобрался, как избежать ошибки кодировки при чтении из файла

@bot.message_handler (commands = ['help'])
def help_handler (message):
    bot.send_message (message.from_user.id, "0) Для того чтобы бот нормально работал нужно всё вводить строго, как написано ниже, ибо защиту от неаккуратного пользователя создатель сделать не успел. 1) </start> для инициализации пользователя и создании для него файла, в котором будут храниться нужные данные. 2) </help>, как не трудно догадаться, для того, чтобы напомнить Вам, как правильно пользоваться этим ботом. 3) <new_item {описание задачи}> добавляет новую задачу в конец списка. !!! сначала нужно написать команду ниже, а потом отсылать фото. 4) </add_photo {номер задачи}> определяет номер задачи, к которой прикрепляется фото; сначала пишете эту команду, а затем присылаете фото. 5) </all> показывает все задачи с картинками (если имеются) на текущий момент. 6) </delete {номер задачи}> удаляет задачу с выбранным номером, а так же все картинки((( Cоздатель очень надеется, что остальное бот проигнорирует")

@bot.message_handler (commands = ['new_item'])
def newitem_handler (message):
    bot.send_message (message.from_user.id, 'Задание успешно добавлено!  (наверное)')
    tdlist = open (f'todolist_{message.from_user.id}.txt','a')
    mes = message.text
    mes = mes.replace('/new_item ', '')
    tdlist.write(mes + '\n')
    tdlist.close ()

@bot.message_handler (commands = ['all'])
def all_handler (message):
    tdlist = open (f'todolist_{message.from_user.id}.txt','r')

# задачи не нумеруются в фаиле; создателю показалось достаточным каждую задачу писать на новой строке, а id фото одлеять от содержимого задачи с помощью знака "----"

    todolist = tdlist.read ().split ('\n')
    for i in range (1, len (todolist)):
        task = todolist[i - 1].split ('----')
        mes = f'{i}' + ' ' + task[0] + '\n'
        bot.send_message (message.from_user.id, mes)
        if len (task) > 1:
            for i in range (1,len(task)):
                photo = task [i]
                bot.send_photo (message.from_user.id, photo)   
    tdlist.close ()

@bot.message_handler (commands = ['delete'])
def delete_handler (message):

    mes = message.text
    mes = mes.split ()[1]
    num = int(mes)

    bot.send_message (message.from_user.id, f'Задание {num} уничтожено!')

    tdlist = open (f'todolist_{message.from_user.id}.txt', 'r')
    todolist = tdlist.read ().split ('\n')
    todolist.pop (num - 1)

    tdlist.close ()

    tdlist = open (f'todolist_{message.from_user.id}.txt', 'w')
    for i in range (1, len (todolist)):
        tdlist.write (todolist[i - 1] + '\n')
    tdlist.close ()

# я не понял, как в телеграме одновременно отправлять фото и текст, результатом чего служит небольшое извращение ниже

# первая функция нужна для того, чтобы понять, к какой задаче мы прикрепляем фотографию 

@bot.message_handler (commands = ['add_photo'])
def add_photo_handler(message):
    mes = message.text
    mes = mes.split ()[1]
    global taskforphotonum
    taskforphotonum = int (mes)

# мы сохраняем не фото, а только лишь его id, и по нему же потом при выполнении /all будем находить фотографию

@bot.message_handler (content_types = ['photo'])
def makingphoto_handler (message):

    photo = message.photo[-1]
    file_id = photo.file_id

    tdlist = open (f'todolist_{message.from_user.id}.txt', 'r')
    todolist = tdlist.read ().split ('\n')
    tdlist.close ()

    tdlist = open (f'todolist_{message.from_user.id}.txt', 'w')
    for i in range (1, len (todolist)):
        if i == taskforphotonum:
            tdlist.write(todolist[i - 1] + f'----{file_id}' +'\n')
        else:   
            tdlist.write (todolist[i - 1] + '\n')
    tdlist.close ()




bot.polling ()
