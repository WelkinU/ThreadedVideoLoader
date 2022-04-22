# ThreadedVideoLoader
Basic multi-threaded wrapper of OpenCV's VideoCapture that behaves like a list and/or generator object.

## Functionality
* Easily grab video frames via iterator or list-like slicing
* Handles Video Files, Webcams, RTSP Stream, HTTP Stream
* More intuitive access to the internal video variables (height, width, fps, etc.)
* Multi-threaded execution and optional frame caching for speed
* Apply image transforms to your output, optionally save new video with transforms applied
* Extract frames from video / webcam and save to image files
* No compatibility issues with different OpenCV versions (handles OpenCV API changes for versions before and after 3.0.0)

## Usage

#### Example Initialization of VideoLoader() Objects
    vid = VideoLoader('myvideo.mp4')                               #Load from video file
    webcam = VideoLoader(0)                                        #Load from webcam
    largerWebcam = VideoLoader(0, height = 1080, width = 1920)     #Force OpenCV to use larger dimensions

#### Iterate Over a VideoLoader() Object
    for frame in vid:                   #iterate over each frame in the video / stream
        #do some processing
    
#### Indexing and List Slicing
    frame100 = vid[100]                 #get the 100th frame of the video - first frame of a video is 0
    lastFrame = vid[-1]                 #negative indexes work too
    slicedList = vid[50:100:-2]         #list-like slicing. Use precache_frames for fast repeated slicing on large slices

#### Easy Access to Video Parameters
    numFrames = len(vid)                #Get the frame length of the video
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
    vid_flipped = VideoLoader('myvideo.mp4', image_transform = np.flipud)

#### Applying image transforms to videos / webcam output
    #This VideoLoader loads cropped images - the first 100 pixels in each row and column are cropped!
    vid_cropped = VideoLoader('myvideo.mp4', image_transform = lambda x: x[100:, 100:])

    #This VideoLoader loads images upside-down!
    vid_flipped = VideoLoader('myvideo.mp4', image_transform = np.flipud)
    
    #save the flipped video as 'myvideo_flipped.mp4'
    vid_flipped.save_video_to_file(output_video_path = 'myvideo_flipped.mp4')

#### Crop video length / downsample frame rate
    vid = VideoLoader('myvideo.mp4')
    
    #output a video starting on frame 100, ending on frame 400 with a step size of 10 
    vid.save_video_to_file(output_video_path = 'my_new_video.mp4', start = 100, end = 400, step = 10)

#### Recording webcam output as video
    webcam = VideoLoader(0)
    
    #record to video "test.mp4". 
    #Use enable_start_stop_with_keypress = True to start/stop recording by pressing any key.
    webcam.save_video_to_file(output_video_path = 'test.mp4', enable_start_stop_with_keypress = True)
    
    #record every 10th frame
    webcam.save_video_to_file(output_video_path = 'test.mp4', step = 10)
    
#### Extract frames from Video / Webcam
Extract frames from a video file or webcam video stream and save them to a folder:

    file_format = 'frame{:05d}.jpg' #frame{:05d}.jpg extracts frames as frame00000.jpg, frame00001.jpg, etc.

    vid = VideoLoader('myvideo.mp4')
    vid.export_frames_from_video('my/output/folder', file_format = file_format)
    
    #output only a portion of frames - every 10th frame from frame 0 to 100
    vid.export_frames_from_video('my/output/folder', start = 0, end = 100, step = 10)
    
    webcam = VideoLoader(0)
    webcam.export_frames_from_video('my/output/folder', file_format = file_format,enable_start_stop_with_keypress = True)
    
    
## Software Requirements
Python 3.6+ with OpenCV installed. (Python 3.6 only required for format strings.) 
Compatibile with multiple versions of OpenCV (>= 3.0.0 and 2.X.Y)

## Troubleshooting
#### VideoLoader(0) doesn't find my webcam!
Try other integers: 1, 2, etc. Use VideoLoader(-1) to see available devices.

#### Slicing VideoLoader() objects is slow for large slices.
Options:
1. Return an iterator from the slice operator with VideoLoader('myvideo.mp4',return_slices_as_iterator = True). Note this only is a speedup for positive values of step. Negative step values still require the loader to read the whole batch of frames.
2. If you can frontload the load time, try VideoLoader('myvideo.mp4', precache_frames = True).

#### When trying to load from certain 1920x1080 webcams on Windows 10, the stream can be very slow!
I think this is a system issue. A workaround I have found is to set VideoLoader(0, height = **1081**, width = 1920) - it loads frames at 30 FPS and returns videos at the correct size 1920x1080 (not 1081)

## TODO
- [ ] For applying image transforms, investigate usage of ThreadPool class (likely faster than single thread)

