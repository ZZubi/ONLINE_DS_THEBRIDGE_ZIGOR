GLOBAL_EASIEST_TRIAL = {
    "missing_values": set(range(99)),
    "row_index": 99,
    "column_index": 99
}

def solve(board):
    """return the solved puzzle as a 2d array of 9 x 9"""
    ## reset global dictionary
    global GLOBAL_EASIEST_TRIAL
    GLOBAL_EASIEST_TRIAL = {
        "missing_values": set(range(99)),
        "row_index": 99,
        "column_index": 99
    }

    previous_gap_count_to_guess = 9999

    while previous_gap_count_to_guess > get_gaps_count_to_guess(board):
        previous_gap_count_to_guess =  get_gaps_count_to_guess(board)

        for row_index, row_value in enumerate(board):
            for column_index, column_value in enumerate(row_value):
                if column_value != 0:
                    continue

                board[row_index][column_index] = get_unique_candidate_for_position(row_index, column_index, board)

    else:
        ## aaaa
        pass

    return board

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
    missing_values = set(range(0,10)) - distinct_values_known

    if (len(GLOBAL_EASIEST_TRIAL["missing_values"]) > len(missing_values)):
        GLOBAL_EASIEST_TRIAL = {
            "missing_values": missing_values,
            "row_index": row_index,
            "column_index": column_index
        }

    return next(iter(missing_values)) if len(missing_values) == 1 else 0

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

print(solve(puzzle))