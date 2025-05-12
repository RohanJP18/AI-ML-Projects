# factorial = 5 = 5* 4 * 3 * 2 * 1
user_number = int(input("Enter a number: "))
factorial = 1;
user_number_loop = user_number
for i in range(user_number_loop):
    factorial = user_number_loop * factorial
    user_number_loop = user_number_loop - 1 

print(f"the factorial of {user_number} is {factorial}")

