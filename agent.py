# This class defines the Agent for our Rubik's  Cube.


from typing import Dict


import random

from cube import Cube
import utils

_N_SCRAMBLES = 6


class Agent:
    """
    Class level document block

    A cube is an instance of the class State()
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, QValues: Dict = None, cube: Cube = None):

        self.QV = QValues if QValues is not None else {}

        # initialize a cube state,
        # else create an initial random cube state by scrambling cube up 6 moves.

        print("\nThe current state of the Cube is : \t", cube, "\n")
        self.start_state = cube if cube is not None \
            else utils.initial_n_move_state(n=_N_SCRAMBLES)
        print("\nInitial state of the Cube is : ", self.start_state)

        # Initialize the rewards for the Agent. It maps a cube state to multiple
        # rewards possible for performing every possible outcome.
        self.rewards = {}

        # Save the current and previous states.
        self.current_state = self.start_state
        self.previous_state = None

        # Store all possible actions along with last action and second last action of the Agent.
        self.actions = self.start_state.actions
        self.last_action = None
        self.second_last_action = None

        # Maintain visited list, visited count, and number of revisits.
        self.visited = []
        self.visit_counter = {}
        self.num_of_revisits = 0

        # Initialize all the moves to zero, 0.
        self.possible_moves = {"front": 0, "back": 0, "left": 0, "right": 0, "up": 0, "down": 0}

        # Pattern lists for associating the weights with the nodes
        # that are closer to the goal state.

        self.moves_away_from_goal = []

    # ------------------------------------------------------------------------------------------------------------------
    def display(self):
        """ Display the current state of the Agent."""

        print("=============")
        x = 0
        y = 0

        for key in self.QV.keys():
            if self.QV[key] != 0:
                x += 1
            else:
                y += 1

        print("Number of Q values in dictionary is : " + str(x + y))
        print("Number of zero Q values are : " + str(y))
        print("Number of non-zero Q values are : " + str(x))
        print("Number of revisited states are : " + str(self.num_of_revisits))

        # print(self.possible_moves)

    # ------------------------------------------------------------------------------------------------------------------
    def max_reward_for_action(self, cube: Cube, action) -> float:
        """
        Compute the maximum reward that the current state of the cube can get for any possible next single cube_perform_action.
        :param cube: The Cube.
        :param action: One of the action from the list of possible actions
        ['front', 'back', 'left', 'right', 'up', 'down']
        :return: The maximum reward possible from the current state for the next posible cube_perform_action.
        """
        next_cube_state = utils.perform_action(cube, action)

        if not next_cube_state in self.rewards.keys():
            self.rewards[next_cube_state] = []

            for action in self.actions:
                self.rewards[next_cube_state].append(self.reward_for_action(next_cube_state, action))

        return max(self.rewards[next_cube_state])

    # ------------------------------------------------------------------------------------------------------------------
    def reward_for_action(self, cube: Cube, action) -> float:
        """
        The reward function for this Agent.

        The property of the reward function are :
        # this reward function should be a function approximation made up of
        # a set of features, these features should be in decreasing order of priority:
        # 1. solved faces ()
        # use next state to get value for next state vs. self.curr_state, to determine
        # if feature values should be 1 or 0, e.g. if solved_sides(next_state) > solved_sides(self.curr_state)
        # then the solved sides feature is 1, else 0
        """

        next_cube_state = utils.perform_action(cube, action)

        if next_cube_state.is_goal_state_reached():
            print('\n\n\t Current Cube state is :', cube)
            print('\n\t', 'REWARD for the action : ', action, ' : is GOAL\n')
            print('\t Next Cube state is :', next_cube_state)
            return 100

        reward = -0.1

        solved_faces = 2 * (utils.num_of_solved_faces(next_cube_state) < utils.num_of_solved_faces(cube))
        solved_facelets = 0.5 * (
                utils.num_of_solved_facelets(next_cube_state) < utils.num_of_solved_facelets(next_cube_state))

        if (next_cube_state.__hash__(), action) in self.QV.keys():
            reward -= 0.2

        reward -= solved_faces
        reward -= solved_facelets

        return reward

    # ------------------------------------------------------------------------------------------------------------------
    def register_pattern_upto_n_moves(self, move_limit: int = 5):
        """
        This function registers patterns for the cube state such as 1 cube_perform_action away from goal state, 2 moves away from
        the goal state, ... , and n moves away from the goal state.
        :param move_limit:  Number of moves upto which you want to register the patterns. Default value is 5.
        :return: None
        """

        # Initialize the moves_away_list by a list of Nones up to the value of move_limit elements
        self.moves_away_from_goal = [[] for _ in range(move_limit + 1)]

        # Initialize the with the goal state, ie. the new cube is in the goal state.
        _0th_cube_state = Cube()
        self.moves_away_from_goal[0].append(_0th_cube_state)

        i = 0
        for i in range(1, move_limit+1, 1):
            print('\n\t moves_away_list_size[', i - 1, '] : ', len(self.moves_away_from_goal[i - 1]))

            for previous_state in self.moves_away_from_goal[i - 1]:

                for action in self.actions:
                    ith_cube_state = utils.perform_action(previous_state, action)
                    self.moves_away_from_goal[i].append(ith_cube_state)

                    best_ith_QV = (move_limit - i + 1)**2
                    worst_ith_QV = -best_ith_QV

                    # Creating the QValues for the second cube_perform_action
                    for temp_action in self.actions:
                        self.QV[(ith_cube_state.__hash__(), temp_action)] \
                            = best_ith_QV if temp_action == action else worst_ith_QV

        print('\n\t moves_away_list_size[', i, '] : ', len(self.moves_away_from_goal[i]))

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        This will invoke the agent to solve the cube.
        :return:
        """

        # Get the start state for this agent
        self.current_state = self.start_state
        print("\n The Current state of the Cube : \n\t", self.current_state)

        self.second_last_action = None
        self.last_action = None

        for i in range(20):
            print('\n\n\n...............................................................................\n'
                  '............................. Iteration : ', i, '..................................\n',
                  '...............................................................................\n')
            best_action = None
            best_QValue = -100000000

            if not (self.current_state.__hash__(), self.actions[0]) in self.QV.keys():

                best_action = random.choice(self.actions)

                while (best_action == self.second_last_action) or (best_action == self.last_action):
                    best_action = random.choice(self.actions)

                for action in self.actions:
                    self.QV[(self.current_state.__hash__(), action)] = 0

                best_QValue = 0

            else:

                for action in self.actions:

                    if (self.QV[(self.current_state.__hash__(), action)] > best_QValue) \
                            and (action != self.last_action and action != self.second_last_action):

                        best_action = action
                        best_QValue = self.QV[(self.current_state.__hash__(), action)]

                # if best_QV == 0:
                #    best_action = random.choice(self.actions)
                #    while best_action == self.last_action or best_action == self.second_last_action:
                #        best_action = random.choice(self.actions)

            print("Actions chosen : " + best_action)
            print("Last action : " + (self.last_action if self.last_action is not None  else "None"))
            print("Q value is : " + str(self.QV[(self.current_state.__hash__(), best_action)]))

            self.current_state.cube_perform_action(best_action)
            self.second_last_action = self.last_action
            self.last_action = best_action

            print(self.current_state)

            if self.current_state.is_goal_state_reached():
                print('\n\nThe Agent has reached a Goal State in ', i, ' iterations !!!\n\n')

                # time.sleep(5)

                return
