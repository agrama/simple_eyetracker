#
#  ProsilicaCameraDevice.py
#  EyeTrackerStageDriver
#
#  Created by David Cox on 7/29/08.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#

#
#  SimulatedCameraDevice.py
#  EyeTrackerStageDriver
#
#  Created by David Cox on 5/26/08.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#

import pypylon as pylon
from numpy import *
#import matplotlib.pylab as pylab

import os
import time

import PIL.Image

import threading


class BaslerCamera:

    def __init__(self, **kwargs):

        self.frame_number = 0

        self.camera = None

        self.im_array = None
        self.image_center = array([0, 0])
        self.pupil_position = array([0., 0.])
        self.cr_position = array([0., 0.])

        self.nframes_done = 0

        self.acquire_continuously = 0
        self.acquisition_thread = None
        
        print("Finding valid Basler cameras...")
        time.sleep(1)
        camera_list = pylon.factory.find_devices()
        print camera_list

        if(len(camera_list) <= 0):
            raise Exception("Couldn't find a valid camera")

        try:
            self.camera = pylon.factory.create_device(camera_list[0])
            self.camera.open()
            
        except:
            raise Exception("Couldn't instantiate camera")


        self.camera.properties['Width'] = 160
        self.camera.properties['Height'] = 120
        self.camera.properties['CenterX'] = True
        self.camera.properties['CenterY'] = True
        self.camera.properties['PixelFormat'] = 'Mono8'
        self.camera.properties['AcquisitionFrameRate'] = 120.0
        self.camera.properties['AcquisitionFrameRateEnable'] = True


        self.generator = self.camera.grab_images(-1)


    def shutdown(self):
        print "Deleting camera (in python)"
        if(self.acquire_continuously):
            print "Terminating acquisition thread in BaslerCameraDevice"
            self.acquisition_thread.terminate()
        if(self.camera is not None):
            print "ending camera capture in BaslerCameraDevice"
            self.camera.close()

    def __del__(self):
        print "Deleting camera (in python)"
        if(self.acquire_continuously):
            self.acquisition_thread.terminate()
        if(self.camera is not None):
            self.camera.close()


    @property
    def roi_width(self):
        return self.camera.properties['Width']

    @roi_width.setter
    def roi_width(self, value):
        self.camera.properties['Width'] = int(value)

    @property
    def roi_height(self):
        return self.camera.properties['Height']

    @roi_height.setter
    def roi_height(self, value):
        print 'setting height'
        self.camera.properties['Height'] = int(value)



    def acquire_image(self):

        if(self.camera is None):
            raise Exception, "No valid camera is in place"

        # self.im_array = self.camera.grab_image()
        self.im_array = self.generator.next()

        timestamp = 0 # dummy for now

        #timestamp = frame.timestamp
        #print "Timestamp: ", timestamp
        # self.camera.releaseCurrentFrame()
        self.frame_number += 1

        return self.im_array, {'frame_number': self.frame_number, 'timestamp': timestamp}


