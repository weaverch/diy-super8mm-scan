###################################################################
# This file is a modification of the file "tc-common.py" from the #
#  RPi Telecine project.  I've included that project's header and #
#  copyright below.                                               #  
###################################################################
# RPi Telecine Common functions
#
# Common functions shared by the telecine scripts 
# Provides for reading and writing the job's ini file
# Moving the film frame-by-frame
# Displaying a preview window
# Stopwatch class for benchmarking
#
# Copyright (c) 2015, Jason Lane
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or 
# other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR 
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import time
import cv2
import super8scan

cam  = super8scan.s8sCamera()
cnf  = super8scan.s8sConfig()
pf   = super8scan.s8sPerforation()
        
# Some useful values returned by cv2.waitKey - 
# probably platform dependent
# These work on the Pi
#cv2_keys = {'RightArrow':65363, 'LeftArrow':65361, \
                        #'UpArrow':65362, 'DownArrow':65364, \
                        #'Escape':27, 'Enter':10, \
                        #'Home':65360, 'End':65367, \
                        #'PgUp':65365, 'PgDn':65366, 'Tab':9 } 

#def display_shadow_text(img,x,y,text):
    #"""
    #Displays with a grey shadow at point x,y
    #"""
    #text_color = (255,255,255) #color as (B,G,R)
    #text_shadow = (0,0,0)
    #text_pos = (x,y)
    #shadow_pos = (x+1,y+1)
    #cv2.putText(img, text, shadow_pos, cv2.FONT_HERSHEY_PLAIN, 1.25, text_shadow, thickness=1, lineType=cv2.LINE_4)
    #cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_PLAIN, 1.25, text_color, thickness=1, lineType=cv2.LINE_4)
    #return img

#def display_image(window_name,img,reduction=2, text=''):
    #""" 
    #Resize image and display using imshow. Mainly for debugging 
    #Resizing the image allows us to see the full frame on the monitor
    #as cv2.imshow only allows zooming in.
    #The reduction factor can be specified, but defaults to half size
    #Text can also be displayed - in white at top of frame
    #"""
    #reduction = constrain(reduction,1.2,6)
    #newx,newy = int(img.shape[1]/reduction),int(img.shape[0]/reduction)  #new size (w,h)
    #newimg = cv2.resize(img,(newx,newy))
    #if text != '':
        #display_shadow_text(newimg,20,25,text)
    #cv2.imshow(window_name,newimg)
    
#def display_thumb(window_name,img,reduction=2, text=''):
    #""" 
    #Displays a reduced sized image - but use Numpy strides to do the resize.
    #A lot faster than using cv2.resize, but is limited to integer reduction factors
    #no interpolation is done, so is subject to aliasing. If no text is needed, no
    #copy of the image data is done.
    #"""
    #reduction = int(constrain(reduction,2,6))
    #if text == '':
        ## Fast - doesn't copy the image data
        #newimg = img[::reduction,::reduction]
    #else:
        ## Putting text only works on a copy of the image
        #newimg = img[::reduction,::reduction].copy()
        #display_shadow_text(newimg,20,25,text)

    #cv2.imshow(window_name,newimg)
    
#def sanitise_job_name(job_name):
    ## Sanitise the jobname as we'll be creating a folder from it
    #delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    #job_name = job_name.translate(None, delchars)
    
    #if not job_name:
        #print('Job name needs to consist of characters "azAZ-_"')
        #quit()
        
    #return job_name
    
class Stopwatch():
    """
    Simple timing class used to record time of capturing frames
    """
    
    def __init__(self):
        self.start_time = None
        
    def start(self):
        if self.start_time is not None:
            # Already started 
            return
        self.running = True
        self.start_time = time.time()
        
    def stop(self):
        # Stop and return elapsed time
        t = time.time()-self.start_time
        self.start_time = None
        return t
