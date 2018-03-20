def rev(word):
    i = 0
    while (i < len(word)):
        print(word[-1-i])
        i+= 1

def any_lowercase4(s):
    flag = False
    for c in s:
        flag = flag or c.islower()
    return flag

def any_lowercase5(s):
    for c in s:
        if not c.islower():
            return False
    return True

# print(any_lowercase4("cHaR"))
# print(any_lowercase5("cHaR"))
#
# print(any_lowercase4("JAhJA"))
# print(any_lowercase5("JAhJA"))
#
# print(any_lowercase4("ct"))
# print(any_lowercase5("ct"))
#
# print(any_lowercase4("KT"))
# print(any_lowercase5("KT"))
#
# rev("happy")

def has_no_e(word):
    if 'e' in word:
        return True
    return False

def avoids(word, forbidden_letters):
    for l in forbidden_letters:
        if l in word:
            return False
    return True

def uses_only(word, only_letters):
    for w in word.strip():
        if w not in only_letters:
            return False
    return True

# print(uses_only("hoe alfalfa", "acefhlo"))
# print(uses_only("Hoe alfalfa", "acefhlox"))

def uses_all(word, all_letters):
    for l in all_letters:
        if l not in word:
            return False
    return True

words_file = open(".\ThinkPython\words.txt")
words = words_file.read()
#print (words)

#e_words = 0
no_forbidden_letter_words = 0
forbidden_letters = "aeiouys"
two_letter_nonforbidden_words = []

# for line in words.splitlines():
#     if (avoids(line.strip(), forbidden_letters)):
#         no_forbidden_letter_words += 1
#         if (len(line.strip()) == 2):
#             two_letter_nonforbidden_words.append(line.strip())
#         print(line.strip())

# print("no " + forbidden_letters +" words count: " + str(no_forbidden_letter_words))
# print("two_letter_nonforbidden_words: " + str(two_letter_nonforbidden_words))

def cartalk1_three_consecutive_double (words):
    for word in words.splitlines():
        word = word.strip()
        if (len(word) >= 6):
            no_of_scans = len(word) - 5
            index = 0

            while (no_of_scans > 0):
                flag = test_six_letter_splice(word[0+index: 6+index])
                if flag == True:
                    print (word)
                    break
                index += 1
                no_of_scans -= 1

def test_six_letter_splice(splice):
    if ((splice[0] == splice[1]) & (splice[2] == splice[3]) & (splice[4] == splice[5])):
        return True
    return False

# print (test_six_letter_splice("aabbcc"))
# print (test_six_letter_splice("aabbcd"))

#cartalk1_three_consecutive_double(words)

def cartalk_palindromic ():
    six_figure_palindromes = []

    for i in range(100000, 999999):
        if (str(i) == str(i)[::-1]):
            six_figure_palindromes.append(i)

    for number in six_figure_palindromes:
        count = 0
        if (str(number-1)[1:5] == str(number-1)[1:5:-1]):
            count += 1
        if (str(number-2)[1:6] == str(number-2)[1:6:-1]):
            count += 1
        if (str(number-3)[2:6] == str(number-3)[2:6:-1]):
            count += 1

        if count == 3:
            print (number)

cartalk_palindromic()

def has_palindrome(i, start, len):
    """Returns True if the integer i, when written as a string,
    contains a palindrome with length (len), starting at index (start).
    """
    s = str(i)[start:start+len]
    return s[::-1] == s


def check(i):
    """Checks whether the integer (i) has the properties described
    in the puzzler.
    """
    return (has_palindrome(i, 2, 4)   and
            has_palindrome(i+1, 1, 5) and
            has_palindrome(i+2, 1, 4) and
            has_palindrome(i+3, 0, 6))


def check_all():
    """Enumerates the six-digit numbers and prints any that satisfy the
    requirements of the puzzler"""

    i = 100000
    while i <= 999996:
        if check(i):
            print (i)
        i = i + 1


print ('The following are the possible odometer readings:')
check_all()
