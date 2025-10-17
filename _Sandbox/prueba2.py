import copy

GLOBAL_EASIEST_TRIAL = {
    "missing_values": list(range(99)),
    "row_index": 99,
    "column_index": 99
}

GLOBAL_ORIGINAL_SUDOKU = []

def ensure_sudoku_is_correct(puzzle):
    if len(puzzle) != 9:
        raise Exception()
    
    for row in puzzle:
        if len(row) != 9:
            raise Exception()
        
    for row_index, row_value in enumerate(puzzle):
        for column_index, column_value in enumerate(row_value):
            if column_value > 9 or column_value < 0:
                raise Exception()
            
def sudoku_solver(puzzle):            
    ensure_sudoku_is_correct(puzzle)
    global GLOBAL_ORIGINAL_SUDOKU
    GLOBAL_ORIGINAL_SUDOKU = puzzle ## save the original sudoku to a global variable

    return sudoku_solver_trial(puzzle)

def sudoku_solver_trial(puzzle, alternative_solution_trial=False):

    """return the solved puzzle as a 2d array of 9 x 9"""
    ## reset global dictionary
    global GLOBAL_EASIEST_TRIAL
    GLOBAL_EASIEST_TRIAL = {
        "missing_values": list(range(99)),
        "row_index": 99,
        "column_index": 99
    }

    previous_gap_count_to_guess = 9999

    while previous_gap_count_to_guess > get_gaps_count_to_guess(puzzle):
        previous_gap_count_to_guess =  get_gaps_count_to_guess(puzzle)

        for row_index, row_value in enumerate(puzzle):
            for column_index, column_value in enumerate(row_value):
                if column_value != 0:
                    continue
                try:
                    puzzle[row_index][column_index] = get_unique_candidate_for_position(row_index, column_index, puzzle)
                except:
                    return []

    else:
        if get_gaps_count_to_guess(puzzle) == 0:
           ## this is ONE CORRECT solution, we need to check if there is another correct one
           # if this is the first solution we have (alternative_solution_trial == False), look for the alternative
           if (not alternative_solution_trial):
                alternative_puzzle_solution = sudoku_solver_trial(copy.deepcopy(GLOBAL_ORIGINAL_SUDOKU), True)

                # Compare both solutions, if they are not equal raise an exception
                if alternative_puzzle_solution and puzzle != alternative_puzzle_solution:
                    raise Exception("This sudoku has more than one alternative")

                return puzzle ## this is the correct solution, and the unique one
           ## ELSE, this is the alternative, so we return it right away
           else:
               return puzzle

        ## if we reach here, the current board ir not a solution, we need to make a bet

        ## bet on each of the possible missing values on the GLOBAL_EASIEST_TRIAL, at least one of them should not return an empty board
        current_easiest_bet_trial = copy.deepcopy(GLOBAL_EASIEST_TRIAL)

        ## This approach based on the trial order tries to get an alternative solution for the sudoku:
        #print(current_easiest_bet_trial)
        missing_values:list = current_easiest_bet_trial["missing_values"] if not alternative_solution_trial else reversed(current_easiest_bet_trial["missing_values"])

        for bet_number in missing_values:
            solved_board = try_to_solve_with_a_bet(puzzle, bet_number, current_easiest_bet_trial["row_index"], current_easiest_bet_trial["column_index"])
            if len(solved_board) != 0:
                return solved_board ## this is a valid approach, otherwise, continue with next iteration

        return [] ## we shouldn't reach this statement

def try_to_solve_with_a_bet(current_board, bet_number, row_index, column_index):
    new_board_bet = copy.deepcopy(current_board)
    new_board_bet[row_index][column_index] = bet_number

    return sudoku_solver_trial(new_board_bet)

def get_gaps_count_to_guess(puzzle):
    gap_count = 0
    for row in puzzle:
        gap_count += row.count(0)
        
    return gap_count

def get_unique_candidate_for_position(row_index, column_index, puzzle):
    global GLOBAL_EASIEST_TRIAL

    row_values = [x for x in puzzle[row_index]]
    column_values = [puzzle[x][column_index] for x in range(0,9)]
    quadrant_values = get_quadrant_values(row_index, column_index, puzzle)

    distinct_values_known = set(row_values + column_values + quadrant_values)
    ##missing_values = list(range(0,10)) - distinct_values_known

    missing_values = [
        item 
        for item in list(range(0,10)) 
        if item not in distinct_values_known
    ]

    missing_values_count = len(missing_values)

    if (missing_values_count > 1 and len(GLOBAL_EASIEST_TRIAL["missing_values"]) > missing_values_count):
        GLOBAL_EASIEST_TRIAL = {
            "missing_values": missing_values,
            "row_index": row_index,
            "column_index": column_index
        }

    if len(missing_values) == 0:
        raise Exception("Error, this approach can be discarded")

    return missing_values[0] if len(missing_values) == 1 else 0

def get_quadrant_values(row_index, column_index, puzzle):
    quadrant_values = []

    rows_to_iterate = get_sudoku_range_to_iterate_quadrant(row_index)
    columns_to_iterate = get_sudoku_range_to_iterate_quadrant(column_index)

    for row_index in rows_to_iterate:
        for column_index in columns_to_iterate:
            quadrant_values.append(puzzle[row_index][column_index])

    return quadrant_values


def get_sudoku_range_to_iterate_quadrant(coordinate:int):
    match coordinate:
        case 0 | 1 | 2:
            return list(range(0,3))
        case 3 | 4 | 5:
            return  list(range(3,6))
        case 6 | 7 | 8:
            return list(range(6,9))

puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8], [0, 8, 0, 0, 9, 0, 0, 3, 0], [2, 0, 0, 0, 0, 5, 4, 0, 0], [4, 0, 0, 0, 0, 1, 8, 0, 0], [0, 3, 0, 0, 7, 0, 0, 4, 0], [0, 0, 7, 9, 0, 0, 0, 0, 3], [0, 0, 8, 4, 0, 0, 0, 0, 6], [0, 2, 0, 0, 5, 0, 0, 8, 0], [1, 0, 0, 0, 0, 2, 5, 0, 0]]
'''
puzzle = [
            [0, 0, 6, 1, 0, 0, 0, 0, 8], 
            [0, 8, 0, 0, 9, 0, 0, 3, 0], 
            [2, 0, 0, 0, 0, 5, 4, 0, 0], 
            [4, 0, 0, 0, 0, 1, 8, 0, 0], 
            [0, 3, 0, 0, 7, 0, 0, 4, 0], 
            [0, 0, 7, 9, 0, 0, 0, 0, 3], 
            [0, 0, 8, 4, 0, 0, 0, 0, 6], 
            [0, 2, 0, 0, 5, 0, 0, 8, 0], 
            [1, 0, 0, 0, 0, 2, 5, 0, 0]
        ]
'''
'''
puzzle = [
            [9, 0, 0, 0, 8, 0, 0, 0, 1],
            [0, 0, 0, 4, 0, 6, 0, 0, 0],
            [0, 0, 5, 0, 7, 0, 3, 0, 0],
            [0, 6, 0, 0, 0, 0, 0, 4, 0],
            [4, 0, 1, 0, 6, 0, 5, 0, 8],
            [0, 9, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 7, 0, 3, 0, 2, 0, 0],
            [0, 0, 0, 7, 0, 5, 0, 0, 0],
            [1, 0, 0, 0, 4, 0, 0, 0, 7]
        ]


puzzle =         [[5,3,0,0,7,0,0,0,0],
                  [6,0,0,1,9,5,0,0,0],
                  [0,9,8,0,0,0,0,6,0],
                  [8,0,0,0,6,0,0,0,3],
                  [4,0,0,8,0,3,0,0,1],
                  [7,0,0,0,2,0,0,0,6],
                  [0,6,0,0,0,0,2,8,0],
                  [0,0,0,4,1,9,0,0,5],
                  [0,0,0,0,8,0,0,7,9]]

solution =         [[5,3,4,6,7,8,9,1,2],
                    [6,7,2,1,9,5,3,4,8],
                    [1,9,8,3,4,2,5,6,7],
                    [8,5,9,7,6,1,4,2,3],
                    [4,2,6,8,5,3,7,9,1],
                    [7,1,3,9,2,4,8,5,6],
                    [9,6,1,5,3,7,2,8,4],
                    [2,8,7,4,1,9,6,3,5],
                    [3,4,5,2,8,6,1,7,9]]
'''
                    
print(sudoku_solver_trial(puzzle))