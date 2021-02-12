import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import _pickle as cPickle

def transform(orig_image, skewed_image, y):
        
        orig_image = np.array(orig_image)
        skewed_image = np.array(skewed_image)
        h, w = orig_image.shape[:2]
        d = y

        orig_image   = cv2.UMat(orig_image)
        #skewed_image = cv2.UMat(skewed_image)
        
        sift = cv2.xfeatures2d.SIFT_create(2000)
        kp1, des1 = sift.detectAndCompute(orig_image, None)
        #kp2, des2 = sift.detectAndCompute(skewed_image, None)
        index = cPickle.loads(open(r'C:\Users\ubaid\AppData\Local\Programs\Python\Python37\CodesandImages\text_files\kp%d.txt'%d, 'rb').read())
        kp2 = []

        for point in index:
            temp = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
            kp2.append(temp)

        des2 = np.loadtxt(r'C:\Users\ubaid\AppData\Local\Programs\Python\Python37\CodesandImages\text_files\des%d.txt'%d, dtype=np.float32)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good.append(m)

        MIN_MATCH_COUNT = 10
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good
                                  ]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good
                                  ]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            ss = M[0, 1]
            sc = M[0, 0]
            scale = math.sqrt(ss * ss + sc * sc)
            theta = math.atan2(ss, sc) * 180 / math.pi
            im_out = cv2.warpPerspective(skewed_image, np.linalg.inv(M),
                (w, h))
            print(theta)
            #im_out = cv2.UMat.get(im_out)
            return (im_out, theta)


    
    
