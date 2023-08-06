import requests
from tqdm.notebook import tqdm_notebook as tqdm_
import time

from IPython import display

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Start():
    url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
    res='/numbers'    
    res_save= '/save'
    res = requests.get(f'{url}{res}')

    presents = ['5 zoom консультаций',
                '10 zoom консультаций',
                '20 zoom консультаций',
                '1 стажировка (3 месяца)',
                '2 стажировки (6 месяцев)',
                '4 стажировки (12 месяцев)',
                'Курс по трейдингу (6 занятий) + стажировка',
                'Курс по обработке данных и алгоритмам (14 занятий)',
                'Курс по PyTorch (10 занятий)',
                'Выкуп стоимости обучения',
                'Скидка 5.000 рублей',
                'Скидка 10.000 рублей',
                'Скидка 20.000 рублей',]
    cost = [9500, 14900, 29800, 14900, 24900, 39900, 39900, 39900, 39900, 39900, 5000, 10000, 20000]    
    current_variant =  [int(value)  for value in res.json().values()]
    bonuses = []
    num_bonus = 1
    for i, elem in enumerate(current_variant):
        if elem:          
          for _ in tqdm_(range(60), desc=f'Выбор бонуса №{num_bonus}', ncols=500):
              time.sleep(0.01)
          num_bonus+=1
          current_present = f'{bcolors.OKBLUE}Бонус:{bcolors.ENDC} {presents[i]} ({cost[i]} руб.)'
          print(current_present)
          time.sleep(1)
          display.clear_output(wait=True)
          bonuses.append(f'{presents[i]} ({cost[i]} руб)')
          print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
          print(f'Ваш список бонусов:{bcolors.ENDC}')
          for b in bonuses:    
              print(f'- {b}')
    print()
    print()
    mail = input('Укажите ваш email: ')
    phone = input('Укажите ваш телефон: ')

    print()
    print()

    res = requests.post(f'{url}{res_save}', params={'email': mail, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})

    if res.status_code==200:
      print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
      print('Скоро мы вам позвоним :)')
    else:
      print(f'{bcolors.FAIL}Ошибка сервера! Обратитесь, пожалуйста, к менеджерам УИИ')