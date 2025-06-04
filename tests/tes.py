import json

# Load common words from key_word.json
with open("key_word.json", "r") as f:
    common_words_data = json.load(f)

common_words = common_words_data["common_words"]

# Input text
text = "seen any good movies lately"

# Tokenize the text into words
words = text.split()

# Filter the words to keep only the important words (not common words)
important_words = [word for word in words if word.lower() not in common_words]

# Join the important words back into a sentence
important_sentence = " ".join(important_words)

print(important_sentence)
