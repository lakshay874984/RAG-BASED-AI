import whisper
import json
import os

model = whisper.load_model("large-v2")

audios = os.listdir("./audios")
print(audios)

for audio in audios: 
    if(" - " in audio):
        number = audio.split(" - ")[0] # audio.split(" - ")[0] splits the filename at the " - " character and takes the first part (index 0) of the resulting list. This represents the lecture number. For example, if the filename is "01 - Introduction.mp3", then audio.split(" - ")[0] will be "01".
        title = audio.split(" - ")[1][:-4] # audio.split(" - ")[1] splits the filename at the " - " character and takes the second part (index 1) of the resulting list. Then, [:-4] removes the last 4 characters (".mp3") from that part, which represents the lecture title. For example, if the filename is "01 - Introduction.mp3", then audio.split(" - ")[1][:-4] will be "01 - Introduction".
        print(number, title)
        result = model.transcribe(audio = f"audios/{audio}",
                              language="hi",
                              task="translate",
                              word_timestamps=False )
                              # syntax of model.transcribe() is model.transcribe(audio, language, task, word_timestamps). The audio parameter specifies the path to the audio file to be transcribed. The language parameter specifies the language of the audio. The task parameter specifies the task to be performed, which can be "transcribe" or "translate". The word_timestamps parameter specifies whether to include word-level timestamps in the output. In this case, we are transcribing the audio file located at "audios/{audio}" in Hindi language, translating it to English, and not including word-level timestamps in the output.and will give a output for example if the audio file is "01 - Introduction.mp3", then the output will be a dictionary with keys "text" and "segments". The "text" key will contain the transcribed text of the audio, and the "segments" key will contain a list of segments, where each segment is a dictionary with keys "start", "end", and "text" representing the start time, end time, and transcribed text of that segment, respectively.
        
        chunks = []
        for segment in result["segments"]:
            chunks.append({"number": number, "title":title, "start": segment["start"], "end": segment["end"], "text": segment["text"]})
        
        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        with open(f"jsons/{audio}.json", "w") as f:
            json.dump(chunks_with_metadata,f) # json.dump() writes the chunks_with_metadata dictionary to a JSON file located at "jsons/{audio}.json". The f-string f"jsons/{audio}.json" constructs the file path by inserting the value of the audio variable into the string. For example, if the audio variable is "01 - Introduction.mp3", then the file path will be "jsons/01 - Introduction.mp3.json". The resulting JSON file will contain the transcribed text and segments of the audio file in a structured format.