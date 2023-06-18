import asyncio
import cv2
import numpy as np
import time

from hume import HumeStreamClient, StreamSocket
from hume.models.config import FaceConfig
from typing import Any, Dict, List

final_emotion = {"Sympathy" : 0, "Surprise (positive)" : 0, "Sadness" : 0, "Romance" : 0, "Pride" : 0, "Pain" : 0, "Nostalgia" : 0, "Love" : 0, "Joy" : 0, "Horror" : 0, "Fear" : 0, "Excitement" : 0, "Doubt" : 0, "Disgust" : 0, "Determination" : 0, "Contentment" : 0, "Confusion" : 0, "Boredom" : 0, "Awe" : 0, "Anger" : 0, "Amusement" : 0, "Adoration" : 0}


camera = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,  480))

def gen_frames():
    t_end = time.time() + 5
    while time.time() < t_end:
        ret, frame = camera.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #frame = cv2.flip(frame, 0)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('frame', frame)
    out.release()
        
async def main():
    client = HumeStreamClient("3yfgKQI2BO49t8Mr8oSg2qnv0QPTAvdH1xBBluugSk5JeWdG")
    config = FaceConfig(identify_faces=True)
    gen_frames()
    async with client.connect([config]) as socket:
        result = await socket.send_file("output.avi")
        print(result)
        n = 0
        while n < 14:
            emotions = result["face"]["predictions"][n]["emotions"]
            print_emotions(emotions)
            n += 1
            

def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Sympathy", "Surprise (positive)", "Sadness", "Romance", "Pride", "Pain", "Nostalgia", "Love", "Joy", "Horror", "Fear", "Excitement", "Doubt", "Disgust", "Determination", "Contentment", "Confusion", "Boredom", "Awe", "Anger", "Amusement", "Adoration"]:
        final_emotion[emotion] += emotion_map[emotion]
        #print(f"- {emotion}: {final_emotion[emotion]:4f}")
n = 0

while True:
        try:
            asyncio.run(main())
            n += 1
            if cv2.waitKey(1) == ord('p'):
                camera.release()
                out.release()
                cv2.destroyAllWindows()
                break

        except:
            print("We could not detect any face anymore")
            camera.release()
            cv2.destroyAllWindows()
            break


if n > 0:
    final_emotion_sorted = dict(sorted(final_emotion.items(), key=lambda x:x[1], reverse=True))
    no = 0
    final_statement = ""
    for emotion in final_emotion_sorted.keys():
        if no < 3: 
            final_statement += emotion + " at " + format((final_emotion_sorted[emotion] /(n*14))*100, ".2f") +"%, "
            no += 1
    print(final_statement)
    
