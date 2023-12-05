

from typing import Any
from typing import List
from typing import Dict
import random
from agent import Agent

__ALPHA = 0.6 #.4  # .6


def QLearning(agent: Agent, discount: float = 0.99, episodes: int = 10, epsilon: float = 0.9) -> None:
    """
    This is known as exploration phase. Perform Q-Learning for a given number of episodes
    :param agent: The agent.
    :param discount: The discount factor, range is (0,1].
    :param episodes: The number of episodes need to be performed.
    :param epsilon: The value of epsilon.
    :return:
    """

    # The current state of the
    # print(agent.current_state)  # six_move_state()

    for i in range(episodes):

        print("\n\n========= EPISODE " + str(i) + " =========")
        print("====== CURRENT STATE =======")
        print("=============================\n")

        # initialize values in Q-State dictionary for
        # any state action pairs including current state
        # that are null
        saved_rewards = agent.current_state.__hash__() in agent.rewards.keys()

        # check if there are no saved rewards, if so then save an empty list for the current state of the cube.
        if not saved_rewards:
            agent.rewards[agent.current_state.__hash__()] = []

        # check if the current state is logged in visit_counter,
        # if not then update the visit counter by 1 for the current state, else increment the counter by 1.
        if not agent.current_state.__hash__ in agent.visit_counter:
            agent.visit_counter[agent.current_state.__hash__()] = 1
        else:
            agent.visit_counter[agent.current_state.__hash__()] += 1

        visit_count = agent.visit_counter[agent.current_state.__hash__()]

        # Initialize Q-Values of 0, for all state action pairs, for the given state if they do not exist. Additionally,
        # check if the saved_rewards is still False, if so then compute the rewards for the given action action and
        # append it to the agent's rewards.
        # If they exist, increment the number of revisits by 1 and break!
        for action in agent.actions:
            if not (agent.current_state.__hash__(), action) in agent.QV.keys():
                agent.QV[(agent.current_state.__hash__(), action)] = 0
            else:
                agent.num_of_revisits += 1
                break

            # After initializing the Q-Value as 0, check if there are 
            # saved rewards if not then compute the rewards for
            # the current action and append it to the agents rewards.
            if not saved_rewards:
                agent.rewards[agent.current_state.__hash__()]\
                    .append(agent.reward_for_action(agent.current_state, action))

        # Check if agent has already reached the goal state!
        if 100 in agent.rewards[agent.current_state.__hash__()]:
            print('Last action for goal state : ', agent.last_action, agent.current_state)
            agent.current_state.is_goal_state_reached()
            print("REACHED GOAL, END Q-LEARN ITERATION")
            return

        # Initialize a random policy value between 0 and 1.
        follow_policy = random.uniform(0, 1.0)
        print("Random follow_policy value generated is " + str(follow_policy))

        # If the random follow_policy number is > epsilon value, we must select best cube_perform_action by
        # the highest Q-Value.
        if follow_policy > epsilon:
            print("\n\nFOLLOWING  RANDOM POLICY")

            for action in agent.actions:
                print("\tQ-Value for action " + action + "\tfrom current state is \t" + str(
                    agent.QV[(agent.current_state.__hash__(), action)]), '\n')

            # Assume there is no best action yet and assign best Q-Value as -10000000.
            best_action = None
            best_QV = -100000000

            # check if the agents current state Q-Value is greater than the present best value,
            # and the current action is not the last action also the current action is not the second last action.
            # If the above conditions are met then we have got our new best action and best Q-Value.
            # this will be repeated for all the possible actions defined for the puzzle.
            for action in agent.actions:
                if (agent.QV[(agent.current_state.__hash__(), action)] > best_QV) \
                        and (action != agent.last_action) \
                        and (action != agent.second_last_action):

                    best_action = action
                    best_QV = agent.QV[(agent.current_state.__hash__(), action)]

            # It may happen that best Q-Value is 0, then chose the best action at random
            if best_QV == 0:
                best_action = random.choice(agent.actions)

                # caution if the best action, when Q-Value is 0, is also the action that was taken in the last
                # cube_perform_action then randomly chose another action other than the last action.
                while best_action == agent.last_action:
                    best_action = random.choice(agent.actions)

            print("\n\t The Best current best action chosen : " + best_action)

            # Increment the Agent`s possible_moves dictionary's with the chosen action by 1
            agent.possible_moves[best_action] = agent.possible_moves[best_action] + 1

            # *********************************************************************************************************
            # *********** Update the Agent's Q-Value table ************************************************************
            # *********************************************************************************************************
            update_agent_QValue_table(agent, discount, visit_count)

            print("\n\t The new Q-Value for \"" + best_action + "\" action is : " + str(
                agent.QV[(agent.current_state.__hash__(), best_action)]))

            agent.current_state.cube_perform_action(best_action)
            agent.current_state = agent.current_state.copy()

            if agent.current_state.is_goal_state_reached():
                print("\n\n reached goal state while in Q-learning epsiode " + str(i), "\n\n")
                # time.sleep(2)
                return

            print("..... agent's last action ..... : ", agent.last_action)
            agent.second_last_action = agent.last_action
            agent.last_action = best_action

        # When the generated random policy number is not greater than the Q-Value
        else:
            # pick a random action
            action = random.choice(agent.actions)
            agent.possible_moves[action] = agent.possible_moves[action] + 1

            # The random chosen action must not be the among the last two actions already performed.
            while (action == agent.last_action) \
                    or (action == agent.second_last_action):
                action = random.choice(agent.actions)

            # *********************************************************************************************************
            # *********** Update the Agent's Q-Value table ************************************************************
            # *********************************************************************************************************
            update_agent_QValue_table(agent, discount, visit_count)

            agent.current_state.cube_perform_action(action)
            agent.current_state = agent.current_state.copy()

            agent.second_last_action = agent.last_action
            agent.last_action = action

            if agent.current_state.is_goal_state_reached():
                print("Reached goal state while in Q-learning episode : " + str(i))
                # time.sleep(2)
                return


def update_agent_QValue_table(agent, discount, visit_count):
    """
    Update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
    alpha times the reward value of the new state plus the discounted max_reward of executing every possible
    action on the new state, minus the original Q-Value
    """
    reward = 0

    for action in agent.actions:
        current_QV = agent.QV[(agent.current_state.__hash__(), action)]
        reward = agent.reward_for_action(agent.current_state, action)
        max_reward = agent.max_reward_for_action(agent.current_state, action)
        agent.QV[(agent.current_state.__hash__(), action)] = \
            current_QV + __ALPHA * (reward + (discount ** visit_count) * max_reward - current_QV)
