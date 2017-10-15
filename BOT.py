import time, vk_api, requests, gtts, datetime, json


def say():
    printmsg()
    try:
        if item['attachments']:
            print('Имеется приложение, невозможно проговорить')
    except KeyError:
        now_time = datetime.datetime.now()
        ogg_name = now_time.strftime("%d%m%Y%I%M%S") + ".ogg"
        try:
            tts = gtts.gTTS(text=command[1], lang='ru')
            tts.save(ogg_name)
            msg = upload_file(ogg_name)
            send_msg(item['user_id'], msg)
        except:
            print('Cannot speak it due to some reason')


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def upload_file(path):
    data = {'file': (path, open(path, 'rb'))}
    upload_url = vk.method('docs.getMessagesUploadServer', {'type': 'audio_message'})['upload_url']
    response = requests.post(upload_url, files=data)
    result = json.loads(response.text)['file']
    msg = vk.method('docs.save', {'file': result})[0]
    return msg


def send_msg(user_id, msg):
    attach = 'doc%s_%s' % (msg['owner_id'], msg['id'])
    vk.method('messages.send', {'user_id': user_id, 'attachment': attach})


def printmsg():
    try:
        if item['attachments']:
            a = item['attachments']
            attachmentdict = a[0]
            if item['body'] == '':
                if attachmentdict['type'] == 'photo':
                    print(item['user_id'], ':', 'Изображение')
                elif attachmentdict['type'] == 'audio':
                    print(item['user_id'], ':', 'Музыка')
                elif attachmentdict['type'] == 'doc':
                    print(item['user_id'], ':', 'Документ (возможно голосовое сообщение)')
            else:
                if attachmentdict['type'] == 'photo':
                    print(item['user_id'], ':', item['body'], '+', 'Изображение')
                elif attachmentdict['type'] == 'audio':
                    print(item['user_id'], ':', item['body'], '+', 'Музыка')
                elif attachmentdict['type'] == 'doc':
                    print(item['user_id'], ':', item['body'], '+', 'Документ (возможно голосовое сообщение)')
    except KeyError:
        print(item['user_id'], ':', item['body'])
    except:
        print('Cannot send message due to some reason')


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


##Код аутентификации
login, password = '+79151514603', 'Bezdelnickru2001'
# login, password = '89112351734', 'Bezdelnickru'
vk = vk_api.VkApi(login, password, captcha_handler=captcha_handler, auth_handler=auth_handler)
vk.auth()
ignore = False
afkmode = False
print('Do you want to turn on AFK mode? y/n')
w = input()
if w == 'y' or w == 'Y':
    afkmode = True
if afkmode:
    print('Do you want ignore spam people? y/n')
    w = input()
    if w == 'y' or w == 'Y':
        ignore = True
attachmentdict = {}
idsent = []
values = {'out': 0, 'count': 100, 'time_offset': 60}
print('Bot is running, all messages will appear here.')

while True:
    time.sleep(1)
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        if afkmode:
            if True == ignore and item['user_id'] in idsent:
                print(item['user_id'], 'проигнорирован, пишет более 1 раза')
                printmsg()
            elif ignore == False and item['user_id'] in idsent:
                write_msg(item['user_id'],
                          'Не спамь пожалуйста, тебе все равно никто кроме меня не ответит. Подожди немного.')
                printmsg()
            else:
                write_msg(item['user_id'],
                          'Привет, к сожалению, владелец этой страницы отошел. Попробуй написать позже.')
                idsent.append(item['user_id'])
                printmsg()
        else:
            try:  # вот тут будут все команды
                command = list(item['body'].split(maxsplit=1))
                if command[0].lower() == 'скажи':
                    say()
            except IndexError:
                print('Кажется, отправлено пустое сообщение')
