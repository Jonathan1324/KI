import os
import random
import string

def getCode():
    code = f"""
import random
import string

def main(message):
    answer = ""
"""
    
    for i in range(random.randint(1, 100)):
        code += f"""
    random_strings = {[''.join(random.choices(string.ascii_letters, k=random.randint(0, 10))) for _ in range(random.randint(1, 100))]}
    for random_message in random_strings:
        if message == random_message:
            answer = "Hello"
            break
"""
    
    code += f"""

    return answer
"""

    return code


def create():
    student = open("student.py", "w")

    code = getCode()

    student.write(code)

def main():
    create()

    os.system("teacher.py")

for i in range(5000):
    main()