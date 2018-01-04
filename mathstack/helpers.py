""" helpers.py
    Helper functions for the mathstack app.
"""

import random

def compute_answer(q_text):
    """ Method to ingest the raw text of a question, e.g., "10 % 2 == 0",
    and return the right answer.  Raises a `RuntimeError` if an unknown
    question format is encountered.  
    Expected question types are divisibility and multiplication questions.
    """
    if "%" in q_text:
        return eval(q_text)  # returns a Boolean
    elif "*" in q_text:
        return eval(q_text[:-1])  # returns an integer
    else:
        raise RuntimeError("Unknown question format; can't parse.")

def get_divisor():
    DIVISORS = [2,3,4,5,6,9]
    return random.choice(DIVISORS)

def get_next_q():
    """ Method to generate a random math question and return it as a string.
    Presently generates divisibility questions only.
    """
    LOWER = 10
    UPPER = 5000
    op1 = random.randint(LOWER, UPPER)
    op2 = get_divisor()
    q_text = "{op1} % {op2} == 0".format(op1=op1, op2=op2)
    return q_text

def parse_question(q_text):
    """ Ingests a question string and returns a dictionary.
    """
    q_dict = {}
    q_items = q_text.split(" ")
    if "%" in q_items:
        q_dict["operand1"] = q_items[0]
        q_dict["divisor"] = q_items[2]
    return q_dict
