import cv2
import time
from controller import send_feed, feed_now, reset_completed, autofeed, COMPORT, validate_feed_time, retrieve_cycles
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import cv2 


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

# initialize PiCamera
camera = PiCamera()
camera.resolution = (320, 320)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 320))

def object_detection() -> None:
    for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = capture.array

        # Object detection
        class_ids, scores, bboxes = model.detect(image)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            x, y, w, h = bbox
            class_name = classes[class_id]
            if class_name == "dog":
                cv2.putText(image, str(class_name), (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 50), 2)
                cv2.rectangle(image, (x, y), (x + w, y + h), (200, 0, 50), 3)
                dog_detected = True
                isValid(dog_detected)

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord("q"):
            break

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
    return    
   
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
    finally:
        camera.close()  # Properly close the camera resource
        cv2.destroyAllWindows()  # Close all OpenCV windows