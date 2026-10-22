# =====================================================================
#  ROOM 4: THE LIBRARY
# =====================================================================
#  You stumble into a dusty library. Every title on the book spines is
#  backwards, and a ghostly librarian blocks the exit:
#
#    "Read my books properly and I'll let you leave."
#
#  WHAT TO DO
#  Finish the three functions below so they RETURN the right answers.
#  Save the file and the game will test them.
#
#  TOPICS: strings, slicing, .split(), .upper(), .lower(), .replace()
# =====================================================================


def reverse_text(text):
    """The book spines are written backwards. Return text reversed.

        reverse_text("ROOD") -> "DOOR"

    Hint: slices can have a step: text[start:stop:step]
    """
    # TODO
    pass


def first_letters(sentence):
    """A hidden message is made from the FIRST letter of each word,
    in CAPITALS.

        first_letters("keep every yard") -> "KEY"

    Hint: .split() turns a sentence into a list of words.
    """
    result = ""
    # TODO
    return result


def is_palindrome(phrase):
    """The librarian only trusts palindromes: phrases that read the same
    forwards and backwards. Ignore capital letters and spaces.
    Return True or False.

        is_palindrome("Race car") -> True
        is_palindrome("Python")   -> False
    """
    # TODO
    pass


# ---------------------------------------------------------------------
#  Try your code here! This part only runs when YOU run this file.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print(reverse_text("ROOD"))              # should print DOOR
    print(first_letters("keep every yard"))  # should print KEY
    print(is_palindrome("Race car"))         # should print True
