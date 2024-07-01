import re

def clean_text(input_text):
    
    cleaned_words = [re.sub(r'[^a-zA-Z]', '', word.lower()) for word in input_text.split()]
    
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text

input_text = input()

cleaned_text = clean_text(input_text)

print()
print(cleaned_text)
