import numpy as np
import random
from typing import List, Tuple

POSSIBLE_CARDS = ['A', '2', '3', '4', '5', '6', '7', '8',
				  '9', '10', 'J', 'Q', 'K']

LEARNING_EPISODES = 5_000_000

def draw_card():
    return random.choice(POSSIBLE_CARDS)

def gen_exploring_starts_state() -> Tuple[int, int, int]:
    player_hand = random.randrange(12, 22)
    player_has_usable_ace = random.randrange(2)
    dealer_hand = random.randrange(2, 12)
    return player_hand, player_has_usable_ace, dealer_hand

def gen_random_action() -> int:
    return random.randint(0,1)

class Episode():
    def __init__(
        self, 
        player_policy = np.array, 
        exploring_starts = False, 
        verbose = False
    ):
        self.player_cards = []
        self.dealer_cards = []
        self.player_policy = player_policy
        self.ace_override = False
        self.exploring_starts = exploring_starts

        if exploring_starts:
            player_hand, player_has_usable_ace, dealer_hand = gen_exploring_starts_state()
            self.player_cards.append(player_hand)
            self.ace_override = player_has_usable_ace # there's an ace in the ES hand
            self.dealer_cards.append(dealer_hand)
        else:
            self.player_cards.append(draw_card())
            self.player_cards.append(draw_card())
            self.player_count = self.count_hand(self.player_cards, self.ace_override)
            while self.player_count < 12: # it's non sensical to stay below 12
                self.player_cards.append(draw_card())
                self.player_count = self.count_hand(self.player_cards, self.ace_override)

            self.dealer_cards.append(draw_card())

        self.player_count = self.count_hand(self.player_cards, self.ace_override)
        self.dealer_count = self.count_hand(self.dealer_cards)

        self.steps = []
        self.player_play_policy()

        if self.player_count <= 21:
            self.dealer_play()

        self.result = self.calculate_result(self.player_cards, self.dealer_cards)

        if verbose:
            print(f"Player cards: {' '.join([str(val) for val in self.player_cards])}")
            print(f"Player count: {self.player_count}")
            print(f"Dealer cards: {' '.join([str(val) for val in self.dealer_cards])}")
            print(f"Dealer count: {self.dealer_count}")
            print(f"Result: {self.result}")

    def player_play_policy(self):
        self.player_count = self.count_hand(self.player_cards, self.ace_override)
        self.player_has_ace = self.hand_has_ace(self.player_cards, self.ace_override)
        self.dealer_count = self.count_hand(self.dealer_cards)
        state = (self.player_count, self.player_has_ace, self.dealer_count)
        policy_state = self.transform_state_to_policy_state(state)
        
        if self.exploring_starts: # the first action is random
            random_action = gen_random_action()
            state_action_pair = (*state, random_action)
            self.steps.append(state_action_pair)
            if random_action:
                self.player_cards.append(draw_card())
                self.player_count = self.count_hand(self.player_cards, self.ace_override)
                self.player_has_ace = self.hand_has_ace(self.player_cards, self.ace_override)
                state = (self.player_count, self.player_has_ace, self.dealer_count)
                policy_state = self.transform_state_to_policy_state(state)
            else:
                return # if action == 0 we have already added to self.steps before the if

        while self.player_count <= 21:
            if self.player_policy[policy_state] == 1: 
                state_action_pair = (*state, 1) # hit
                self.steps.append(state_action_pair)
                self.player_cards.append(draw_card())
                self.player_count = self.count_hand(self.player_cards, self.ace_override)
                self.player_has_ace = self.hand_has_ace(self.player_cards, self.ace_override)
                state = (self.player_count, self.player_has_ace, self.dealer_count)
                policy_state = self.transform_state_to_policy_state(state)
            else:
                state_action_pair = (*state, 0) # stay
                self.steps.append(state_action_pair)
                break

    def transform_state_to_policy_state(self, state: Tuple[int, int, int]) -> Tuple[int, int, int]:
        return state[0] - 12, state[1], state[2] - 2

    def dealer_play(self):
        if self.player_count > 21: # player have busted, dealer is not forced to proceed
            return
        while self.dealer_count < 17:# or (self.player_count <= 21 and self.player_count > self.dealer_count):
            self.dealer_cards.append(draw_card())
            self.dealer_count = self.count_hand(self.dealer_cards, self.ace_override)

    def calculate_result(self, player_hand: List[str], dealer_hand: List[str]) -> int:
        """
        Returns 1 if player wins, 0 if draw, -1 if dealer wins.
        """
        player_count = self.count_hand(player_hand, self.ace_override)
        dealer_count = self.count_hand(dealer_hand, self.ace_override)
        if player_count > 21: return -1
        elif player_count <= 21 and dealer_count > 21: return 1
        elif player_count == dealer_count: return 0
        elif player_count > dealer_count: return 1
        else: return -1

    def count_hand(self, hand: List[str], ace_override = False) -> int:
        hand_sum = 0
        ace_count = 0
        for card in hand:
            if type(card) == str:
                if card == 'A':
                    ace_count += 1
                elif card >= '2' and card <= '9':
                    hand_sum += int(card)
                else:
                    hand_sum += 10
            else:
                hand_sum += card
        if hand_sum > 21 and ace_override:
            hand_sum -= 10
        
        for used_aces in reversed(range(1, ace_count + 1)):
            if hand_sum + 11 * used_aces + (ace_count - used_aces) <= 21:
                return hand_sum + 11 * used_aces + (ace_count - used_aces)
        return hand_sum + 1 * ace_count

    def hand_has_ace(self, hand: List[str], ace_override: bool) -> int:
        if 'A' in hand or ace_override: # ace_override for exploring starts
            return 1
        return 0

# possible states

# player_sum: 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 : 10 values
# if player_sum is 10 or below he will obviously hit

# has_ace: 0 or 1 whether the player has the ace : 2 values

# dealer_sum: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 : 10 values
# card the player revealed at the beginning of the game 

# state space player_sum x has_ace x dealer_sum

# action: 0: stay, 1: hit

if __name__ == '__main__':
    q = np.random.uniform(-0.5, 0.5, size=(10, 2, 10, 2))
    returns = np.zeros(shape = (10, 2, 10, 2))
    count = np.zeros(shape = (10, 2, 10, 2))
    policy = np.random.randint(low = 0, high = 2, size = (10, 2, 10))

    for i in range(LEARNING_EPISODES):
        episode = Episode(player_policy = policy, exploring_starts = True, verbose = False)
        previous_states = set()
        result = episode.result
        for state_action_pair in episode.steps:
            player_sum, has_ace, dealer_sum, action = state_action_pair
            if state_action_pair in previous_states:
                continue
            previous_states.add(state_action_pair)
            state_action_pair = (player_sum - 12, has_ace, dealer_sum - 2, action)
            state = (player_sum - 12, has_ace, dealer_sum - 2)
            returns[state_action_pair] += result
            count[state_action_pair] += 1
            q[state_action_pair] = returns[state_action_pair] / count[state_action_pair]
            policy[state] = np.argmax(q[player_sum - 12, has_ace, dealer_sum - 2, :])

    from graphs import plot_count, plot_q, plot_policy
    plot_policy(policy)
    plot_q(q)
    plot_count(count)
