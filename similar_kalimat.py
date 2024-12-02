import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_sentences(target_sentence, sentences_list):
    model = api.load("glove-wiki-gigaword-100")  # Menggunakan model GloVe yang telah dilatih sebelumnya
    target_embedding = sum([model[word] for word in target_sentence.split()]) / len(target_sentence.split())

    most_similar_sentences = []
    for sentence in sentences_list:
        sentence_embedding = sum([model[word] for word in sentence.split()]) / len(sentence.split())
        similarity_score = cosine_similarity([target_embedding], [sentence_embedding])[0][0]
        if similarity_score:  # Ubah threshold sesuai kebutuhan
            most_similar_sentences.append(sentence)

    return most_similar_sentences

# Contoh penggunaan
target_sentence = "what is that"
sentences_list = [
    "what is mean",
    "tell me about"
]

similar_sentences = find_similar_sentences(target_sentence, sentences_list)
print(similar_sentences)
