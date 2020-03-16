import cv2
import numpy as np
from  random import *


class blob:
    def __init__(self,r,thickness,spawn,speed,limit):
        self.x = spawn[0]
        self.y = spawn[1]
        self.xlimit = (r+thickness,limit[0]-(r+thickness))
        self.ylimit = (r+thickness,limit[1]-(r+thickness))
        self.position = (self.x, self.y)
        self.radius = r
        self.thickness = thickness
        self.speed_x =speed[0]*choice([-1,1])
        self.speed_y =speed[1]*choice([-1,1])



    def update(self):

        # Bounce back from the edges by reversing the spped of x and y
        if self.x <= self.xlimit[0] or self.x >=self.xlimit[1]:
            self.speed_x  = self.speed_x*-1
        if self.y <= self.ylimit[0] or self.y >= self.ylimit[1]:
            self.speed_y  = self.speed_y*-1

        # update the co-ordinates
        self.x += self.speed_x
        self.y += self.speed_y
        self.position  = (self.x,self.y)

    def __sub__(self, other):
        # returns the distance from other blob

        return int( ((self.x-other.x)**2 + (self.y-other.y)**2 )**(1/2))



if "__main__" == __name__:

    #-- Setting of window size and blob features-----

    window = (700,700)
    blob_color = [255, 255, 255]
    # bg_color = [213, 193,62 ]
    bg_color = [0, 0,0 ]
    bob_sensitive_dist = 300
    speed = 20
    no_blob = 30

    #-------------------------------------------------


    blobs=  []
    for x in range(no_blob):
        blobs.append(blob(5,1, (randint(0,window[0]),randint(0,window[1])),(randint(1,speed),randint(1,speed)),window))


    while True:

        # color = [213, 193,62 ]
        main_matrix = np.array( [[bg_color]*window[0]]*window[1], np.uint8)
        # main_matrix = np.zeros((window[0],window[1]),np.uint8)

        for Blob in blobs:
            for other in blobs:

                if Blob !=other:
                    if 0 < Blob-other  < bob_sensitive_dist:
                        ratio = (Blob - other) / bob_sensitive_dist
                        brightB =  bg_color[0]*(ratio) + blob_color[0]*(1-ratio)
                        brightG =  bg_color[1]*(ratio) + blob_color[1]*(1-ratio)
                        brightR =  bg_color[2]*(ratio) + blob_color[2]*(1-ratio)
                        cv2.line(main_matrix, (Blob.x,Blob.y), (other.x,other.y), (brightB,brightG ,brightR), 1)

        for Blob in blobs:
            cv2.circle(main_matrix, Blob.position, Blob.radius, (blob_color[0], blob_color[1], blob_color[2]), -1)
            Blob.update()
        cv2.imshow("image", main_matrix)

        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
