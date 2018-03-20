# A function object is a value you can assign to a variable or pass as an argument

def do_four(f, value):
    do_twice(f, value)
    do_twice(f, value)

def do_twice(f, value):
    f(value)
    f(value)

def print_it(value):
    print("value is " + str(value))

#do_twice(print_it, "spam")
#do_four(print_it, "Fantastic4")

def ack(m, n):
    if (m == 0):
        return n+1

    if (n == 0):
        return ack(m-1, 1)

    return ack(m-1, ack(m, n-1))


# print("\n" + str(ack(3,6)))

def first(word):
    return word[0]

def last(word):
    return word[-1]

def middle(word):
    return word[1:-1]

def is_palindrome(word):
    # if (len(word) <=1):
    #     return True
    # if (first(word) != last(word)):
    #     return False
    # return is_palindrome(middle(word))
    return (word == word[::-1])

print (is_palindrome('allen'))
print (is_palindrome('bob'))
print (is_palindrome('otto'))
print (is_palindrome('redivider'))


def print_n(s, n):
    while n!=0:
        print(s)
        n -= 1

def square_root(a):
    x = a/10
    epsilon = 0.0000001


    while True:
        print (x)
        y = (x + a/x) / 2
        if abs(y-x) < epsilon:
            return y
        x = y

# print_it(square_root(100000))
# print_it(square_root(1))
# print_it(square_root(81))

def eval_loop():
    while True:
        user_input = input("Enter an expression")
        if user_input == "done":
            break
        print(eval(user_input))

#eval_loop()
