def min_max(t):
    return min(t), max(t)

print(min_max((4, -2)))

def print_all(*args):
    print (type(args))

#print_all(1, 2.0, '3')

def sumall(*args):
    sum = 0
    for arg in args:
        sum += arg
    return sum

#print(sumall(1, 4, -97))

"""do exercise 2 random unstable sort later"""
def sort_by_length(words):
    t = []
    for word in words:
       t.append((len(word), word))

    t.sort(reverse=True)

    res = []
    for length, word in t:
        res.append(word)
    return res

print(sort_by_length(["avara", "kim", "bokar", "poerla", "oopsi", "expelliarmus", "trg"]))

def most_frequent(word):
    d = dict()
    freq = []
    """
    character:
        1. {'c': 2, 'h': 1 ...}
        2. [(2, 'c'), (1, 'h') ...]
    """

    for char in word:
        d[char] = 1 + d.get(char, 0)

    for key in d:
        freq.append((d[key], key))

#    freq.sort(reverse=True)
    return d # list of 2 tuple ('2', 'c')

def vowel_frequency ():
    # d = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0
    #         'j': 0,}

    v = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

    words_file = open(".\ThinkPython\words.txt")
    for word in words_file:
        char_freq = most_frequent(word)
        for char in char_freq:
            if char in v:
                v[char] += char_freq[char]

    print (v)

# most_frequent("character")
# vowel_frequency()

def sets_of_anagrams():
    words_file = open(".\ThinkPython\words.txt")
    dict_len_map = dict()

    for word in words_file:
        word = word.strip()
        if len(word) not in dict_len_map:
            dict_len_map[len(word)] = []
        dict_len_map[len(word)].append(word)

    anagram_dict = dict()
    for length in dict_len_map:
        if length > 2:
            for word in dict_len_map[length]:
                if "".join(sorted(word)) not in anagram_dict:
                    anagram_dict["".join(sorted(word))] = []

            for word in dict_len_map[length]:
                if "".join(sorted(word)) in anagram_dict:
                    anagram_dict["".join(sorted(word))].append(word)

    # with open("anagrams.txt", 'w') as ana_file:
    #     for values in anagram_dict.values():
    #         if len(values) > 1:
    #             ana_file.write(str(values) + "\n")
    #
    # with open("largest_anagrams.txt", 'w') as ana_file:
    #     for values in list(anagram_dict.values())[::-1]:
    #         if len(values) > 1:
    #             ana_file.write(str(values) + "\n")

    bingo = []

    for key, value in anagram_dict.items():
        if (len(key) == 8):
            if (len(value) >= len(bingo)):
                bingo = value

    print (bingo)

    return anagram_dict

# def metathesis_pair (anagram_d):
#     words_file = open(".\ThinkPython\words.txt")
#
#     for word in words_file:
#         word = word.strip()
#
#
# metathesis_pair(sets_of_anagrams())




def children (word):
    children = []
    length = len(word)

    if length == 1:
        children.append(word)
    else:
        children.append(word[:-1])
        children.append(word[1:])
        index = 1
        while (index <= length-2):
            children.append(word[0:index] + word[index+1:])
            index += 1

    return children

def make_dict():
    words_file = open(".\ThinkPython\words.txt", 'r')
    d = dict()

    for word in words_file:
        word = word.strip().lower()
        d[word] = word

    for letter in ['', 'a', 'i']:
        d[letter] = letter

    return d

"""
memo{} is a dict of reducible words where memo[red_word] = [list of
reducible children]
"""
memo = {}
memo[''] = ['']

"""
if word is_red() returns list of reducible children,
else returns empty string
"""
# def is_reducible(word, word_dict):
#     if word in memo:
#         return memo[word]
#     else:
#         if word in word_dict:
#

def is_reducible (word):
    global known_reducible, known_counter
    d = dictionary()

    if word in known_reducible:
        return True
    elif word in d:
        for child in children(word):
            flag = False
            flag = is_reducible(child)
            if flag == True:
                known_reducible[word] = known_counter
                known_counter += 1
                return True
    return False

def reducible():
    d = dictionary()
    all_reducible = []

    for word in d:
        if is_reducible(word):
            print(word)
            all_reducible.append(word)

    print (len(all_reducible), len(d))


    with open("reducibles.txt", 'w') as reducibles_file:
        for word in all_reducible:
            reducibles_file.write("%s\n" % (word))

print (children("spit"))
print (is_reducible("spit"))
print (known_reducible)

reducible()
