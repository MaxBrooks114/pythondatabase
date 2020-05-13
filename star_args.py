def print_backwards(*args, **kwargs):
    for word in args[::-1]:
        print(word[::-1], **kwargs)

print_backwards("hello", "dude", "how", "are", "you", end='\n')