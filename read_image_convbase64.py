import rospy
from sensor_msgs.msg import Image
import base64
import serial
import time
import cv2
import numpy as np

def resize_image(image, width, height):
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def image_callback(msg):
    try:
        # Convert the Image message to a NumPy array
        img_np = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, -1)

        # Resize the image to a smaller resolution (e.g., 640x480)
        resized_img = resize_image(img_np,30,30)
        #max json 30*30

        # Convert the resized image to base64
        img_data = base64.b64encode(resized_img.tobytes())
        img_str = img_data.decode('utf-8')
        ser = serial.Serial('/dev/ttyUSB0', 115200)  # Change '/dev/ttyUSB0' to your Arduino port

        # Send the base64 data to the Arduino
        ser.write((img_str + '\n').encode('utf-8'))
        print(len(img_str))
        ser.flush()  # Ensure all data is sent
        print("Data sent")
        time.sleep(10)  # 1 second delay
        # Close the serial connection

        # ... (rest of the code)
    except Exception as e:
        rospy.logerr("Error processing image: %s", str(e))

if __name__ == '__main__':
    rospy.init_node('image_to_serial_publisher')

    # Set the image topic you want to subscribe to
    image_topic = '/your/image/topic'
    rospy.Subscriber(image_topic, Image, image_callback)

    rospy.spin()
    