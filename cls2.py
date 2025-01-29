import cv2
import numpy as np
from tensorflow import keras
from tensorflow import math as ops
from landmarker import Landmarker

LETTERS = "ABCDEFGHIKLMNOPQRSTUVWXY"


class Classifier:
    def __init__(self):
        self.model = keras.models.load_model("models/model5.keras")

    def classify(self, points):
        predictions = self.model.predict(points[:, :, :2], verbose=0)
        prediction = ops.argmax(predictions, -1).numpy()
        probability = predictions[0][prediction[0]]
        letter = LETTERS[prediction[0]]

        return letter, probability


def main():
    landmarker = Landmarker()
    classifier = Classifier()

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Process the frame with Landmarker
        success, processed_image, points, wrist_position, handedness = landmarker.draw_landmarks(
            frame)

        if success and points is not None:
            # Classify the hand gesture
            letter, probability = classifier.classify(points)

            # Display the result on the frame
            cv2.putText(processed_image, f"Letter: {letter}", (
                10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(processed_image, f"Probability: {probability:.2f}", (
                10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Sign Language Detection', processed_image)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
