import random as rd
number_to_guess = rd.randint(1, 100)
counter = 1
while(int(input("Guess a number: ")) != number_to_guess):
    counter += 1
    if counter == 11:
        break
    continue
if(counter == 1):   
    print("You guess in one go!!! You got super powers man!")
elif(counter == 11):
    print("Game over :( better luck next time you got it champ!")
else:
    print(f"Congrats you guess in {counter} attempts")