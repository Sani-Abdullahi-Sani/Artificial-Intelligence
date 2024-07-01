def rain_prob_extended(observations, num_future_days):

    # Transition matrix
    P_rain_given_rain = 0.7
    P_rain_given_norain = 0.3

    # Emission Probabilities
    P_umbrella_given_rain = 0.9
    P_umbrella_given_norain = 0.2

    # Initial probability distribution - Assume a uniform prior
    p_rain = 0.5
    p_norain = 0.5

    # List to store probabilities of rain at each timestep n
    P_s_n = [round(p_rain, 3)]

    # Process observations
    for observation in observations:
        # Prediction step
        rain_predicted = P_rain_given_rain * p_rain + P_rain_given_norain * p_norain
        norain_predicted = 1 - rain_predicted

        # Update step based on observation (1 for umbrella, 0 for no umbrella)
        if observation == 1:
            likelihood_rain = P_umbrella_given_rain
            likelihood_norain = P_umbrella_given_norain
        else:
            likelihood_rain = 1 - P_umbrella_given_rain
            likelihood_norain = 1 - P_umbrella_given_norain

        # Update beliefs with the Forward algorithm - Posterior
        updated_rain = rain_predicted * likelihood_rain
        updated_norain = norain_predicted * likelihood_norain

        # Normalize probabilities to ensure they sum up to 1
        normalizing_constant = updated_rain + updated_norain
        p_rain = updated_rain / normalizing_constant
        p_norain = updated_norain / normalizing_constant

        P_s_n.append(round(p_rain, 3))

    # Predict future days without new observations
    for _ in range(num_future_days):

        # Use only transition probabilities since no new observation is available
        future_rain = P_rain_given_rain * p_rain + P_rain_given_norain * p_norain
        future_norain = 1 - future_rain

        p_rain = future_rain
        p_norain = future_norain

        P_s_n.append(round(p_rain, 3))

    return P_s_n


user_input = input()
observations = list(map(int, user_input.split()))

probability_of_rain = rain_prob_extended(observations, num_future_days=2)

for i, prob in enumerate(probability_of_rain):
    print(f'Timestep {i}: {prob}')
