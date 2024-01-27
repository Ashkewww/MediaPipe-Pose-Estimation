import json

names = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST',
             'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

def landmarks_to_json(landmrk):
    response = {}
    for i, frame in enumerate(landmrk):
        frm = {}
        for j, landmark in enumerate(frame):
            temp = {}
            temp["posx"] = landmark.x
            temp["posy"] = landmark.y
            temp["posz"] = landmark.z
            temp["visibility"] = landmark.visibility
            frm[names[j]] = temp
        response['frame' + str(i+1)] = frm

    return response


def landmark_to_json_per_frame(frame, indexOfFrame):
    response = {}
    response['status'] = "Success"
    response['frameNumber'] = indexOfFrame
    landmarks = {}
    for i, landmark in enumerate(frame):
        temp = {}
        temp["posx"] = landmark.x
        temp["posy"] = landmark.y
        temp["posz"] = landmark.z
        temp["visibility"] = landmark.visibility
        landmarks[names[i]] = temp
    response["landmarks"] = landmarks
    return json.dumps(response)

def person_not_found_status():
    response = {}
    response['status'] = "Failure"
    return json.dumps(response)
    
    
        
        