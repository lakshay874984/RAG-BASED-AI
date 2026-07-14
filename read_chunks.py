import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib


def create_embedding(text):
    r = requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text
    })  # r will be a response object that contains the response from the server. The response object has a method called json() that returns the JSON data from the response as a Python dictionary. In this case, the JSON data contains a key called 'embeddings' that contains the embeddings for the input text. We can access this key using r.json()['embeddings'] to get the embeddings as a list of lists.
    # print("hey",r)
    print("h",r.json())
    embedding = r.json()['embeddings']
    return embedding
jsons = os.listdir("jsons") # os.listdir() returns a list of all the files and directories in the specified directory. In this case, it returns a list of all the files in the "jsons" directory. The list will contain the names of the files as strings, without the full path. For example, if the "jsons" directory contains two files named "file1.json" and "file2.json", then jsons will be equal to ["file1.json", "file2.json"].
my_dict = []
chunk_id = 1
for json1 in jsons:
    with open(f"jsons/{json1}","r",encoding="utf-8") as f:
        read_json = json.load(f) # json.load() reads the JSON data from the file and converts it into a Python dictionary. In this case, it reads the JSON data from the file "jsons/{json1}" and stores it in the variable read_json. The read_json variable will be a dictionary that contains the data from the JSON file. For example, if the JSON file contains {"chunks": [{"text": "chunk1"}, {"text": "chunk2"}]}, then read_json will be equal to {"chunks": [{"text": "chunk1"}, {"text": "chunk2"}]}.
    embeddings2 = create_embedding([c['text'] for c in read_json["chunks"]]) # create_embedding() takes a list of strings as input and returns a list of embeddings for each string. In this case, we are passing a list of the 'text' values from each chunk in the read_json dictionary. The result will be a list of embeddings corresponding to each chunk's text.
    # print(embeddings)
    for i,chunk in enumerate(read_json["chunks"]):
        chunk['chunk_id'] = chunk_id
        chunk["embedding"] = embeddings2[i]
        chunk_id +=1
        # print(chunk)
        my_dict.append(chunk)

    
# print(my_dict)
df = pd.DataFrame.from_records(my_dict) # from_records() creates a DataFrame from a list of dictionaries. Each dictionary in the list represents a row in the DataFrame, and the keys of the dictionaries represent the column names. In this case, my_dict is a list of dictionaries where each dictionary contains information about a chunk, including its 'text', 'chunk_id', and 'embedding'. The resulting DataFrame df will have columns corresponding to these keys and rows corresponding to each chunk.
print(df)
joblib.dump(df,"embeddings.joblib") # joblib.dump() serializes the DataFrame df and saves it to a file named "embeddings.joblib". This allows us to save the DataFrame to disk so that we can load it later without having to recreate it from scratch. The resulting file "embeddings.joblib" will contain the serialized representation of the DataFrame, which can be loaded back into memory using joblib.load().







# incoming_query = input("Ask a question:")
# question_embedding = create_embedding([incoming_query])[0] # 0 is used to get the first element of the list returned by create_embedding(), which is the embedding for the incoming query. The create_embedding() function returns a list of embeddings, and since we are only passing one query, we want to extract the first (and only) embedding from that list.
# print("question embedding",question_embedding)  # question embeeding is a 1d array 
# similarities = cosine_similarity(np.vstack(df['embedding']), np.array([question_embedding])).flatten()  
# # cosine similarity returns a 2D array of shape (n_samples_X, n_samples_Y), where n_samples_X is the number of samples in the first input and n_samples_Y is the number of samples in the second input. In this case, we have one sample in the second input (the question embedding), so the output will be a 2D array with shape (n_samples_X, 1). for example, if we have 5 samples in the first input like [embedding1, embedding2, embedding3, embedding4, embedding5], the output will be a 2D array with shape (5, 1). The flatten() method is used to convert this 2D array into a 1D array of shape (n_samples_X,), which contains the cosine similarity values between the question embedding and each of the embeddings in the first input.
# # // flatten convert the 2D array to 1D array

# print("similarities",similarities)

# Top_index = 3
# max_ind = np.argsort(similarities)[-Top_index:][::-1]

# print("max_ind",max_ind)

# new_df = df.loc[max_ind]

# print("new_df",new_df)
# # print("t",create_embedding(["cat sat on the mat","hey cat my name is lakshay"]))

