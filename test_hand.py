# test_hand.py
import cv2
from hand import HandController

controller = HandController()

print("🖐️ Gesture Control Active — ESC to exit")

while True:
    frame = controller.process_frame()
    if frame is not None:
        cv2.imshow("Hand Gesture Mouse Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

controller.release()
cv2.destroyAllWindows()
