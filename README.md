# ThreadedVideoLoader
Basic multi-threaded wrapper of OpenCV's VideoCapture that behaves like a list and/or generator object.

## Functionality
* Loading from anything supported by OpenCV: Videos (mp4, avi, mov, etc.), Webcams, etc. Untested: RTSP stream and HTTP stream.
* Loading in background thread by default. Alternatively you can pre-cache frames.
* Easy iteration over video frames, particularly if iterating multiple times.
* Easy indexing/slicing of videos with [ ] operator (not currently supported for video streams)
* More intuitive access to the internal video variables (fps, height, width, etc.)
* Compatibility with multiple versions of OpenCV (>= 3.0.0 and 2.X.Y)

## Usage
    #create a threaded VideoLoader() object, can also do a "with" statement.
    vid = VideoLoader('myvideo.mp4', use_threading = True, max_queue_size = 50)     #Load from video file
    webcam = VideoLoader(0, use_threading = True)                                   #Load from webcam
    largerWebcam = VideoLoader(0, height = 1080, width = 1920)                      #Force OpenCV to use larger dimensions
    
    for frame in vid:                   #iterate over each frame in the video / stream
        #do some processing
    
    frame100 = vid[100]                 #get the 100th frame of the video, [] not supported for video streams
    lastFrame = vid[-1]                 #negative indexes work too
    reversedVideo = vid[::-1]           #List-like slicing. Use precache_frames for fast slicing on large slices

    numFrames = len(vid)                #Get the frame length of the video. Can also do vid.frame_count
    fps = vid.fps                       #Get the video fps
    height = vid.height                 #Get the height in pixels
    width = vid.width                   #Get the width in pixels

    print(vid)                          #Print the main properties of the VideoLoader object
      
    #Release resources. Can skip this if the object was initialized using a "with" statement
    vid.release()

## Software Requirements
Python 3 with OpenCV installed.

## Issues
#### VideoLoader(0) doesn't find my webcam!
Try other integers - 1, 2, etc. Use VideoLoader(-1) to see available devices.

#### Slicing VideoLoader() objects is slow for large slices.
Try using VideoLoader(precache_frames = True). For now, this is the best you can do on this.

#### When trying to load from certain 1920x1080 webcams on Windows 10, the stream can be very slow!
I think this is a system issue. A workaround I have found is to set VideoLoader(0, height = **1081**, width = 1920) - it is fast, and returns videos at 1920x1080 (not 1081)

## TODO
[ ] Have VideoLoader slicing return iterator instead of list?
[ ] Smarter frame caching algorithm. Need to test tradeoffs between different frame caching methods for different use cases.
