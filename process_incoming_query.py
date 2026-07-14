import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests

def create_embedding(text):
    r = requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text
    })  # r will be a response object that contains the response from the server. The response object has a method called json() that returns the JSON data from the response as a Python dictionary. In this case, the JSON data contains a key called 'embeddings' that contains the embeddings for the input text. We can access this key using r.json()['embeddings'] to get the embeddings as a list of lists.
    # print("hey",r)
    # print("h",r.json())
    embedding = r.json()['embeddings']
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate",json={
        "model":"llama3.2",
        "prompt":prompt,
        "stream":False
    })
    return r.json()['response']
    

df = joblib.load("embeddings.joblib") # joblib.load() deserializes the DataFrame from the file "embeddings.joblib" and loads it into memory. This allows us to access the DataFrame without having to recreate it from scratch. The resulting DataFrame df will contain the same data as when it was saved, including the 'text', 'chunk_id', and 'embedding' columns for each chunk.



incoming_query = input("Ask a question:")
question_embedding = create_embedding([incoming_query])[0] # 0 is used to get the first element of the list returned by create_embedding(), which is the embedding for the incoming query. The create_embedding() function returns a list of embeddings, and since we are only passing one query, we want to extract the first (and only) embedding from that list.
print("question embedding",question_embedding)  # question embeeding is a 1d array 
similarities = cosine_similarity(np.vstack(df['embedding']), np.array([question_embedding])).flatten()  
# cosine similarity returns a 2D array of shape (n_samples_X, n_samples_Y), where n_samples_X is the number of samples in the first input and n_samples_Y is the number of samples in the second input. In this case, we have one sample in the second input (the question embedding), so the output will be a 2D array with shape (n_samples_X, 1). for example, if we have 5 samples in the first input like [embedding1, embedding2, embedding3, embedding4, embedding5], the output will be a 2D array with shape (5, 1). The flatten() method is used to convert this 2D array into a 1D array of shape (n_samples_X,), which contains the cosine similarity values between the question embedding and each of the embeddings in the first input.
# // flatten convert the 2D array to 1D array

print("similarities",similarities)

Top_index = 5
max_ind = np.argsort(similarities)[-Top_index:][::-1]

# print("max_ind",max_ind)

new_df = df.loc[max_ind]

prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course.
'''
with open("prompt.txt", "w") as f:
    f.write(prompt)


# print("new_df",new_df[['title','text','number']])

for index,item in new_df.iterrows():
    print("item",item['text'],item['title'],item['number'],item['start'],item['end'])

# print("t",create_embedding(["cat sat on the mat","hey cat my name is lakshay"]))

response = inference(prompt)
print("response",response)

with open("response.txt", "w") as f:
    f.write(str(response))