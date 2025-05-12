age = int(input("How old are you? "))
if age >= 18:
    print("Congratulations! You are eligible to vote. Go make a difference!")
else: 
    difference = 18 - age
    print("Oops! You’re not eligible yet. But hey, only", difference, "more years to go!")
