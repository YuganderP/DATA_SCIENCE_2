from itertools import count

from questions import quizz_questions as qq
import random
questions=[]
for i in qq.items():
    questions.append(i)

def quizz_main(count):
    score=0
    quizz_questions=random.sample(questions,count)
    while(count):
        question,answer=quizz_questions[count-1]
        print(question)
        ans=input("enter the answer").lower().strip()
        if(answer==ans):
            score+=1
            print(f"Nice You got it right!!!")
            print(f"your score is {score}")
            count -= 1
        else:
            print(f"oops!!!!, you got it wrong and the correct answer was {answer}")
            print(f'The correct answer was {answer}')
            print(f"your score is {score}")
            count-=1
    else:
        print("your quizz is complete ")




print("Welcome to the quizz")
a=0
try:
    a=int(input("How many questions would you like?"))
except ValueError:
    print("You have not entered a valid number please restart the application")

if a>0:
    quizz_main(a)









