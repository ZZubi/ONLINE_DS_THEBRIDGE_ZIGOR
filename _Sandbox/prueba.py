import sys

# Set a new, higher limit
sys.setrecursionlimit(999999) 

def sequence_sum2(begin_number, end_number, step):

    if step == 0 or (begin_number > end_number and step > 0) or (begin_number < end_number and step < 0):
        return 0

    next_number = begin_number + step
    
    if next_number <= end_number:
        return begin_number + sequence_sum(next_number, end_number, step)
    
    return begin_number

def sequence_sum(begin_number, end_number, step):
    if step == 0 or (begin_number > end_number and step > 0) or (begin_number < end_number and step < 0):
        return 0

    return_value = begin_number
    next_sum_value = begin_number + step

    continue_flag = (step > 0 and next_sum_value <= end_number) or (step < 0 and next_sum_value >= end_number)

    while continue_flag:

        return_value += next_sum_value
        next_sum_value += step
        continue_flag = (step > 0 and next_sum_value <= end_number) or (step < 0 and next_sum_value >= end_number)

    return return_value


print(sequence_sum(20, 673388797, 5))