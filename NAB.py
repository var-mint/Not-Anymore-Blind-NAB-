#NOT ANYMORE BLIND (NAB)
    #    NAB is an openCV Project which provide guidence for blind people. It helps them to walk without the help of a walking stick or a person.
    #    The camera(webcam) here detects multiple objects infront of it and if the program identifies it as an obstacle it will measure the distance
    #    between the obstacle and the camera(webcam) and then convert the measured distance from text to speech and gives a voice output,which helps
    #    the blind people to identify obstacles infront of them easly.


# Importing libraries
import cv2
import pyttsx3


# Initialize the text-to-speech engine
engine = pyttsx3.init()

distance = 0
# Placeholder values for camera calibration
focal_length = 100  # in pixels
object_actual_size = 0.5  # in meters
# Placeholder threshold for obstacle detection
threshold_distance = .5  # in meters

# Main loop to capture frames from webcam
cap = cv2.VideoCapture(0)  # default webcam

if not cap.isOpened():
    print("Error: Unable to open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Unable to capture frame.")
        break
    
    cv2.imshow('Frame without Obstacles', frame)

    # Convert frame to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Perform edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours of objects
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Flag to check if obstacles are detected
    obstacle_detected = False
    
    
    
    # Draw bounding boxes around detected objects and check for obstacles
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate object size in pixels (maximum of width or height)
        object_size_in_pixels = max(w, h)
        
        # Calculate distance from the camera
        distance = focal_length * object_actual_size / object_size_in_pixels
    
    
    # Display the frame with obstacle detection
    cv2.imshow('Frame with Obstacles', frame)

    if distance < threshold_distance:
            # Convert distance to string
            distance_str = "{:.2f} meters".format(distance)
            # Speak the distance
            engine.say("Obstacle detected at " + distance_str)
            
            
            # engine.stop()
            obstacle_detected = True
            engine.runAndWait()
    
    # Check if obstacle is detected
    if obstacle_detected:
        print("Obstacle detected!")
    
    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()