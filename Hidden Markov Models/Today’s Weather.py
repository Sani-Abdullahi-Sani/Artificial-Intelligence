def rain_prob(observations):
   
    # Transition matrix
    P_rain_given_rain = 0.7
    P_rain_given_norain = 0.3

    # Emission Probabilities of umb given rain or not
    P_umbrella_given_rain = 0.9
    P_umbrella_given_norain = 0.2

    # Initial probability distribution - Assume a uniform prior
    p_rain = 0.5
    p_norain = 0.5

    # Initialise a list to store probabilities of rain at each timestep n

    P_s_n = [round(p_rain, 3)]

    # Observation processes
    for observation in observations:
        # Prediction for rain tomorrow
        rain_predicted = (P_rain_given_rain * p_rain) + (P_rain_given_norain * p_norain)
        norain_predicted = 1 - rain_predicted

        # Update setps based on observations- 1 for umbrella, 0 for no umbrella
        if observation == 1:
            # likelihood of seeing an umbrella
            likelihood_rain = P_umbrella_given_rain
            likelihood_norain = P_umbrella_given_norain

        else:
            # likelihood of not seeing an umbrella
            likelihood_rain = 1 - P_umbrella_given_rain
            likelihood_norain = 1- P_umbrella_given_norain

        # Update beliefs with forward algorithm - Posteriori
        updated_rain = rain_predicted * likelihood_rain
        updated_norain = norain_predicted * likelihood_norain

        # Normalise probabilities to ensure they sum up to 1
        normalising_constant = updated_rain + updated_norain
        p_rain = updated_rain / normalising_constant
        p_norain = updated_norain / normalising_constant

        P_s_n.append(round(p_rain, 3))
    
    return P_s_n

# Input
user_input = input()
observations = list(map(int, user_input.split()))

probability_of_rain = rain_prob(observations)
# Output
for i, prob in enumerate(probability_of_rain):
    print(f'Timestep {i}: {prob}')
          