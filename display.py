from colorama import Fore, Back, Style
from sys import platform
from os import system
from time import sleep


def clear():
    if platform == 'win32':
        system('cls')
    elif platform == 'darwin':
        system('printf \'\\33c\\e[3J\'')
    else:
        system('clear')


def print_info(text: str):
    print(f'{Fore.BLUE}{Back.BLACK}{text}{Style.RESET_ALL}')


def print_input(text: str):
    result = input(f'{Fore.GREEN}{Back.BLACK}{text}{Fore.MAGENTA}')
    print(Style.RESET_ALL)

    return result


def print_error(text: str, abrupt = False):
    print(f'\n{Fore.RED}{Back.BLACK}{text}{Style.RESET_ALL}')
    sleep(2)
    if abrupt == False:
        print_input('Hit ENTER/RETURN to continue...')


def print_job(title: str, url: str):
    print(f'{Fore.RED}{"-"*30} {Fore.GREEN}{Back.BLACK}{title} {Fore.RED}{"-"*30}{Style.RESET_ALL}')
    print(f'{Fore.BLUE}{Back.BLACK}{url}{Style.RESET_ALL}')
