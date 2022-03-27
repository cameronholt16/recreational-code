def contains_3_digits_that_sum_to_15(list_of_digits):
    if len(list_of_digits) < 3:
        return False
    if (2 in list_of_digits and 7 in list_of_digits and 6 in list_of_digits):
        return True
    if (9 in list_of_digits and 5 in list_of_digits and 1 in list_of_digits):
        return True    
    if (4 in list_of_digits and 3 in list_of_digits and 8 in list_of_digits):
        return True
    if (2 in list_of_digits and 9 in list_of_digits and 4 in list_of_digits):
        return True
    if (7 in list_of_digits and 5 in list_of_digits and 3 in list_of_digits):
        return True
    if (6 in list_of_digits and 1 in list_of_digits and 8 in list_of_digits):
        return True
    if (2 in list_of_digits and 5 in list_of_digits and 8 in list_of_digits):
        return True
    if (4 in list_of_digits and 5 in list_of_digits and 6 in list_of_digits):
        return True
    return False