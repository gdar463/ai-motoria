import os
import platform

import PIL.Image as Image


def show_image( output ):
    # Check if running in WSL
    if platform.uname().release.endswith("microsoft-standard-WSL2"):
        # If in WSL, open with wslview
        os.system("wslview output.png")
    else:
        # Leaving OpenCV implementation if ever needed
        # # If not, let OpenCV handle it
        # cv2.imshow("Pose Detection", output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        Image.fromarray(output).show()
