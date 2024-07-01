import os
import re
from collections import Counter
import math

def clean_text(input_text):
    cleaned_words = [re.sub(r'[^a-zA-Z]', '', word.lower()) for word in input_text.split()]
    return cleaned_words

def compute_bag_of_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = ' '.join(clean_text(text))
        word_list = cleaned_text.split()
        return Counter(word_list)

def compute_log_probabilities(sentence, play_models, total_words_per_play):
    sentence_words = clean_text(sentence)
    results = {}
    for play, model in play_models.items():
        log_probability = 0
        for word in sentence_words:
            word_count = model.get(word, 0)
            if word_count > 0:
                log_probability += math.log(word_count)
        log_probability += math.log(1 / total_words_per_play[play])  # Adding prior (uniform prior)
        results[play] = log_probability
    return results

def compute_probabilities(results):
    max_log_prob = max(results.values())
    exp_sum = sum(math.exp(log_prob - max_log_prob) for log_prob in results.values())
    probabilities = {play: round(math.exp(log_prob - max_log_prob) / exp_sum * 100) for play, log_prob in results.items()}
    return probabilities

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

    total_words_per_play = {}
    for play, filename in play_filenames.items():
        word_counts = compute_bag_of_words(filename)
        total_words_per_play[play] = sum(word_counts.values())

    play_models = {}
    for play, filename in play_filenames.items():
        play_models[play] = compute_bag_of_words(filename)

    sentence = input().strip()

    if sentence:
        
        results = compute_log_probabilities(sentence, play_models, total_words_per_play)

        probabilities = compute_probabilities(results)

        sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        for play, prob in sorted_probabilities:
            print(f"{play}: {prob}%")
    else:
        print("Input sentence is empty.")

if __name__ == "__main__":
    main()
