from tqdm.notebook import tqdm_notebook as tqdm_
import time
import random
from termcolor import colored
from IPython import display
import gspread
from google.oauth2 import service_account
import numpy as np

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
    
def SaveFile():
    txt='''
    {
        "type": "service_account",
        "project_id": "woven-perigee-305411",
        "private_key_id": "976df23e4b85f294ea19eca819319d30078029f6",
        "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCp1tKsvxq+wY8W\\nIUSILajRvBXKRDKou8oj0rFAE5jHrfm3SZ1+eyIf4FbgSr+9YB/29VzP05qerJp9\\ntEG5eC/n0iqhtV2EBWftHifNml5I3EFkjPoGOVco7/PBhFspcZ/Y+zsZ5X+iXwI1\\nj/2n4HEeyl3Y4tA7nmYwTAopV9wsW3ftGT8uvsmsobwI+2R0jNrYjkcWAZXqHvgr\\nD73+z3ILIpzHXu7XIBMZ+3PXC90XQnLIM2WR8qvtC2xFRS2xr9y/U07N+yZW5An2\\nX+XawNXbC3Fnv9JIxoPPoifYivHhEruFKqTWQGrh8tMYHo8cQZAw+gVvbB2q+Nh8\\nWqAifzfHAgMBAAECggEAJqb4TU40xQMCEHRDx4Y0rH7UqrK4oMQULfDuW/nZxF/o\\nu/jp+fYF/yEsRGFen7e3rpmKpNWwk7oOcttKNe6PYH/pKeI/xSMB0uoQ/u7J1GUk\\nEMEwyafVGUD6xajcomL0kQokGjGryYU72HrLrKAcvngpwYllAJx8/zLfASe4uPM9\\nOE1ZHOEDv1T2K6j6HXtVZx9EgFcsUI5JuuohQR0W7igQFeA0pqK6B/0QPe0KjnTh\\nfUN3aNlYng2Us/IttGWTXwSOx/ulQPJ18E+zEY7cLm8L6Hy4prIbipm1LnvfRg2L\\nLhvEPnDSjHe1paQk+onQTU/3oXdDBeT6W/nhui2duQKBgQDVyxCRO0oc0sf0GZzZ\\n0kLnU6QYjOLpHL4U80a6CBWJ3CMC0YCctSKJ+YPJe3CkQb1geI72qnMweL9EIWZI\\nqJjfYQU2/aoTzggsHyRfrmWHgOTQy+cic1XEcAtgM26oebGtTB1/8fp/fdzS1OO8\\nMFWqd9tAqgfpXK5KxyTYNWjxGwKBgQDLXlr5MZqqVs8hd/USs6JHX9RFGINLvrFm\\nDhiwAsT1tFy+8yJmrkPCTgTVts+DIM96ZARD2guvtitTjkoA6sGezVb4YJbfwOdr\\nez11Bac6AgKckOtb3FPJtgoXQ+A7+6CKen+R6dVF1wLcfKnzIGUpywjitvVZ7S19\\nm986dcHqxQKBgBxMo+XFhlroX8Vk+okutuJuBOOnCoY24sZdKXiIh2lXNV8zIiYc\\nJ/VBjPtHlrJ3bTzu2GW4TEUXRqIbFbH6dzniWtFbpH64oAZPHP55VEEqg59Lzk2W\\nHL1C446ZYEV2zlkVITaFblYf7/IMchTABSbqdKBLoX53YS7Oy4a/EyQPAoGAE83W\\nchngg+H8Pbgex3lyvhyY4Tmn34JsaBHLWaiLYZn0xiuLGBC0TIGoet9Yid5yFesT\\nd0AOj0fgJDzg/AHgZQR+CaXuS0/PuWnA7FpmlIGJm5GJOeLUzfnKNcXIWk8ArTuM\\nnLr2p9xuTOZe7mwjLdS1ws4qSl2MZoT9UgYRojkCgYEAr3nYXJi5SwJEh8Cy7+UC\\nk92p4V45uzeEZxBaJkEST2kRQvO22GneR5yzP3Oo1YrzpkLHifI+hljJUErBdqeG\\n7OeXp4V9DoReSZYDk1rgd2g/3d4lXKSpq/OU5rjjLmnakXgSAXnNOYNyxD9Ga1XR\\n5uAmPm8HioxFvpKkWy4EzvM=\\n-----END PRIVATE KEY-----\\n",
        "client_email": "srv-name@woven-perigee-305411.iam.gserviceaccount.com",
        "client_id": "112155977488362377206",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/srv-name%40woven-perigee-305411.iam.gserviceaccount.com"
        }
    '''
    f = open('cred.json', 'w')
    f.write(txt)
    f.close()


def getData(gc):    

    sh  = gc.open_by_url('https://docs.google.com/spreadsheets/d/1VsLFpp9y7eSCC7BkDC2pTRsFDN4AqsfTD-aq1e7Gw8k/edit?usp=sharing').sheet1

    # get_all_values gives a list of rows.
    rows = sh.get_all_values()

    # Convert to a DataFrame and render.
    import pandas as pd
    df = pd.DataFrame.from_records(rows)
    return df

def SendData(dataframe, gc):
    worksheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1VsLFpp9y7eSCC7BkDC2pTRsFDN4AqsfTD-aq1e7Gw8k/edit?usp=sharing').sheet1

    idx = dataframe.shape[0]-1
    cell_list = worksheet.range(f'A{idx+1}:D{idx+1}')
    for i, cell in enumerate(cell_list):
        cell.value = dataframe.iloc[idx, i]

    worksheet.update_cells(cell_list)

def Start():
    SaveFile()
    SERVICE_ACCOUNT_FILE = 'cred.json'
    gc = gspread.service_account(SERVICE_ACCOUNT_FILE)
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
    probability = [.5, .15, .05, .15, .1, .05, .3, .5, .5, .5, .3, .1, .05]
    current_variant = np.array([np.random.choice([0,1], 1, p=[1-p, p]) for p in probability]).reshape(-1)
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

    df = getData(gc)
    from datetime import date
    today = date.today()
    df = df.append([[str(date.today()), mail, phone, "• "+ "\n• ".join(bonuses)]])
    SendData(df, gc)

    print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
    print('Скоро мы вам позвоним :)')