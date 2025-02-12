import random

random_number = random.randint(1, 100)
print("I have picked a number between 1 and 100. Can you guess it?")

while True:
    user_number = int(input("Your guess: "))

    if user_number < random_number:
        print("Please, try a bigger number!")
    elif user_number > random_number:
        print("Please, try a smaller number!")
    else:
        print(f"Congratulations! You Win. Number is:{random_number}")
        break

print("Game Over")