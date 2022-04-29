# blackjack
Reinforcement Learning project for policy optimization of simple blackjack player agent with Monte Carlo Exploring Starts.

The algorithm is based on the book Reinforcement Learning: An Introduction Chapter 5: Monte Carlo Methods by Richard Sutton and Andrew Barto.

The general ideia of this project is to find the optimal play of a blackjack player playing against the dealer by playing the game a large number of times until the optimal policy (map from state to action) is found.

A state is represented by a tuple, the sum of the player cards, the first card of the dealer and whether the player has an ace. 
A state action pair is a tuple consisting of the combination of a state and an action.
The assumption that each card is drawn from a new deck (with reposition) is used, such that the cards already dealt have no impact on future cards.
Exploring starts means that for each episode (game) of the learning algorithm the starting point is random such that we guarantee that all initial state action pairs have a sufficient number of occurences (infinity on the limit). 
Initially the agent starts with a random policy (random probability of hitting or sticking given any state). 
As it tries different actions, for any given state it appends the result of the game to the state action pair. 
At the end of the episode the algorithm updates its policy by being greedy (choosing the best policy, hitting or sticking) for each state.

A detailed description of Monte Carlo Exploring Starts and the algorithmic scheme can be found on page 99 second edition of the referenced book.

## Random initial Policy
If the policy value is zero the player is supposed to stick with her current hand, if one, to hit. <br/><br/>
![random_start](https://user-images.githubusercontent.com/25706305/165876049-49213ee5-7168-48d2-98e9-caba040a464f.png)

## Policy after about 20m games
![policy_result](https://user-images.githubusercontent.com/25706305/165876059-56bcd992-0ec1-4f25-8086-409707876f0c.png)

## Q values after 20m games
![Q](https://user-images.githubusercontent.com/25706305/165876063-c78cf97c-95f2-470a-bf6b-4bcf4f587db1.png)
