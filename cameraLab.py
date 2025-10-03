# [180DA, Lab 1] 
#Reference
#Github User: aysebilgegunduz
#Uses: "find_histogram" from kmeans.py given in the lab manual
#url: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097

#Improvements:
# -live camera tracking 
# - desginated central rectangle (instead of whole frame)
# - check if camera available


import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pdb 

#-----From Given Example Code (kmeans.py)---------------------------------
def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
#---------------------------------------------------------


def main():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("could not find webcam")
        return
    
    roi_rel_w, roi_rel_h = 0.35,0.35

    print("Press q to quit")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        H, W = frame.shape[:2]
        rw, rh = int(W * roi_rel_w), int(H * roi_rel_h)
        x1 = (W - rw) // 2
        y1 = (H-rh) // 2
        x2 = x1 + rw
        y2 = y1 + rh

        roi = frame[y1:y2, x1:x2]

        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        pixels = roi_rgb.reshape((-1,3))

        clt = KMeans(n_clusters=3, n_init = "auto", random_state=42)
        clt.fit(pixels)


        hist = find_histogram(clt)
        centers = clt.cluster_centers_
        dom_index = int(np.argmax(hist))
        dominant_rgb = centers[dom_index]

        dr, dg, db = map(int, dominant_rgb)
        print(f"Dominant RGB in ROI: ({dr}, {dg}, {db})")

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255),2)
        cv2.imshow("Video Feed (Central ROI shown)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

