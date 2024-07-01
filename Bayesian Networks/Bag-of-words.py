import re
from collections import Counter

def clean_text(input_text):
   
    cleaned_words = [re.sub(r'[^a-zA-Z]', '', word.lower()) for word in input_text.split()]
    
    return cleaned_words

def count_words(filename):
    word_counts = Counter()
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = clean_text(line)
            word_counts.update(cleaned_line)
    
    return word_counts

def top_three_common_words(word_counts):
    top_words = word_counts.most_common(3)
    return [word[0] for word in top_words]

filename = input()

word_counts = count_words(filename)

top_three_words = top_three_common_words(word_counts)

print()
print(' '.join(top_three_words))