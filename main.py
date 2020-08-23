import vk_api
import csv
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

try:
    from data import *
    login
    password
except:
    login, password = input('Введите свой номер телефона '), input('Введите свой пароль ')

try:
    from data import *
    count_users_analis
except:
    count_users_analis = int(input('Введи число пользователей до которго будет анализироватся в тыс '))

try:
    from data import *
    goup_id
except:
    group_id = input('Введите id группы (это то что идёт после /) vk.com/')

date = dt.date(2019, 12, 31)
date_list = []
age_list = []
for i in range(1, 120):
    age_list.append(0)
for i in range(366):
    date_list.append(0)

full_date = 0
part_date = 0
hiden_date = 0
users_numbers = 0

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

vk = vk_session.get_api()

with open('vk_data.csv', 'w') as new_file:
    # csv
    for i in range(0, count_users_analis):
        vk_group = vk.groups.getMembers(group_id=group_id, offset=1000 * i, fields='bdate')
        for k in range(0, 1000):
            try:
                user = vk_group['items'][k]
            except:
                break
            try:
                user_bdate = user['bdate'].split('.')
                if len(user_bdate) == 2:
                    part_date += 1
                elif len(user_bdate) == 3:
                    full_date += 1
                    # print(2020 - int(user_bdate[2]))
                    age_list[(2020 - int(user_bdate[2]))] += 1
                user_date = dt.date(2020, int(user_bdate[1]), int(user_bdate[0]))
                user_num_day = int((str(user_date - date)).split(' ')[0])
                date_list[user_num_day] += 1
            except:
                hiden_date += 1
            new_file.write('\n')
            users_numbers += 1


print('Всего {} человек из них {} скрыли дату рождения, {} частично показали и {} полностью показали'.format(users_numbers, hiden_date, part_date, full_date))
hiden_percent = (hiden_date*100)//users_numbers
part_percent = (part_date*100)//users_numbers
full_percent = (full_date*100)//users_numbers
print('{}% Скрыло, {}% Частично, {}% Полностью'.format(hiden_percent, part_percent, full_percent))
# print(date_list)
# print(age_list)


def draw_gist(y1, y2):
    """Draw Histogram"""
    x1 = np.arange(1, len(y1) + 1)
    x2 = np.arange(1, len(y2) + 1)
    fig, ax = plt.subplots(2, 1)
    ax[0].bar(x1, y1)
    ax[1].bar(x2, y2)
    ax[0].set_title('Распределение дат рождений по дням года')
    ax[1].set_title('Распределение возрастов людей')

    plt.show()


draw_gist(y1=np.array(date_list), y2=np.array(age_list))
# draw_gist(y=np.array(date_list))
# draw_gist(y=np.array(age_list))