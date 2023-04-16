import time

def send_transcript_thread(transcript, shutdown, words=10, timestep=5): 
    print("Starting send_transcript thread!")
    lecture=""
    with open("example_lecture.txt","r") as f:
        lecture=f.readlines()
    print(lecture)
    while not shutdown.is_set():
        text=lecture[:words]
        text=text[words:]
        transcript.append(text + ' ')
        print(transcript.get_full())
        time.sleep(timestep)
    print("ending send_transcript")