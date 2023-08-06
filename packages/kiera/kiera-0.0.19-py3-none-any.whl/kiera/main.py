#!/usr/bin/env python3

import requests
import argparse
import random
import time
import tomli
import tomli_w
import os
import sys

from rich.columns import Columns
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS

from rich.console import Console
import uuid
import webbrowser
from rich import print as rich_print
import subprocess as sp
import colored
import getch
from importlib import metadata

console = Console()

SERVER_URL_DEV = 'http://localhost:5000'
SERVER_URL_PROD = 'https://jkl-backend-eu.herokuapp.com'
# SERVER_URL_PROD = 'https://prod.kiera.ai'

if len(sys.argv) > 1 and sys.argv[1] == '--dev':
    DEV_MODE = True
    SERVER_URL = SERVER_URL_DEV
    sys.argv.pop(1)
else:
    DEV_MODE = False
    SERVER_URL = SERVER_URL_PROD

TERMS_AND_SEVICES = 'https://www.kiera.ai/terms'
PRIVACY_POLICY = 'https://www.kiera.ai/privacypolicy'

if DEV_MODE:
    CLIENT_ID="6ba695f9a731779de3eb"
else:
    CLIENT_ID="8bf8ed3294d9901c9729"


STATE = str(random.random())

CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'kierarc')

def write_access_key_to_file(access_key):
    data = {'access_key': access_key}
    with open(API_KEYS_LOCATION, 'w') as f:
        f.write(tomli_w.dumps(data))

def read_access_key_from_file():
    if not os.path.exists(API_KEYS_LOCATION):
        return None

    with open(API_KEYS_LOCATION, 'r') as f:
        data = tomli.loads(f.read())

    if 'access_key' not in data:
        return None

    return data['access_key']

ACCESS_KEY = read_access_key_from_file()

def server_test():
    r = requests.get(f'{SERVER_URL}/test')
    print(r.text)

def hello():
    print("Hello, world!")
    print('Trying to connect to the server...')
    server_test()


def login():
    accepted_tns = terms_and_sevices_prompt()
    if not accepted_tns:
        return
    accepted_pp = privacy_policy_prompt()
    if not accepted_pp:
        return
    url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&state={STATE}'
    # print(url)
    print(f'\nIn case your browser doesn\'t open automatically, visit \n{url}')
    webbrowser.open(url)
    while True:  
        access_key = get_access_key_from_state(STATE)
        if access_key:
            print('Access key received')
            break
        time.sleep(0.5)

    write_access_key_to_file(access_key)
    sys.exit(0)



def terms_and_sevices_prompt():
    print()
    print(f'Terms and Services: {TERMS_AND_SEVICES}')
    print('Do you agree to the terms and services? [y/n]', end=' ')
    answer = input()
    if answer == 'y' or answer == 'yes':
        return True
    else:
        print('You must accept the terms and services to use Kiera')
        return False

def privacy_policy_prompt():
    print()
    print(f'Privacy Policy: {PRIVACY_POLICY}')
    print('Do you agree to the privacy policy? [y/n]', end=' ')
    answer = input()
    if answer == 'y' or answer == 'yes':
        return True
    else:
        print('You must accept the privacy policy to use Kiera')
        return False


def parse_args():
    parser = argparse.ArgumentParser(description='Kiera')
    parser.add_argument('command', nargs='?', choices=['login', ''])
    return parser.parse_args()

def send_command_feedback(data):
    r = requests.post(f'{SERVER_URL}/command_feedback', json=data)

def get_credits():
    r = requests.post(f'{SERVER_URL}/get_credits', json={'access_key': ACCESS_KEY})
    requests_this_month = r.json()['requests_this_month']
    max_requests_per_month = r.json()['max_requests_per_month']
    return requests_this_month, max_requests_per_month

def show_credits():
    print()
    with console.status('', spinner='growVertical'):
        requests_this_month, max_requests_per_month = get_credits()

    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.table import Table

    overall_progress = Progress()
    overall_task = overall_progress.add_task("Credits", total=max_requests_per_month)

    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(
            overall_progress, title="Used Credits", border_style="green", padding=(2, 2)
        ),
    )

    with Live(progress_table, refresh_per_second=10):
        overall_progress.update(overall_task, completed=requests_this_month)

    print(f'You have {requests_this_month} requests this month out of {max_requests_per_month} allowed requests per month')




    sys.exit(0)





def main():
    arg_login = None
    help_text = '''
Kiera is a command line interface for Kiera.ai

Usage:
    kiera <command>

Commands:
    login                                                Login to kiera.ai
    credit, credits                                      Show your credit balance
    --version, version                                   Show the version of kiera
    --help, help                                         Show this help message
            '''

    if len(sys.argv) > 1:
        if sys.argv[1] == 'login':
            login()

        if sys.argv[1] == 'credit' or sys.argv[1] == 'credits':
            show_credits()

        if sys.argv[1] == '--version' or sys.argv[1] == 'version':
            print(metadata.version('kiera'))
            sys.exit(0)

        if sys.argv[1] == '--help' or sys.argv[1] == 'help':
            print(help_text)
            sys.exit(0)



    if not ACCESS_KEY:
        print('No access key found, running login\n')
        login()

    if len(sys.argv) > 1:
        generate_completion()
    else:
        print(help_text)




def send_main2_request(data, attempt=0):
    r = requests.post(f'{SERVER_URL}/main2', json=data)
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        if attempt < 3:
            time.sleep(2**attempt - 1)
            return send_main2_request(data, attempt=attempt+1)
        else:
            print('Could not get command')
            exit(1)






def generate_completion():
    input_text = ' '.join(sys.argv[1:])

    session_uuid = str(uuid.uuid1())
    exit_code = None
    while True:
        with console.status('', spinner='aesthetic'):
            parsed = send_main2_request({'data': input_text, 'access_key': ACCESS_KEY, 'session_id': session_uuid})

        generated_command = parsed['data']


        def execute_command(command):
            exit_code = sp.call(command, shell=True)
            return exit_code


        if generated_command is None:
            print('Could not get command, please try again later.')
            exit(1)

        max_padding = 20
        if len(generated_command) < max_padding:
            generated_command_padded = (generated_command + ' ' * max_padding)[:max_padding]
        else:
            generated_command_padded = generated_command
        with Live(Panel(generated_command_padded, title='Kiera', subtitle='Execute (Y/n)?', expand=False, border_style='blue'), refresh_per_second=1) as live:

            execute_answer = getch.getch().strip()

            command_accepted = execute_answer in ['y', 'Y', '']
            if command_accepted:
                break

            send_command_feedback({'id': parsed['id'], 'accepted': command_accepted, 'access_key': ACCESS_KEY, 'exit_code': exit_code, 'session_id': session_uuid})
            live.update(None)

        if execute_answer in ['y', 'Y', '']:
            break

    print()
    exit_code = execute_command(generated_command)
    send_command_feedback({'id': parsed['id'], 'accepted': command_accepted, 'access_key': ACCESS_KEY, 'exit_code': exit_code, 'session_id': session_uuid})





def get_access_key_from_state(state):
    response = requests.post(f'{SERVER_URL}/get_access_key_from_state', json={'state': state})
    access_key = response.json()['jkl_access_key']
    return access_key



if __name__ == "__main__":
    main()
