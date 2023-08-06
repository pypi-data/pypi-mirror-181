print("Hello....")
number_one = int(input("your first number: "))
number_two = int(input("your second number: "))

def add_num(a,b):
    return a + b
def div_num(a, b):
    return a / b
def multi_num(a,b):
    return a * b
def sub_num(a,b):
    return a - b


operation = input("{+} for add two nmber\n{/} for dividing two number\n{*} for multiple two number\n{-} for subtraction two number\nyour operation please: ")

if operation == "+":
    print(add_num(number_one, number_two))
elif operation == "-":
    print(sub_num(number_one, number_two))
elif operation == "*":
    print(multi_num(number_one, number_two))
elif operation == "/":
    print(div_num(number_one, number_two))