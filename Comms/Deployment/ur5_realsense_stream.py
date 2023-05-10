import os
import cv2
import pyrealsense2 as rs
import numpy as np

# def save_image_data(image_folder):
#     """
#     This function captures frames from a RealSense camera and saves the RGB data as a PNG file.
#     """
#     # Create a context object. This object owns the handles to all connected realsense devices
#     pipeline = rs.pipeline()

#     # Configure streams
#     config = rs.config()
#     config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 12)

#     # Start streaming
#     profile = pipeline.start(config)

#     # Alignment object
#     align_to = rs.stream.color
#     align = rs.align(align_to)

#     frames = pipeline.wait_for_frames()
#     aligned_frames = align.process(frames)
#     color_frame = aligned_frames.get_color_frame()

#     color_image = np.array(color_frame.get_data())

#     # Save image data to a PNG file
#     image_path = os.path.join(image_folder, "realsense_img.png")
#     cv2.imwrite(image_path, color_image)

#     print(f"Image data saved at: {image_path}")

#     pipeline.stop()

from flask import Flask, render_template, Response

app = Flask(__name__)

def get_realsense_feed():
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    print(config)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 10)

    # Start streaming
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            ret, jpeg = cv2.imencode('.jpg', color_image)
            
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    finally:
        pipeline.stop()
        print('The RealSense pipeline could not be accessed!')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(get_realsense_feed(),
                    content_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)