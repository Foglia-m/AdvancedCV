
import numpy as np
import cv2
import os

baseDir = "./data/"
camDir = os.path.join(baseDir,"camera/")
Pose3DPath = baseDir + "OP3DTXT/Lea/"
renderPath = baseDir +"OP3DRendered/"

#There are 4 cameras: each configured by data_i.xml
#disstortion coefficients change
#Pose.xml gives relative positions, ex pose_0_1.xml: the relative pose between camera 0 and 1

# Projection using pose_0_i.xml (relative positions)
#  .xml(rotation)  .xml(

#create camera 0 list of coordinates:

# file outline : r,x,i,j, score
def create_frames_list(path):
    x = []
    y = []
    z = []
    frames = [] # frames with coord inside so frame_number is the index
    f = open(Pose3DPath+path, "r")
    lines = f.readlines()
        # adding frames and coord into frames
    c=0
    for line in lines:
        if c<5:
            c+=1
        else:

            content_list= line.split()
            x = list(map(float,content_list[1::4]))
            y = list(map(float,content_list[2::4]))
            z = list(map(float, content_list[3::4]))
            frames.append(list(zip(x,y,z)))
    f.close()
    return frames



#define a function projection that project the cam_0 coordinates according to the xml file: pose_0_i.xml
def projection_to_cam(i,frames):
    #get the camera matrix K
    cam_xml = cv2.FileStorage(camDir + "out_camera_data_" + str(i) + ".xml", cv2.FILE_STORAGE_READ)
    K = cam_xml.getNode("camera_matrix").mat()
    alpha = [K[0,0],K[1,1]]
    xoyo = np.array([K[0,2],K[1,2]]) #according to the intrinsic parameters definiton in the course
    # get the pose_0_i
    fs = cv2.FileStorage(camDir+"pose_0_"+str(i)+".xml", cv2.FILE_STORAGE_READ)
    transform = fs.getNode("transform").mat()


    rot_frames = []

    for frame in frames:
        #compute matrix for every coordinates
        # #why is P dim 3x4?
        # P = R*WP + t
        rot_frame = []
        for coord in frame:
            rot_coord =[]
            coord_reshaped = np.append(coord,[1]) #reshaping (X,Y,Z) to (X,Y,Z,1) in order to apply the transformation matrix
            # transform accordingly using the parameters
            new_coord = np.dot(transform, np.transpose(coord_reshaped)) #we get the unhomogenous coordinates
            new_coord_2D = new_coord[:2]/new_coord[2] #this lets us use the form of the central projection


            #here I use the intrinsic matrix coordinates:
            final_2d_coord = new_coord_2D*alpha + xoyo
            #print(final_2d_coord)
            rot_coord= (tuple(final_2d_coord))
            rot_frame.append(rot_coord)
        rot_frames.append(rot_frame)
        #if k ==10:
        #    break
    #append to the frames scope
    #write file??
    return rot_frames





def main(i,path):
    #create frame list (with cam 0 coordinates) from the txt file
    frames = create_frames_list(path)
    #projection for each camera
    #npframes = np.array(frames)
    rotated_frames = projection_to_cam(i, frames)
    print(rotated_frames[0][0]) # test first frame

    return rotated_frames

if __name__ == "__main__":
    # execute only if run as a script
    main(1)