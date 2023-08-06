import requests
from tqdm.notebook import tqdm_notebook as tqdm_
import time

import ipywidgets as widgets
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

def work(progress):
  print('Выбор бонуса')
  total = 100
  for i in range(total):
      time.sleep(0.05)
      progress.value = float(i+1)/total

btn_ok = widgets.Button(description="Забронировать", button_style='success')
btn_no = widgets.Button(description="Заново", button_style='danger')
buttons = widgets.HBox([btn_ok, btn_no])

txt_name = widgets.Text(
    value='',
    placeholder='Имя',
    description='Имя:',
    disabled=False
)

txt_mail = widgets.Text(
    value='',
    placeholder='mail',
    description='mail:',
    disabled=False
)

txt_phone = widgets.Text(
    value='',
    placeholder='phone',
    description='phone:',
    disabled=False
)

btn_send = widgets.Button(description="Отправить", icon='send', button_style='info')

texts = widgets.VBox([txt_name, txt_mail, txt_phone, btn_send])
bonuses = []
current_cost = 0

def ok_onclick(b):
  display.display(texts)

def send_onclick(b):
  display.clear_output(wait=True)
  print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
  print(f'Ваш список бонусов:{bcolors.ENDC}')
  for b in bonuses:    
      print(f'- {b}')
  print()
  print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
  res_save= '/save'
  url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
  name = txt_name.value
  mail = txt_mail.value
  phone = txt_phone.value
  res = requests.post(f'{url}{res_save}', params={'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})

  if res.status_code==200:    
    print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
    print('Скоро мы вам позвоним :)')
  else:
    print(f'{bcolors.FAIL}Ошибка сервера! Обратитесь, пожалуйста, к менеджерам УИИ')

def Start(b):
    global bonuses, current_cost
    display.clear_output(wait=True)
    url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
    res='/numbers'    
    res_save= '/save'
    res = requests.get(f'{url}{res}')
    progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
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
    print(f'{bcolors.BOLD}Готовимся выбирать бонусы...{bcolors.ENDC}')
    time.sleep(1)
    current_cost = 0
    for i, elem in enumerate(current_variant):
        if elem:          
          #for _ in tqdm_(range(60), desc=f'Выбор бонуса №{num_bonus}', ncols=500):
          #    time.sleep(0.05)
          display.display(progress)
          work(progress)
          num_bonus+=1
          current_cost += cost[i]
          current_present = f'{bcolors.OKBLUE}Бонус:{bcolors.ENDC} {presents[i]} ({cost[i]} руб.)'
          print(current_present)
          time.sleep(1)
          display.clear_output(wait=True)
          bonuses.append(f'{presents[i]} ({cost[i]} руб)')
          print(f'{bcolors.BOLD}Готовимся выбирать бонусы...{bcolors.ENDC}')
          print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
          print(f'Ваш список бонусов:{bcolors.ENDC}')
          for b in bonuses:    
              print(f'- {b}')
    print()
    print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
    print()
    print()
    print(f'Вам нравится такой бонус?')
    
    display.display(buttons)

btn_no.on_click(Start)
btn_ok.on_click(ok_onclick)
btn_send.on_click(send_onclick)