# ThreadedVideoLoader
Basic Multi-threaded Wrapper of OpenCV's VideoCapture That Behaves Like Other Python Objects

## Functionality
* Loading from anything supported by OpenCV: Videos (mp4, avi, mov, etc.), Webcams, etc. Untested: RTSP stream and HTTP stream.
* Loading in background thread by default.
* Easy iteration over video frames, particularly if iterating multiple times.
* Easy indexing into local videos with [ ] operator (not currently supported for video streams)
* More intuitive access to the internal video variables

## Usage
    #create a threaded VideoLoader() object, can also do a "with" statement.
    vid = VideoLoader('myvideo.mp4', use_threading = True, max_queue_size = 50)     #Load from video file
    webcam = VideoLoader(0, use_threading = True)                                   #Load from webcam
    
    for frame in vid:                   #iterate over each frame in the video / stream
        #do some processing
    
    frame100 = vid[100]                 #get the 100th frame of the video, [] not supported for video streams
    lastFrame = vid[-1]                 #negative indexes work too

    numFrames = len(vid)                #Get the frame length of the video. Can also do vid.frame_count
    fps = vid.fps                       #Get the video fps
    height = vid.height                 #Get the height in pixels
    width = vid.width                   #Get the width in pixels

    print(vid)                          #Print the main properties of the VideoLoader object
      
    #Release resources. Can skip this if the object was initialized using a "with" statement
    vid.release()

## Software Requirements
Python 3 with OpenCV installed.
