assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())

    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    boxes = cross(rows,cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # print(values)
    potential_twins = [key for key,val in values.items() if len(val) == 2]
    print("twins",potential_twins)
    naked_twins = []
    for twin in potential_twins:
        for peer in peers[twin]:
            if peer in potential_twins and values[peer] == values[twin]:
                naked_twins.append([twin,peer])
                # print("peer",peer)
                # print("twin",twin)
                # print("value1", values[peer])
                # print("value2", values[twin])
    for i in range(len(naked_twins)):
        twin1 = naked_twins[i][0]
        twin2 = naked_twins[i][1]
    print('naked_twins',naked_twins)
    # for val in potential_twins:
        # for peer in peers[val]:
            # print("peer",peer)
            # print("peer_val",values[peer])
            # print("values_val",values[val])

    # for key,val in values.items():
    #     for
    #     if len(val) > 1:
    #         for peer in peers[key]:
    #             if len(values[peer]) == 1:
    #                 val = val.replace(values[peer],"")
    #     values[key] = val
    # return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    boxes = cross(rows,cols)
    values = {box:'' for box in boxes}
    chars = [val if val in digits else digits for val in grid]
    for i,key in enumerate(values):
        assign_value(values,key,chars[i])
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = cross(rows,cols)
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    boxes = cross(rows,cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    for key,val in values.items():
        if len(val) > 1:
            for peer in peers[key]:
                if len(values[peer]) == 1:
                    val = val.replace(values[peer],"")
        assign_value(values,key,val)
        values[key] = val
    return values

def only_choice(values):
    boxes = cross(rows,cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    for unit in unitlist:
        for digit in '123456789':
            count = [box for box in unit if digit in values[box]]
            if len(count) == 1:
                assign_value(values,count[0],digit)
                values[count[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        # values = naked_twins(values)
        naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    boxes = cross(rows,cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
