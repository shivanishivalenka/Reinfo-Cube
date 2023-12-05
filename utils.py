from typing import Any
from typing import List
from typing import Tuple
from typing import Dict
from typing import Mapping
from typing import NoReturn

import random
from cube import Cube


# ------------------------------------------------------------------------------------------------------------------
def initial_n_move_state(n: int = 5) -> Cube:
    """ Create initial n cube_perform_action state of a cube from the solved state."""
    print('\nThe new cube will be scrambled by : ', n, ' moves.\n\n')
    cube = Cube()
    return scramble(cube, n=n)


# ------------------------------------------------------------------------------------------------------------------
def initial_1_move_state() -> Cube:
    """
    Perform initial single cube_perform_action
    :return:
    """
    cube = Cube()
    cube.cube_perform_action(cube.actions[0])
    return cube


# ------------------------------------------------------------------------------------------------------------------
def scramble(cube: Cube, n: int = 5) -> Cube:
    """ Scramble a cube to a given number of moves."""

    new_cube = cube.copy()

    for _ in range(n):
        new_cube = random_move(new_cube)
    return new_cube


# ------------------------------------------------------------------------------------------------------------------
def random_move(cube: Cube) -> Cube:
    """ Perform a single random cube_perform_action of 180 degree on the given cube."""

    action = random.choice(cube.actions)

    print("executing " + action + "\t180 rotation")
    cube = perform_action(cube, action)
    return cube


def perform_action(cube, action):
    #print("in util.cube_perform_action() : ", cube)
    new_state = cube.copy()

    if action == 'left':
        new_state.turn_left()
    elif action == 'right':
        new_state.turn_right()
    elif action == 'front':
        new_state.turn_front()
    elif action == 'back':
        new_state.turn_back()
    elif action == 'up':
        new_state.turn_up()
    elif action == 'down':
        new_state.turn_down()
    new_state.__sides__ = [new_state.front(), new_state.back(), new_state.left(), new_state.right(), new_state.up(),
                           new_state.down()]
    return new_state


# ------------------------------------------------------------------------------------------------------------------
def num_of_solved_faces(cube: Cube) -> int:
    """
    Computes the number of solved faces of a given cube.
    :param cube: The Cube.
    :return: Number of solved faces.
    """
    # Initialized the number of solved faces to be zero.
    solved_faces_count = 0

    # If all the facelets are of same colour to the first facelet
    # then that face is considered as solved face.
    for face in cube.__faces__:
        color = face[0][0]

        # #if number of pieces on this side equal to first square
        # #is number of total pieces, side is solved
        if sum(row.count(color) for row in face) == cube.size ** 2:
            solved_faces_count += 1

    return solved_faces_count


# ------------------------------------------------------------------------------------------------------------------
def num_of_solved_facelets(cube: Cube) -> int:
    """
    Computes the number of correct facelets that matches to the center/middle facelet colour.
    :param cube: The Cube.
    :return: Number of correct facelets in the whole cube.
    """

    # Initialize the number of solved facelets to be zero.
    correct_facelet_count = 0

    for facelet in cube.__faces__:
        # Find the colour of the middle facelet
        color = facelet[int(cube.size / 2)][int(cube.size / 2)]

        # As the middle facelet is always solved, thus subtract 1 from the current facelet count
        correct_facelet_count -= 1

        # Add all the number of facelets having same color as the middle facelet of that face.
        # This assumes that we have hot-encoded the colors of the facelets, thus either the color is 0 or 1
        for row in facelet:
            correct_facelet_count += row.count(color)

    return correct_facelet_count

# ------------------------------------------------------------------------------------------------------------------
