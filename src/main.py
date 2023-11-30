import cv2
import time
from controller import send_feed, feed_now, reset_completed, autofeed, COMPORT, validate_feed_time, retrieve_cycles
import time


#opencv DNN variables
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320), scale=1/255)

#load class list for object detection
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

print("object list")
print(classes)
#initialize camera
cap = cv2.VideoCapture(0)

def object_detection() -> None: 
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

    print("class ids", class_ids)
    print("score", score)
    print("bboxes", bboxes)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    print(key)
    return

def isValid(detection: bool) -> None: 
    detection_start_time = time.time()
    detection_threshold = 2 #this is seconds you want to wait until dawg detected 
    detection_valid = False 
    print(f"MAMA WE MADE IT")
    while True:
        if detection: 
            time.sleep(3) # buffer to get the detection_start_time to catch up to threshold 
            stopwatch = time.time() - detection_start_time
            print(f"{stopwatch}")
            if  stopwatch >= detection_threshold: 
                detection_valid = True 
                print(f"DAWG_STATUS: {detection_valid}")
                valid = validate_feed_time()
                if (valid != 0): 
                    cycles = retrieve_cycles(valid) 
                    send_feed(COMPORT, cycles)
                break
            else: 
                print(f"DAWG_STATUS: {detection_valid}")
                detection_start_time = 0
                detection_valid = False 
                break     
   
# while loop where all of the code run

def main(args=None) -> None:
    while True: 
        feed_now()
        reset_completed()
        autofeed() 
        object_detection()

if __name__ == '__main__':
        try:
            main()
        except Exception as e:
            print(e)