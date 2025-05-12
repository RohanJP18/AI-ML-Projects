user_ting = input("Enter a word: ")
if user_ting == user_ting[::-1]:
    print(f"congrats, {user_ting} is a palindrome!")
else:
    print(f"sorry, {user_ting} is not a palindrome!")