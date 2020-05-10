def get_int(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except TypeError:
            print("That's not a number you dingus")
        except ValueError:
            print("That's not a number you dingus")
        finally:
            print("You will always see this line")


x = get_int("First Number is: ")
y = get_int("Second Number is: ")

try:
    print("{} is {} divided by {}".format(x/y, x, y))
except ZeroDivisionError:
    print("Can't divide by zero dingus")
else:
    print("Division performed successfully")
