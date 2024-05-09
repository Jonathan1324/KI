import student

def test():

    TestMessage = "Hello"

    message = student.main(TestMessage)

    responses = ["Hi", "Hello"]

    for response in responses:
        if message == response:
            successFile = open("success.py", "w")
            successFile.write(open("student.py", "r").read())
            return "success"
        
    return "fail"

print(test())