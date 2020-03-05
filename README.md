# ThreadedVideoLoader
Basic multi-threaded wrapper of OpenCV's VideoCapture that behaves like a list and/or generator object.

## Functionality
* Handles Video Files, Webcams, RTSP Stream, HTTP Stream
* Easy iteration and list-like slicing of video frames
* More intuitive access to the internal video variables (fps, height, width, etc.)
* Multi-threaded execution and optional frame caching for speed
* Apply image transforms to your output, optionally save new video with transforms applied
* Extract frames from video / webcam and save to image files

## Usage

#### Example Initialization of VideoLoader() Objects
    vid = VideoLoader('myvideo.mp4')                                                #Load from video file
    webcam = VideoLoader(0)                                                         #Load from webcam
    largerWebcam = VideoLoader(0, height = 1080, width = 1920)                      #Force OpenCV to use larger dimensions

#### Iterate Over a VideoLoader() Object
    for frame in vid:                   #iterate over each frame in the video / stream
        #do some processing
    
#### Indexing and List Slicing
    frame100 = vid[100]                 #get the 100th frame of the video - first frame of a video is 0
    lastFrame = vid[-1]                 #negative indexes work too
    slicedList = vid[50:100:-2]         #list-like slicing. Use precache_frames for fast repeated slicing on large slices

#### Easy Access to Video Parameters
    numFrames = len(vid)                #Get the frame length of the video. Can also do vid.frame_count
    fps = vid.fps                       #Get the video fps
    height = vid.height                 #Get the height in pixels
    width = vid.width                   #Get the width in pixels

    print(vid)                          #Print the main properties of the VideoLoader object

#### Object Cleanup (Release Resources)
    #Release resources. Can skip this if the object was initialized using a "with" statement
    vid.release()

## Advanced Usage
#### Automatic image transforms
    import numpy as np
    #This VideoLoader loads images upside-down!
    vid_flipped = VideoLoader('myvideo.mp4', transform = np.flipud())

#### Applying image transforms to videos / webcam output
    #This VideoLoader loads images upside-down!
    vid_flipped = VideoLoader('myvideo.mp4', image_transform = np.flipud)
    
    #save the flipped video as 'myvideo_flipped.mp4'
    vid_flipped.apply_transform_to_video(output_video_path = 'myvideo_flipped.mp4')

#### Recording webcam output as video
    webcam = VideoLoader(0)
    
    #record to video "test.mp4". 
    #Use enable_start_stop_with_keypress = True to start/stop recording by pressing any key.
    webcam.apply_transform_to_video(output_video_path = 'test.mp4', enable_start_stop_with_keypress = True)
    
#### Extract frames from Video / Webcam
Extract frames from a video file or webcam video stream and save them to a folder:

    file_format = 'frame{:05d}.jpg' #frame{:05d}.jpg extracts frames as frame00000.jpg, frame00001.jpg, etc.

    vid = VideoLoader('myvideo.mp4')
    vid.dump_frames_from_video('my/output/folder', file_format = file_format)
    
    webcam = VideoLoader(0)
    webcam.dump_frames_from_video('my/output/folder', file_format = file_format,enable_start_stop_with_keypress = True)
    
    
## Software Requirements
Python 3.6+ with OpenCV installed. (Python 3.6 only required for format strings.) 
Compatibile with multiple versions of OpenCV (>= 3.0.0 and 2.X.Y)

## Issues
#### VideoLoader(0) doesn't find my webcam!
Try other integers: 1, 2, etc. Use VideoLoader(-1) to see available devices.

#### Slicing VideoLoader() objects is slow for large slices.
Options:
1. Return an iterator from the slice operator with VideoLoader('myvideo.mp4',return_slices_as_iterator = True). Note this only is a speedup for positive values of step. Negative step values still require the loader to read the whole batch of frames.
2. If you can frontload the load time, try VideoLoader('myvideo.mp4', precache_frames = True).

#### When trying to load from certain 1920x1080 webcams on Windows 10, the stream can be very slow!
I think this is a system issue. A workaround I have found is to set VideoLoader(0, height = **1081**, width = 1920) - it loads frames at 30 FPS and returns videos at the correct size 1920x1080 (not 1081)

## TODO
- [x] Have VideoLoader slicing return iterator instead of list - Use VideoLoader('myvideo.mp4',return_slices_as_iterator = True)
- [ ] Smarter frame caching algorithm. 
