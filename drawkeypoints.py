import numpy as np
import cv2
import os
import pose_Projectfrom3D
baseDir = "./data/"
camDir = os.path.join(baseDir,"camera")
Pose3DPath = baseDir + "OP3DTXTRefined/"
renderPath = baseDir +"OP3DRendered/"
OP2DTXTPath = baseDir +"OP2DTXT/Lea/"


def createframefrom2Dfile(path):


    # 2D coordinates file into frames list
    x = []
    y = []
    frames = [] # frames with coord inside so frame_number is the index
    f = open(OP2DTXTPath+path, "r")
    lines = f.readlines()
        # adding frames and coord into frames
    for line in lines:
        content_list= line.split()
        x = list(map(float,content_list[::3]))
        y = list(map(float,content_list[1::3]))
        frames.append(list(zip(x,y)))
    print(frames[1])
    f.close()
    return frames


#drawing on the frames
def drawing(frames,videopath):
    cap= cv2.VideoCapture(videopath)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter(baseDir + 'extractedframes/output.avi',cv2.VideoWriter_fourcc(*'MJPG'),60,size)
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        #frame treatment
        for point in frames[i]:
            #draw function
            cv2.circle(frame, (int(point[0]),int(point[1])), radius = 3,color=(0, 0, 255), thickness=-1)
        result.write(frame)
        i += 1

    cap.release()
    result.release()
    cv2.destroyAllWindows()
    return

def main():
    videoPath = baseDir + "Videos/Lea/squat_1_0.1.avi"
    frames2 = createframefrom2Dfile("squat_1_0.1.txt")
    #frames2 = pose_Projectfrom3D.main(1,"squat_1_0.txt")
    drawing(frames2,videoPath)
    return


if __name__ == "__main__":
    # execute only if run as a script
    main()



