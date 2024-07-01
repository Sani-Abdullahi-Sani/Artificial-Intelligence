# Weather Prediction

## Introduction

In this Task, we implemented algorithms on Hidden Markov Models (HMM) to predict weather conditions. Specifically, we modelled two weather conditions: rainy and not rainy, using data collected over several days. 

### Data
- If it was raining yesterday, there is a 70% chance it will rain today.
- If it was not raining yesterday, there is a 30% chance it will rain today.
- On rainy days, our neighbor leaves home with an umbrella 90% of the time.
- On non-rainy days, our neighbor leaves home with an umbrella 20% of the time.

## Task 1: Today’s Weather

We aim to predict the probability of rain at each timestep given a sequence of observations of our neighbor carrying an umbrella.

### Input
A single line containing 0s and 1s separated by spaces, where each integer represents whether an umbrella was observed (1) or not (0) at each timestep.

### Output
For each timestep (including timestep 0), output the probability that it is raining, rounded to 3 decimal places.

### Example
**Input:**
```
1 1
```
**Output:**
```
Timestep 0: 0.5
Timestep 1: 0.818
Timestep 2: 0.883
```

## Task 2: Tomorrow’s Weather

Using the model from Submission 1, we extend our predictions two timesteps into the future.

### Input
A single line containing 0s and 1s separated by spaces, where each integer represents whether an umbrella was observed (1) or not (0) at each timestep.

### Output
The output should include probabilities for two additional future timesteps beyond the observations.

### Example
**Input:**
```
1 1
```
**Output:**
```
Timestep 0: 0.5
Timestep 1: 0.818
Timestep 2: 0.883
Timestep 3: 0.653
Timestep 4: 0.561
```

## Task 3: Some Questions

### Some Key Questions we try to answer:
1. What happens when we try to make predictions many timesteps into the future without evidence?
2. How are these far-off predictions affected by the prior distribution? What if you assign a prior probability of 1 to rain?
3. What is the effect on these future predictions if the transition probabilities are changed?

### Observations
1. **Predictions without Evidence:**
   - When making predictions many timesteps into the future without new evidence, the probabilities tend to converge to their initial value, which is 0.5.

2. **Effect of Prior Distribution:**
   - Assigning a prior probability of 1 to rain results in the probabilities still converging to 0.5 over time, indicating that the prior distribution affects only the initial predictions and doesn't have a lasting impact without new evidence.

3. **Effect of Transition Probabilities:**
   - Changing the transition probabilities leads to a convergence over time that aligns with the new transition probabilities. For example, decreasing the transition probability (P(Rain | rain)) results in future predictions decreasing from 0.5 to 0.333 and then to 0.241.

