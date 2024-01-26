import json
import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import asyncio, websockets
from websockets.server import serve
from helper import landmarks_to_json, landmark_to_json_per_frame

lmrks = []
timeTaken = []
async def detectPose(websocket):
    try:
        #cap = cv2.VideoCapture(1)
        cap = cv2.VideoCapture("C:\dev\Final Year Project\Pose Estimation\Scripts\DemoVids\demo.mp4")
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            i = 0
            while cap.isOpened():
                ret, frame = cap.read()

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                
                startTime = (time.time() * 1000)
                results = pose.process(image)
                endTime = (time.time() * 1000)
                
                timeTakenForFrame = endTime - startTime
                timeTaken.append(timeTakenForFrame)
                
                print(f"Time taken by frame{i}:", timeTakenForFrame)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    response = landmark_to_json_per_frame(results.pose_landmarks.landmark, i)
                    #await websocket.send(json.dumps(response))
                    i += 1
                    lmrks.append(results.pose_landmarks.landmark)
                except:
                    print("No Person Detected")

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                await asyncio.wait(1/15)

            cap.release()
            cv2.destroyAllWindows()
            
    except Exception as e:
        print(e)
        cap.release()
        cv2.destroyAllWindows()


async def main():
    async with serve(detectPose, "localhost", 6969):
        await asyncio.Future()



asyncio.run(main())
    
