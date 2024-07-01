import os
import re
from collections import Counter
import math

# Function to clean the words
def clean_text(input_text):
    cleaned_words = [re.sub(r'[^a-zA-Z]', '', word.lower()) for word in input_text.split()]
    return cleaned_words

# Function to compute bag-of-words model
def compute_bag_of_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = ' '.join(clean_text(text))
        word_list = cleaned_text.split()
        return Counter(word_list)

# Function to compute probabilities
def compute_probabilities(sentence, play_models):
    sentence_words = clean_text(sentence)
    results = {}
    for play, model in play_models.items():
        log_probability = 0
        for word in sentence_words:
            word_count = model.get(word, 0)
            if word_count > 0:
                log_probability += math.log(word_count)
        results[play] = log_probability
    return results


# Main function
def main():
    play_filenames = {
        "The Merchant of Venice": "merchant.txt",
        "Romeo and Juliet": "romeo.txt",
        "The Tempest": "tempest.txt",
        "Twelfth Night": "twelfth.txt",
        "Othello": "othello.txt",
        "King Lear": "lear.txt",
        "Much Ado About Nothing": "ado.txt",
        "Midsummer Night’s Dream": "midsummer.txt",
        "Macbeth": "macbeth.txt",
        "Hamlet": "hamlet.txt"
    }

    # Compute bag-of-words model for each play
    play_models = {}
    for play, filename in play_filenames.items():
        play_models[play] = compute_bag_of_words(filename)

    # Input sentence
    sentence = input()

    # Compute probabilities
    probabilities = compute_probabilities(sentence, play_models)

    # Determine most likely play
    most_likely_play = max(probabilities, key=probabilities.get)
    print(most_likely_play)

if __name__ == "__main__":
    main()
