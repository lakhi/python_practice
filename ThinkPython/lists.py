def cum_sum (list):
    cum_sum = []
    sum = 0
    for n in list:
        sum += n
        cum_sum.append(sum)
    return cum_sum

#print(cum_sum([1, 2, 3]))

def middle (list):
    return list[1:-1]

def chop(list):
    list.remove(1)
    list.remove(6)
    return None

l = [13, 24, 35, 54, 5, 16]
#print("l became chop(l) after " + str(chop(l)) + " \n" + str(l))

orig = l[:]
l.sort()

#print(orig, l)

def equals(l1, l2):
    i = 0
    while (i < len(l1)):
        if (l1[i] != l2[i]):
            return False
        i += 1
    return True

def anagram(word1, word2):
    if (len(word1) != len(word2)):
        return False

    l1 = list(word1)
    l2 = list(word2)

    l1.sort()
    l2.sort()

    if (equals(l1, l2)):
        return True

    return False

def anagram2(word1, word2):
    # return (str(list(word1).sort()) == str(list(word2).sort()))
    return (sorted(word1) == sorted(word2))


print(anagram2("more", "rome"))
print(anagram2("more", "romeo"))
print(anagram2("more", "romi"))


# def has_duplicates (list):
#     i = 0
#     while (i <= len(list)-2):
#         j = i+1
#         while (j <= len(list)-1):
#             if (list[i] == list[j]):
#                 return True
#             j += 1
#         i += 1
#     return False

import random

def has_duplicates (list):
    l = list[:]
    l.sort()
    for i in range(len(l)-1):
        if l[i] == l[i+1]:
            return True
    return False

def remove_duplicates (list):
    l = list[:]
    l.sort()
    unique = l[:]
    for i in range(len(l)-1):
        if l[i] == l[i+1]:
            print (i, unique)
            del unique[i]
            del unique[i]

    return unique

# print(remove_duplicates([1, 2, 3, 3, 4, 5]))
# print(has_duplicates([12, 2, 13, 3, 4, 5]))

import time

def listbuild1():
    words_file = open(".\ThinkPython\words.txt")
    list_words = []
    for word in words_file:
        list_words.append(word.strip())
    return list_words

def listbuild2():
    words_file = open(".\ThinkPython\words.txt")
    list = []
    for word in words_file:
        list = list + [word.strip()]
    return list

# start = time.time()
# l1 = listbuild1()
# end = time.time()
# print ("l1 time: " + str(end-start))
#
# start = time.time()
# l2 = listbuild2()
# end = time.time()
# print ("l2 time: " + str(end-start))

""" Binary Search! """
def bisect (list, value):
    i = 0
    j = len(list)

    if (len(list) >= 1):
        middle = int((j-i)/2)
        if (list[middle] == value):
            return middle
        elif (list[middle] > value):
            return bisect(list[:middle], value)
        else:
            return bisect(list[middle:], value) + middle
    else:
        return None

# def bisect_iter (list, value):
#     copy = list[:]
#     length = len(list)
#     start = list[0]
#     end = list[length - 1]
#
#     while ():


# print(bisect([10, 20, 30], 20))
# print(bisect([0, 10, 20, 30], 20))
# print(bisect([-10,1, 2, 3, 4, 10, 20, 30], 30))
# print(bisect([-10,1, 2, 3, 4, 10, 22, 29, 30], 22))
# print(bisect([10, 20, 30], 25))

# def reverse_pair ():
#     words = listbuild1()
#     i = 0
#     count = 0
#     while (i <= len(words)-2):
#         j = i+1
#         #print (j)
#         while (j <= len(words)-1):
#             #print (i,j)
#             if (is_reverse(words[i], words[j])):
#                 count += 1
#                 print (str(count) + ". " + words[i] + " & " + words[j])
#             j += 1
#         i += 1

def is_reverse (word1, word2):
    return (word1 == word2[::-1])

# reverse_pair("bakchod", "dohckab")
