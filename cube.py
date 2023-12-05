from __future__ import annotations  # used for future reference, like using type hint as the current class name

from typing import Any
from typing import List
from typing import Tuple
from typing import Dict
from typing import Mapping
from typing import NoReturn

import copy


class Cube:
    """
    This class is the state object for the standard 3x3 Rubik's Cube.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, size: int = 3, c=None):
        self.size = size
        self.actions = ['front', 'back', 'left', 'right', 'up', 'down']

        if c:
            self.__front__ = c["front"]
            self.__back__ = c["back"]
            self.__left__ = c["left"]
            self.__right__ = c["right"]
            self.__up__ = c["up"]
            self.__down__ = c["down"]

            self.__faces__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]
            return

        # create array of values 1-6 for different colors
        # and multiply by number of pieces per size to get
        # equal amount of each color (white. black, red, orange, green, yellow)
        '''nums = ['W','B','R','O','G','Y']*(size**2)
        # shuffle numbers
        shuffle(nums)
        front, nums = nums[0:size**2],nums[size**2:]
        self.__front__ = [front[i:i + size] for i in range(0,len(front), size)]
        back, nums = nums[0:size**2],nums[size**2:]
        self.__back__ = [back[i:i + size] for i in range(0,len(front), size)]
        left, nums = nums[0:size**2],nums[size**2:]
        self.__left__ = [left[i:i + size] for i in range(0,len(front), size)]
        right, nums = nums[0:size**2],nums[size**2:]
        self.__right__ = [right[i:i + size] for i in range(0,len(front), size)]
        top, nums = nums[0:size**2],nums[size**2:]
        self.__top__ = [top[i:i + size] for i in range(0,len(front), size)]
        bottom, nums = nums[0:size**2],nums[size**2:]
        self.__bottom__ = [bottom[i:i + size] for i in range(0,len(front), size)]'''

        self.__front__ = [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']]
        self.__back__ = [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]

        self.__left__ = [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]
        self.__right__ = [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']]

        self.__up__ = [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']]
        self.__down__ = [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]

        self.__faces__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        """ toString method for a Cube or State."""
        return "\n\tFRONT\t" + str(self.__front__) + \
               "\n\tBACK\t" + str(self.__back__) + \
               "\n\tLEFT\t" + str(self.__left__) + \
               "\n\tRIGHT\t" + str(self.__right__) + \
               "\n\tUP\t" + str(self.__up__) + \
               "\n\tDOWN\t" + str(self.__down__)

    # ------------------------------------------------------------------------------------------------------------------
    def __hash__(self):
        return hash(self.__str__())

    # ------------------------------------------------------------------------------------------------------------------
    def equals(self, other: Cube) -> bool:
        """
        Equals (like in java) function for the cube/state object.
        :param other:
        :return:
        """
        is_equal = (self.__front__ == other.front()) \
                   and (self.__back__ == other.back()) \
                   and (self.__left__ == other.left()) \
                   and (self.__right__ == other.right()) \
                   and (self.__up__ == other.up()) \
                   and (self.__down__ == other.down())

        return is_equal

    # ------------------------------------------------------------------------------------------------------------------
    def copy(self):
        """ Make a deep copy of the current state of the cube."""
        state_copy = copy.deepcopy(self)
        return state_copy

    # ------------------------------------------------------------------------------------------------------------------
    def is_goal_state_reached(self) -> bool:
        """
        Check if the agent has reached the Goal/Solved State.
        :return: boolean: True when goal state is reached else False.
        """

        # check if all 3 lists that make up a face are equal
        # for every face, return false if this is not the case
        # e.g. face = [[1,1,1], [1,1,1], [1,1,2]]
        for face in self.__faces__:
            char = face[0][0]
            # check if all values in each row are equal
            # to the first value
            for row in face:
                if not char == row[0] == row[1] == row[2]:
                    return False

        #for face in self.__faces__:
        #    print('\t Face is : ', face)
        #print('\n Cube has reached its GOAL State!!!', self.__str__(), '\n')
        #print('\n Copied Cube has reached its GOAL State!!!', self.copy(), '\n')
        #print('\t Number of solved faces : ', self.num_of_solved_faces(), '\n')

        return True

    # ------------------------------------------------------------------------------------------------------------------
    def num_of_solved_faces(self) -> int:
        """
        Computes the number of solved faces of a given cube.
        :param cube: The Cube.
        :return: Number of solved faces.
        """
        # Initialized the number of solved faces to be zero.
        solved_faces_count = 0

        # If all the facelets are of same colour to the first facelet
        # then that face is considered as solved face.
        for face in self.__faces__:
            color = face[0][0]

            # #if number of pieces on this side equal to first square
            # #is number of total pieces, side is solved
            if sum(row.count(color) for row in face) == self.size ** 2:
                solved_faces_count += 1

        return solved_faces_count

    # ------------------------------------------------------------------------------------------------------------------
    def cube_perform_action(self, action):
        """
        Perform the action (cube_perform_action) on the cube.
        :param action: One of the action from the list of actions
        ['front', 'back', 'left', 'right', 'up', 'down']
        :return: self
        """

        if action == 'left':
            self.turn_left()
        elif action == 'right':
            self.turn_right()
        elif action == 'front':
            self.turn_front()
        elif action == 'back':
            self.turn_back()
        elif action == 'up':
            self.turn_up()
        elif action == 'down':
            self.turn_down()
        self.__faces__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]

    # ------------------------------------------------------------------------------------------------------------------
    # current cube_perform_action constraints: can only cube_perform_action clockwise
    # and can only turn the cube 180 degrees,
    # turn the front face to the right, causes the first
    # row of up/down to be swapped, and the first row of
    # left/right to be swapped, and the front face to be inverted
    # when we rotate a face, we are implementing it assuming that the
    # user turns their face to that face of the rubik's cube, then
    # does a 180 degree left rotation, this simplifies the implementation

    def turn_front(self):
        # invert the front face
        self.__front__ = self.rotate_face(self.__front__)
        # swap the first row of the left/right face, and swap
        # the last column of the left face with the first column of the right face
        self.__up__, self.__down__ = self.swap_first_row(self.__up__, self.__down__)
        self.__left__, self.__right__ = self.swap_first_last_col(self.__left__, self.__right__)

    def turn_back(self):
        # swap the last row of the left/right faces, and the first
        # row of the up/down faces
        # must rotate 90 degrees twice
        self.rotate_cube()
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()
        self.rotate_cube()

    def turn_left(self):
        # left become front, front becomes right, right becomes back, back becomes left
        # up gets rotated 90 degrees counter clockwise
        # (3 6 9 -> 1 2 3) (2 5 8 -> 4 5 6) (1 4 7 -> 7 8 9)

        # must turn the cube 90 degrees counter clockwise to face the
        # left face of the cube, now as the front, then turn_front
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()

    def turn_right(self):
        # must make 3 90 degree rotations of the cube for the right
        # face to face front
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()

    def turn_up(self):
        self.flip_cube(forward=True)
        self.turn_front()
        self.flip_cube()

    def turn_down(self):
        self.flip_cube()
        self.turn_front()
        self.flip_cube(forward=True)

    # ------------------------------------------------------------------------------------------------------------------
    # execute a 180 degree rotation of a given face
    def rotate_face(self, face):
        """
        Rotate a face to 180 degree
        :param face:
        :return:
        """
        new_face = [[], [], []]
        for i in reversed(range(self.size)):
            for y in range(self.size):
                new_face[self.size - 1 - i].append(face[i][self.size - 1 - y])
        return new_face

    # swap the first row of two given faces, in place
    def swap_first_row(self, face1, face2):
        face1_1 = face1[0]
        face2_1 = face2[0]
        # get rest of rows of face1
        new_face1 = [face2_1] + list(face for face in face1[1:])
        # get rest of rows of face2
        new_face2 = [face1_1] + list(face for face in face2[1:])
        return new_face1, new_face2

    # take the last element of each row of face 1, swap in place with
    # first element of reach row of face 2
    def swap_first_last_col(self, face1, face2):
        for i in range(len(face1)):
            face1[i][self.size - 1], face2[i][0] = face2[i][0], face1[i][self.size - 1]
        return face1, face2

    # rotate the cube 90 degrees counter clockwise
    def rotate_cube(self):
        left_face = self.__left__
        self.__left__ = self.replace_face(self.__back__)
        front_face = self.__front__
        self.__front__ = self.replace_face(left_face)
        right_face = self.__right__
        self.__right__ = self.replace_face(front_face)
        self.__back__ = self.replace_face(right_face)
        self.__up__ = self.columns_to_rows(self.__up__, reverse=True)
        self.__down__ = self.columns_to_rows(self.__down__)

    # given a new face, return a copy of this face,
    # to replace a given face of a cube
    def replace_face(self, face):
        new_face = []
        for row in face:
            new_face.append(row)
        return new_face

    # modify a face, rotating its rows to columns, either in left to right
    # or right to left order, depending on the reverse parameter
    def columns_to_rows(self, face, reverse=False):
        new_face = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # left to right order
                if not reverse:
                    row.append(face[self.size - 1 - j][i])
                # right to left order
                else:
                    row.append(face[j][self.size - 1 - i])
            new_face.append(row)
        return new_face

    # flip cube, either forward or backward, and invert
    # faces that must be inverted as a result
    def flip_cube(self, forward=False):
        # if flipping forward, we set front to be up
        # up to be back, back to be down, and down
        # to be front, we must then invert the back and front

        # if flipping backward, we set front to be down
        # up to be front, back to be up, and down to be
        # back, we must then invert the up and down
        if forward:
            self.flip_forward()
            self.__front__ = self.rotate_face(self.__front__)
            self.__back__ = self.rotate_face(self.__back__)
            self.__left__ = self.columns_to_rows(self.__left__)
            self.__right__ = self.columns_to_rows(self.__right__, reverse=True)
        else:
            self.flip_backward()
            self.__up__ = self.rotate_face(self.__up__)
            self.__down__ = self.rotate_face(self.__down__)
            self.__left__ = self.columns_to_rows(self.__left__, reverse=True)
            self.__right__ = self.columns_to_rows(self.__right__)

    # flip cube forward, from perspective of user looking at front
    # flipping such that front goes to down and up comes to front
    def flip_forward(self):
        front = self.__front__
        self.__front__ = self.replace_face(self.__up__)
        down = self.__down__
        self.__down__ = self.replace_face(front)
        back = self.__back__
        self.__back__ = self.replace_face(down)
        self.__up__ = self.replace_face(back)

    # flip cube backward, from perspective of user looking at front
    # flipping such that front goes to up and down goes to front
    def flip_backward(self):
        front = self.__front__
        self.__front__ = self.replace_face(self.__down__)
        up = self.__up__
        self.__up__ = self.replace_face(front)
        back = self.__back__
        self.__back__ = self.replace_face(up)
        self.__down__ = self.replace_face(back)

    # ************** Getters and Setters of the Class ******************************************************************
    def front(self):
        return self.__front__

    def set_front(self, front: List[List[str]]):
        self.__front__ = front

    def back(self):
        return self.__back__

    def set_back(self, back: List[List[str]]):
        self.__back__ = back

    def left(self):
        return self.__left__

    def set_left(self, left: List[List[str]]):
        self.__left__ = left

    def right(self):
        return self.__right__

    def set_right(self, right: List[List[str]]):
        self.__right__ = right

    def up(self):
        return self.__up__

    def set_up(self, up: List[List[str]]):
        self.__up__ = up

    def down(self):
        return self.__down__

    def set_down(self, down: List[List[str]]):
        self.__down__ = down
    # ******************************************************************************************************************
