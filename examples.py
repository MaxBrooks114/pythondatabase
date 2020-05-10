x = 8 -5
# y = x / 0

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)
try:
    print(factorial(900))
except (RecursionError, ZeroDivisionError, OverflowError):
    print("This program cannot handle factorials that large")
# except ZeroDivisionError:
#     print("Can't divide by zero dingus")

print("program terminating")
