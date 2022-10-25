""" File: maze_solver.py
    Author: Kevin Cascais Nisterenko
    Purpose: This program reads an input maze file and
             outputs the correct message for the user
             based on their command. It uses a dictionary
             and a 4-ary tree to solve the maze.
"""
class TreeNode:
    """
    This class creates a TreeNode object with the given
    attributes.

    The constructor initializes an instance by using the
    given value tuple and path type string.

    The class defines no other methods apart from the constructor.
    """
    def __init__(self, val, path_type):
        """
        This constructor takes the value (tuple of two integers),
        and the path type (a string that is START, END or #) and
        builds the TreeNode object with them. Both parameters are
        fields in themselves. The children are found in an array
        of four elements and they are initialized to None.

        Parameters:
            val -- tuple of two integers representing xy coordinates
                   of a path/cell in the maze.
            path_type -- string that represents the type of path.

        Returns:
            None

        Pre-condition:
            The program must call the TreeNode class to create an object
            and the parameters must be passed.

        Post-condition:
            The TreeNode object will be created.
        """
        self.val = val
        #  This array contains the adjacents (children), in
        #  the order: up, down, left, right.
        self.children = [None, None, None, None]
        #  Marks the end node.
        if path_type == "END":
            self.is_end = True
        else:
            self.is_end = False

def get_maze_coordinates(filename):
    """
    This function reads the input file, or returns if the
    file is not found. It creates the maze_coords dictionary
    by reading through the lines in the file and adding the
    coordinates (as a tuple) as keys and the string (START,
    END or #) as the values. It does not add the whitespace
    characters in the file to the dictionary.

    Parameters:
        filename -- user input string that represents the
                    name of a text file.

    Returns:
        maze_coords -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.

    Pre-condition:
        The user must give an input string.

    Post-condition:
        The function will return None (for any invalid inputs) or
        the maze_coords dict for valid files.
    """
    num_starts = 0
    num_ends = 0
    maze_coords = {}
    try:
        file_obj = open(filename)
    except FileNotFoundError:
        print("ERROR: Could not open file: {}".format(filename))
        return
    y_pos = 0
    #  Iterates over the lines in the file, initializes the
    #  x position.
    for line in file_obj:
        x_pos = 0
        line = line.strip("\n")
        #  Iterates over the characters, adds the valid characters
        #  and marks the start, end and paths.
        for char in line:
            coord = (x_pos, y_pos)
            if char == "S":
                maze_coords[coord] = "START"
                num_starts += 1
            elif char == "E":
                maze_coords[coord] = "END"
                num_ends += 1
            elif char == "#":
                maze_coords[coord] = "#"
            elif char == " ":
                pass
            else:
                print("ERROR: Invalid character in the map")
                return
            x_pos += 1
        y_pos += 1
    file_obj.close()

    #  Error checking for no/more than 1 start or end in the file.
    if num_starts > 1:
        print("ERROR: The map has more than one START position")
        return
    if num_starts == 0:
        print("ERROR: Every map needs exactly one START", end='')
        print(" and exactly one END position")
        return
    if num_ends > 1:
        print("ERROR: The map has more than one END position")
        return
    if num_ends == 0:
        print("ERROR: Every map needs exactly one START", end='')
        print(" and exactly one END position")
        return

    return maze_coords

def dump_cells(coordinates):
    """
    This function iterates through the coordinates dictionary
    and prints all the cells in it.

    Parameters:
        coordinates -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.

    Returns:
        None

    Pre-condition:
        The user must call the dumpCells command and the dictionary
        of coordinates must be passed to the function.

    Post-condition:
        The function will print out the cells to the output, one
        per line.
    """
    print("DUMPING OUT ALL CELLS FROM THE MAZE:")
    #  Gets the valid cells (paths), in the dictionary
    #  and prints them accordingly.
    for coordinate in sorted(coordinates):
        print_str = "  " + str(coordinate)
        if coordinates[coordinate] == "START":
            print(print_str + "    START")
        elif coordinates[coordinate] == "END":
            print(print_str + "    END")
        else:
            print(print_str)

def get_start_coord(coordinates):
    """
    This function iterates through the coordinates dictionary
    and finds the starting coordinate, which it then returns.

    Parameters:
        coordinates -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.

    Returns:
        coordinate -- tuple of two integers reprsenting the coordinate
                      of the starting point in the maze.

    Pre-condition:
        The dictionary must be valid and passed to the function.

    Post-condition:
        The function will return the coordinate of the starting point in
        the maze.
    """
    #  Iterates over the dictionary and finds the starting
    #  coordinate.
    for coordinate in coordinates:
        if coordinates[coordinate] == "START":
            return coordinate
    assert False

def build_tree(coord, coordinates, used_coords):
    """
    This function recursively builds the tree of the coordinates.
    It uses a set to store the used coordinates (so no child
    referecnes a parent node) and it checks for the adjacent in
    the dictionary before recursing.

    Parameters:
        coord -- tuple of two integers, representing xy coordinate
        coordinates -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.
        used_coords -- set of tuples that is passed to the function
                       and stores the used coordinates/parents already
                       in the tree.

    Returns:
        root -- TreeNode object that represents the root of the tree.

    Pre-condition:
        The dictionary must be valid, a starting coordinate must be found.

    Post-condition:
        The function will recursively build a tree using the TreeNode class
        and return the root node on the final stackframe.
    """
    #  Builds the node in each call.
    root = TreeNode(coord, coordinates[coord])
    #  Adds the node coordinate to the used set.
    used_coords.add(coord)

    #  Checks if it is possible to recurse up, then does so.
    if (coord[0], coord[1] - 1) in coordinates and \
       (coord[0], coord[1] - 1) not in used_coords:
        root.children[0] = build_tree((coord[0], coord[1] - 1),
                                      coordinates, used_coords)

    #  Checks if it is possible to recurse down, then does so.
    if (coord[0], coord[1] + 1) in coordinates and \
       (coord[0], coord[1] + 1) not in used_coords:
        root.children[1] = build_tree((coord[0], coord[1] + 1),
                                      coordinates, used_coords)

    #  Checks if it is possible to recurse left, then does so.
    if (coord[0] - 1, coord[1]) in coordinates and \
       (coord[0] - 1, coord[1]) not in used_coords:
        root.children[2] = build_tree((coord[0] - 1, coord[1]),
                                      coordinates, used_coords)

    #  Checks if it is possible to recurse right, then does so.
    if (coord[0] + 1, coord[1]) in coordinates and \
       (coord[0] + 1, coord[1]) not in used_coords:
        root.children[3] = build_tree((coord[0] + 1, coord[1]),
                                      coordinates, used_coords)
    return root

def dump_tree(root, char=""):
    """
    This function recursively prints the values of the nodes
    of the tree in a pre-order traversal. It makes use of default
    char parameter so that the indentation can be done correctly.

    Parameters:
        root -- TreeNode object that represents the root of the tree.
        char -- string that defaults at an empty string and is incremented
                with "| " for every level in the tree.

    Returns:
        None

    Pre-condition:
        The root node must be passed to the function and the user must
        call the dumpTree command.

    Post-condition:
        The function will recursively and in a pre-order traversal,
        print the tree.
    """
    #  Base case, end of tree.
    if root is None:
        return
    #  Pre order, first print the root.
    print("  " + char + str(root.val))
    #  Then iterate over the children and
    #  do the recursive call, now adding a
    #  character to the default.
    for child in root.children:
        dump_tree(child, char + "| ")

def get_solution_arr(root, path, solution):
    """
    This function recursively finds the solution to the maze, by
    storing the visited nodes in an array, which is then copied to
    the solution when the path is found. It modifies the arrays in
    place and uses a pre-order traversal to first check the node for
    the end marker and then copy the contents of the lists when
    it is found. Otherwise, it traverses the tree with a copy of the
    current path recursively.

    Parameters:
        root -- TreeNode object that represents the root of the tree.
        path -- empty array that will be used to store the traversal
                as a whole. In the recursive calls it is no longer
                empty.
        solution -- empty array that will have the contents of the
                    path appended to it when the function finds the
                    end node.

    Returns:
        None

    Pre-condition:
        The dictionary must be valid, a starting coordinate must be found.

    Post-condition:
        The function will recursively build a tree using the TreeNode class
        and return the root node on the final stackframe.
    """
    if root is None:
        return
    #  As we visit nodes, append them to the path
    #  array.
    path.append(root.val)
    #  Found the end node.
    if root.is_end:
        #  Iterate through the path array we have now.
        for coord in path:
            #  Append to the solution array, which is
            #  created outside the function so the
            #  recursive calls don't change it.
            solution.append(coord)
    else:
        for child in root.children:
            #  A copy is used to ensure that
            #  only one path is given and not all
            #  nodes that were searched.
            curr_path = path[:]
            get_solution_arr(child, curr_path, solution)

def dump_solution(solution):
    """
    This function iterates through the solutions array and
    prints the tuples found in it.

    Parameters:
        solution -- array of tuples that represent the path
                    from start to end of the maze. The tuples
                    contain two integers representing xy
                    coordinates.

    Returns:
        None

    Pre-condition:
        The solutions array must be passed to the function and the
        user must call the dumpSolution command.

    Post-condition:
        The function will print, line by line, the cells that
        represent the solution path of the maze.
    """
    print("PATH OF THE SOLUTION:")
    #  Simply iterates over the solution array we generated using
    #  the get_solution_arr function and print out the cells.
    for coord in solution:
        print(" ", coord)

def get_size(coordinates):
    """
    This function iterates through the coordinates dictionary
    and finds the maximum width and height values, which it then
    returns.

    Parameters:
        coordinates -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.

    Returns:
        max_wid + 1 -- integer that represents the maximum width
                       of the maze.
        max_hei + 1 -- integer that represents the maximum height
                       of the maze.

    Pre-condition:
        The dictionary must be valid and passed to the function.

    Post-condition:
        The function will return integers that represent the maximum
        width and height of the maze.
    """
    max_wid = 0
    max_hei = 0

    #  Iterate over what we have now (dictionary),
    #  and calculate the max width and height.
    for coord in coordinates:
        if coord[0] > max_wid:
            max_wid = coord[0]
        if coord[1] > max_hei:
            max_hei = coord[1]

    #  Incremented so that it can be iterated correctly for
    #  printing.
    return max_wid + 1, max_hei + 1

def dump_size(wid, hei):
    """
    This function simply prints the maximum width and height of
    the maze to the output.

    Parameters:
        wid -- integer that represents the maximum width
                       of the maze.
        hei -- integer that represents the maximum height
                       of the maze.

    Returns:
        None

    Pre-condition:
        The width and height must be passed to the function and the
        user must call the dumpSize command.

    Post-condition:
        The function will print the maximum width and height of the
        maze.
    """
    print("MAP SIZE:")
    print("  wid:", wid)
    print("  hei:", hei)

def print_solved_maze(coordinates, solution, max_wid, max_hei):
    """
    This function uses nested for loops to iterate over the width
    and height of the maze, then check each coordinate, if they are
    on the solution, it prints a period. If they are on the coordinate
    but not on the solution, it prints a #. Otherwise, if they are
    not in the coordinates dictionary, it prints a blank space. This
    way, the map with the solution path outlined is printed at the
    end.

    Parameters:
        coordinates -- dictionary where each key is a tuple
                       of two integers representing xy coordinates
                       and the keys are strings.
        solution -- array of tuples that represent the path
                    from start to end of the maze. The tuples
                    contain two integers representing xy
                    coordinates.
        max_wid -- integer that represents the maximum width
                       of the maze.
        max_hei -- integer that represents the maximum height
                       of the maze.

    Returns:
        None

    Pre-condition:
        All parameters must be passed to the function and the user
        must not enter any command, just press enter.

    Post-condition:
        The function will print out the maze with the solution
        path outlined by periods.
    """
    print("SOLUTION:")
    #  Iterates over the height, so it prints one row at a time.
    for i in range(max_hei):
        #  Iterates over the width, so it prints each character
        #  correctly in the rectangle.
        for j in range(max_wid):
            coord = (j, i)
            #  Checks which character to print.
            if coord in coordinates:
                if coordinates[coord] == "START":
                    print("S", end='')
                elif coordinates[coord] == "END":
                    print("E", end='')
                elif coord in solution:
                    print(".", end='')
                else:
                    print("#", end='')
            else:
                print(" ", end='')
        print()

def main():
    filename = input()

    #  Gets the coordinates dictionary.
    coordinates_dict = get_maze_coordinates(filename)

    if coordinates_dict is None:
        return

    user_command = input()

    #  Builds the tree.
    root_coord = get_start_coord(coordinates_dict)
    used_coords = set()
    root = build_tree(root_coord, coordinates_dict, used_coords)

    #  Builds the solution array (for both empty input and
    #  dumpSolution).
    path = []
    solution = []
    get_solution_arr(root, path, solution)

    #  Gets the size for both dumpSize and printing later.
    wid, hei = get_size(coordinates_dict)

    if user_command == "dumpCells":
        dump_cells(coordinates_dict)
    elif user_command == "dumpTree":
        print("DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:")
        dump_tree(root)
    elif user_command == "dumpSize":
        dump_size(wid, hei)
    elif user_command == "dumpSolution":
        dump_solution(solution)
    elif user_command == "":
        print_solved_maze(coordinates_dict, solution, wid, hei)
    else:
        print("ERROR: Unrecognized command {}".format(user_command))

if __name__ == "__main__":
    main()