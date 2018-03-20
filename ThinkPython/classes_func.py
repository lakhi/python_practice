class Time:
    def __init__(self, h=0, m=0, s=0):
        self.h = h
        self.m = m
        self.s = s

    def __str__(self):
        time = "hrs: " + str(self.h) + "   mins: " + str(self.m) + \
                "   secs: " + str(self.s)
        return time

# def is_after (t1, t2):
#     return (t1.h * 60 * 60 + t1.)

def int_to_time (n):
    t = Time()
    minutes, seconds = divmod(n, 60)
    t.h, t.m = divmod(minutes, 60)
    t.s = seconds
    return t

def time_to_int (t):
    seconds = t.h * 60 * 60 + t.m * 60 + t.s
    return seconds

# print (int_to_time(360))
# print (int_to_time(5))
# print (int_to_time(36063))

def mul_time(time, num):
    product = time_to_int(time) * num
    return int_to_time(product)


t1 = Time(2, 0, 0)
t2 = Time(0, 0, 6)
t3 = Time(3, 47, 59)

# print (mul_time(t1, 2))
# print (mul_time(t2, 10))
# print (mul_time(t3, 3))


class Kangaroo:
    def __init__(self, contents=[]):
        self.pouch_contents = list(contents)

    def __str__(self):
        kangaroo = [object.__str__(self) + ' with pouch contents']
        for obj in self.pouch_contents:
            s = '   ' + object.__str__(obj)
            kangaroo.append(s)
        return ('\n'.join(kangaroo))

    def put_in_pouch(self, item):
        self.pouch_contents.append(item)

kanga = Kangaroo()
roo = Kangaroo()
print (kanga)
print (roo)

kanga.put_in_pouch('wallet')
kanga.put_in_pouch('car keys')
kanga.put_in_pouch(roo)

print (kanga)
print (roo)
# kanga = Kangaroo()
# roo = Kangaroo()
#
# roo.put_in_pouch("roo")
# kanga.put_in_pouch(roo)
# kanga.put_in_pouch({})

print (roo.pouch_contents)
print (kanga.pouch_contents)

print (roo.pouch_contents == kanga.pouch_contents)
