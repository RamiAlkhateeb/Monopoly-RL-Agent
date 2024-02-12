import numpy as np


class RL_Agent:
    def __init__(self ,best_player_in_total,player_total_won_policy):
        self.num_elements = 8
        self.winning_rates = player_total_won_policy
        self.q_values = best_player_in_total
        #self.action_counts = np.zeros(self.num_elements)  # Counts of each action taken
        self.epsilon = 0.2  # Exploration-exploitation parameter

    def select_action(self):
        if np.random.rand() < self.epsilon:
            # Exploration: Randomly choose an action
            key = np.random.choice(list(self.winning_rates))
            return self.winning_rates[key]
        else:
            # Exploitation: Choose the action with the highest estimated value
            return self.winning_rates[max(self.winning_rates.keys())]

    def update_q_values_plus(self,chosen_action, reward ):
        self.q_values = chosen_action
        self.q_values[2] += reward 
        self.q_values[3] += 5 * reward 
        self.q_values[4] += 5 * reward 
        self.q_values[6] += 100 * reward 

        return self.q_values


    def update_q_values_minus(self, chosen_action , reward):
        self.q_values = chosen_action
        self.q_values[2] -= reward 
        self.q_values[3] -= 5 * reward 
        self.q_values[4] -= 5 * reward 
        self.q_values[6] -= 100 * reward 

        return self.q_values
