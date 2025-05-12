special_chars = ["!", "@", "#", "$", "%", "^", "&", "*" ]
errors = []

password = input("Enter password: ")

length = len(password)
upC = 0
lowC = 0
digC = 0
sC = 0
for i in password:
    if i.isupper():
        upC += 1
    if i.islower():
        lowC += 1
    if i.isdigit():
        digC += 1
    if i in special_chars:
        sC += 1

if length >= 8 and upC >= 1 and lowC >= 1 and digC >= 1 and sC >= 1:
    print("Your password is strong! 💪")
else:
    if length < 8:
        errors.append("doesnt meet length")
    if upC < 1:
        errors.append("needs at least one Upper Character")
    if lowC < 1:
        errors.append("needs at least one lower case character")
    if digC < 1:
        errors.append("needs at least one digit")
    if sC < 1:
        errors.append("needs at least one special character")
    for i in errors:
        if len(errors) > 1:
            print(i + " and ", end="")
        elif len(errors) == 1:
            print(i)