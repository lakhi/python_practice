def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return "Zero Div"

a = 1
b = "2"
print(int(2.5))
print(a + int(b))

print("Division....................")
print(divide(1, int(divide(a,int(b)))))
