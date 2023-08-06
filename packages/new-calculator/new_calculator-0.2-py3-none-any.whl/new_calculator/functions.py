import click
import random
from colorama import Fore, Back, Style

def add_number(a, b): 
    return a + b

def mul_number(a, b): 
    return a * b

def div_number(a, b): 
    return a / b

def sub_number(a, b): 
    return a - b


@click.command()
@click.argument("mode", nargs=1, type=click.Choice(['add', 'sub', 'div', 'mul']))
@click.option('-n1', '--num1', nargs=1, type=int, default=0, help='The First Number')
@click.option('-n2', '--num2', nargs=1, type=int, default=0, help='The Second Number')
def func(mode, num1:int, num2:int):
    if mode == 'add': 
        result = add_number(num1, num2)
        print(Fore.BLUE + f"Add Result: {result}")

    elif mode == 'sub':
        result = sub_number(num1, num2)
        print(Fore.BLUE + f"Sub Result: {result}")

    elif mode == 'mul':
        result = mul_number(num1, num2)
        print(Fore.BLUE + f"Mul Result: {result}")

    else:
        if num2 == 0: 
            print(Back.RED + Fore.WHITE, "Not num2 is 0")
        else: 
            result = div_number(num1, num2)
            print(Fore.BLUE + f"Div Result: {result}")
    

if __name__ == '__main__':
    func()