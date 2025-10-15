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

    total_steps = (end_number - begin_number) // step + 1
    ##print("total_steps:",total_steps)

    ##sumatorio_de_steps = sum(range(1, total_steps))
    ##print("sum1:", sumatorio_de_steps)
    sumatorio_de_steps = (total_steps * (total_steps - 1))/2
    ##print("sum2:", sumatorio_de_steps)

    ##print(sumatorio_de_steps)
    return begin_number * total_steps + step * sumatorio_de_steps


def determine_if_we_should_continue(step, next_sum_value, end_number):
    return next_sum_value <= end_number if step > 0  else next_sum_value >= end_number


def sequence_sum3(begin_number, end_number, step):
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
print(20516913255418539316)
##print(sequence_sum3(58340206, 9059307733, 2))