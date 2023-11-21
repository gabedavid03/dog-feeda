import cv2
import time

def isValid(detection): 
    detection_start_time = time.time()
    detection_threshold = 2 #this is seconds you want to wait until dawg detected 
    detection_valid = False 
    print(f"MAMA WE MADE IT")
    while(1):
        if detection: 
            time.sleep(3) # buffer to get the detection_start_time to catch up to threshold 
            stopwatch = time.time() - detection_start_time
            print(f"{stopwatch}")
            if  stopwatch >= detection_threshold: 
                detection_valid = True 
                print(f"DAWG_STATUS: {detection_valid}")
                cap.release()
                cv2.destroyAllWindows()
                break
            else: 
                print(f"DAWG_STATUS: {detection_valid}")
                detection_start_time = 0
                detection_valid = False 
                break     
   
#opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320), scale=1/255)

#load class list
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

print("object list")
print(classes)
#initialize camera
cap = cv2.VideoCapture(0)

#create a window

while True:
    #get frames
    ret, frame = cap.read()

    #object detection
    (class_ids, score, bboxes)= model.detect(frame)
    for class_id, score, bbox in zip(class_ids, score, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]
        if class_name == "dog":
            cv2.putText(frame, str(class_name), (x,y-5), cv2.FONT_HERSHEY_PLAIN, 1, (200,0,50), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (200,0,50), 3)
            dog_detected = True
            isValid(dog_detected)

    # print("class ids", class_ids)
    # print("score", score)
    # print("bboxes", bboxes)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    # print(key)
    if key == 113:
        break

# cap.release()
# cv2.destroyAllWindows()

