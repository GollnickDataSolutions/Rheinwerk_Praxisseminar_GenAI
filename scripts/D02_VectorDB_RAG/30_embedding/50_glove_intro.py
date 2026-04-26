#%%
import torch
# import torchtext.vocab as vocab

# %% import GloVe
import requests
import zipfile
import io
import os

glove_url = "https://nlp.stanford.edu/data/glove.6B.zip"
glove_path = "glove.6B.50d.txt"

if not os.path.exists(glove_path):
    print("Downloading GloVe embeddings...")
    r = requests.get(glove_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extract(glove_path)
    print("Download complete.")
    
#%% load the glove embeddings
with open(glove_path, 'r', encoding='utf-8') as f:
    glove = f.readlines()
    
# glove word list
glove_words = [line.split()[0] for line in glove]

# glove embeddings
glove_embeddings = [torch.tensor([float(val) for val in line.split()[1:]]) for line in glove]



#%%
def get_embedding_vector(word):
    word_index = glove_words.index(word)
    emb = glove_embeddings[word_index]
    return emb

def get_closest_words_from_word(word, max_n=5):
    word_emb = get_embedding_vector(word)
    distances = [(w, torch.dist(word_emb, get_embedding_vector(w)).cpu().item()) for w in glove_words]
    dist_sort_filt = sorted(distances, key=lambda x: x[1])[:max_n]
    return dist_sort_filt


#%%
get_closest_words_from_word('chess')

# %% Get an embedding vector
def get_embedding_vector(word):
    word_index = glove.stoi[word]
    emb = glove.vectors[word_index]
    return emb

word_emb = get_embedding_vector('man')

#%% Find closest words based on input word
def get_closest_words_from_word(word, max_n=5):
    word_emb = get_embedding_vector(word)
    distances = [(w, torch.dist(word_emb, get_embedding_vector(w)).cpu().item()) for w in glove.itos]
    dist_sort_filt = sorted(distances, key=lambda x: x[1])[:max_n]
    return dist_sort_filt

get_closest_words_from_word('chess')

#%% 
def get_closest_words_from_embedding(word_emb, max_n=5):
    distances = [(w, torch.dist(word_emb, get_embedding_vector(w)).cpu().item()) for w in glove.itos]
    dist_sort_filt = sorted(distances, key=lambda x: x[1])[:max_n]
    return dist_sort_filt


# %% Find Word Analogies
# e.g. King is to Queen as Man is to Woman
def get_word_analogy(word1, word2, word3, max_n=5):
    # logic w1=king, w2=man, w3=woman --> w4 queen
    # w1 - w2 + w3
    word1_emb = get_embedding_vector(word1)
    word2_emb = get_embedding_vector(word2)
    word3_emb = get_embedding_vector(word3)
    word_diff = word1_emb - word2_emb + word3_emb
    analogy = get_closest_words_from_embedding(word_diff)
    return analogy[1][0]

analogy = get_word_analogy(word1='sister', 
                           word2='brother', 
                           word3='nephew')
analogy
# %%
