import os
import subprocess


# import os

# folder = r"D:\rag based ai\videos"  # Change to your folder path

# for filename in os.listdir(folder):
#     if filename.endswith(".mp4"):
#         new_name = filename.replace("_1080p60", "")
        
#         old_path = os.path.join(folder, filename)
#         new_path = os.path.join(folder, new_name)
        
#         os.rename(old_path, new_path)
#         print(f"Renamed: {filename} -> {new_name}")

# print("Done!")


files = os.listdir('./videos') # os.listdir() returns a list of all the files and directories in the specified directory. In this case, it returns a list of all the files in the "videos" directory. The list will contain the names of the files as strings, without the full path. For example, if the "videos" directory contains two files named "file1.mp4" and "file2.mp4", then files will be equal to ["file1.mp4", "file2.mp4"].
for file in files:
    lecture_number = (file.split('#')[1])[0:2] #  # file.split('#')[1] splits the filename at the '#' character and takes the second part (index 1) of the resulting list. Then, [0:2] takes the first two characters of that part, which represents the lecture number. For example, if the filename is "Lecture #01 - Introduction.mp4", then file.split('#')[1] will be "01 - Introduction.mp4", and (file.split('#')[1])[0:2] will be "01". This extracts the lecture number from the filename.
    lecture_name = file.split(" _ ")[0] # file.split(" _ ")[0] splits the filename at the " _ " character and takes the first part (index 0) of the resulting list. This represents the lecture name. For example, if the filename is "Lecture #01 - Introduction.mp4", then file.split(" _ ")[0] will be "Lecture #01 - Introduction".
    subprocess.run(["ffmpeg","-i",f"./videos/{file}", f"./audios/{lecture_number} - {lecture_name}.mp3"])
    # subprocess.run() is used to run the ffmpeg command in a subprocess. The command is passed as a list of strings, where each string represents a part of the command. In this case, the command is "ffmpeg -i ./videos/{file} ./audios/{lecture_number} - {lecture_name}.mp3". This command takes the input video file (./videos/{file}) and converts it to an audio file (./audios/{lecture_number} - {lecture_name}.mp3) using ffmpeg. The -i flag specifies the input file, and the output file is specified after that. The resulting audio file will be saved in the "audios" directory with a name that includes the lecture number and lecture name.
print("Done!")

    
  
