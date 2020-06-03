def intro_text():
    print("Welcome To the classic game of battleship!")
    print("By Peter Agalakov")
    print('v0.1')


def valid_entry(entry):
    """
    Checks if an entry is a valid one.
    """
    valid_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    condition_a = entry[0] in valid_list
    if len(entry) == 2:
        try:
            condition_b = 1 <= int(entry[1]) <= 10
        except ValueError:
            return False

    elif len(entry) == 3:
        try:
            condition_b = int(entry[1]) == 1 and int(entry[2]) == 0
        except ValueError:
            return False
    else:
        return False

    if condition_a and condition_b:
        return True
    else:
        return False


def valid_end_entry(end_loc, max_end_points, valid_end_loc):
    while True:
        try:
            if 1 <= int(end_loc) <= max_end_points:
                end_loc = valid_end_loc[int(end_loc)]
                return [True, end_loc]
            else:
                print('Invalid entry, please try again!')
                return [False]
        except ValueError:
            print('Invalid entry, please try again!')
            return [False]


def to_alpha_numeric(entry):
    """
    Transforms a grid position into a matrix position (IE: A3 --> [0, 3]
    """
    grid_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
            7: 'H', 8: 'I', 9: 'J'}
    # Columns then rows
    entry = [grid_dict[entry[1]] + str(entry[0] + 1)]
    return entry


def to_numeric(entry):
    """
    Transforms a grid position into a matrix position (IE: A3 --> [0, 3]
    """
    grid_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                 'H': 7, 'I': 8, 'J': 9}
    # Columns then rows
    if len(entry) == 2:
        entry = [int(entry[1]) - 1, grid_dict[entry[0]]]
    elif len(entry) == 3:
        entry = [9, grid_dict[entry[0]]]

    return entry


def select_dict(a_list):
    """
    Takes a list of valid locations and make a dictionary with them so the
    user can easily select an end location.
    :param a_list:
    :return: dictionary
    """
    my_dict_matrix = {}
    my_dict_print = {}
    for i in range(len(a_list)):
        my_dict_matrix[i + 1] = a_list[i]
        my_dict_print[i + 1] = to_alpha_numeric(a_list[i])
    return my_dict_matrix, my_dict_print
