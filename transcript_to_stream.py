import time

def send_transcript_thread(transcript, shutdown, file, words=10, timestep=5): 
    print("Starting send_transcript thread!")
    content = ''
    with open(file,"r") as f:
        content = f.read()
    lines = content.split('.')
    
    i = 0
    while not shutdown.is_set() and i < len(lines):
        transcript.append(lines[i] + '. ')
        i += 1
        time.sleep(timestep)
    print("ending send_transcript")
