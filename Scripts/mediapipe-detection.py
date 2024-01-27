import mediapipe as mp
import asyncio, websockets, threading, json, cv2, time
from websockets.server import serve
from helper import landmark_to_json_per_frame
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

response = None
stopServer = threading.Event()

def detectPose():
    global response
    global stopServer
    try:
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture('C:\dev\Final Year Project\MediaPipe Pose Estimation\Scripts\DemoVids\demo.mp4') #- for demosS
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
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    response = json.dumps(landmark_to_json_per_frame(results.pose_landmarks.landmark, i))
                    print(f"LOG::Frame Detection Success::Time taken by frame{i}:", timeTakenForFrame)
                    i += 1
                except:
                    print("LOG::No Person Detected")
                
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                
                cv2.imshow("Mediapipe Window",image)
                
                if (cv2.waitKey(10) & 0xFF == ord('q')):
                    break

            cap.release()
            cv2.destroyAllWindows()            
            
            
    except Exception as e:
        print("LOG::Exception::" + str(e))
        cap.release()
        cv2.destroyAllWindows()
        
async def mainServer(websocket, path):
    global response
    global stopServer
    while True:
        if response != None:
            await websocket.send(response)
            response = None
        await asyncio.sleep(1/15)
    

if "__main__" == __name__:
    try:
        stopServer == False
        detectPoseThread = threading.Thread(target=detectPose, daemon=True)
        detectPoseThread.start()
        
        start_server = serve(mainServer, "localhost", 6969)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("LOG::Server has been stopped")
              

    
