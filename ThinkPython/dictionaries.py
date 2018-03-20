def words_dictionary ():
    count = 0
    d = dict()

    words_file = open(".\ThinkPython\words.txt")

    for word in words_file:
        d[word.strip().lower()] = count
        count += 1

    return d

# flag = "account" in dic
# print (flag)

def histogram (word):
    d = dict()
    for char in word:
        d[char] = 1 + d.get(char, 0)
    return d

def print_hist(h):
    keys = list(h.keys())
    keys.sort()

    for c in keys:
        print (c, h[c])

h = histogram("parrot")
print_hist(h)

def reverse_lookup(d, v):
    keys = []
    for k in d:
        if d[k] == v:
            keys.append(k)

    return keys

def invert_dict(d):
    inverse = dict()
    for key in d:
        val = d[key]

        if val not in inverse:
            inverse[val] = [key]
        else:
            inverse[val].append(key)
    return inverse

#print (invert_dict(h))

known = {0:0, 1:1}

def fibonacci(n):
    if n in known:
        return known[n]

    res = fibonacci(n-1) + fibonacci(n-2)
    known[n] = res
    return res

def fibo_org(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return (fibo_org(n-1) + fibo_org(n-2))

import time

start = time.time()
fibo1 = fibo_org(20)
end = time.time()
print ("f1 time: " + str(fibo1) + "     " + str(end-start))

start = time.time()
fibo2 = fibonacci(20)
end = time.time()
print ("f2 time: " + str(fibo2) + "     " + str(end-start))

def has_duplicates (list1):
    l = list1[:]
    l.sort()
    for i in range(len(l)-1):
        if l[i] == l[i+1]:
            return True
    return False

# print (has_duplicates([1,2,3, 4, 5, 6,7, -1, 1, 8]))
# print (has_duplicates([1,2,3, 4, 5, 6,7, -1]))

def has_duplicates_dict(l):
    s = set(l)

    return len(l) != len(s)

    # for key in l:
    #     if key not in d:
    #         d[key] = ""
    #     else:
    #         return True
    # return False

# print (has_duplicates_dict([1,2,3, 4, 5, 6,7, -1, 1, 8]))
# print (has_duplicates_dict([1,2,3, 4, 5, 6,7, -1]))

def rotate_pairs(wordlist):
    d = words_dictionary()
