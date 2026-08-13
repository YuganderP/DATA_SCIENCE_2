import random

def guessingGame():
    gen_number = random.randint(1, 100)
    print('Guess number between 1 and 100')
    num=int(input("please enter your guess: "))
    if(num==gen_number):
        print("you guessed the number")
    else:
        print("you guessed it  wrong")
        print("the number was ",gen_number)

guessingGame()