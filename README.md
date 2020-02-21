# ThreadedVideoLoader
Basic multi-threaded wrapper of OpenCV's VideoCapture that behaves like a list.

## Functionality
* Loading from (almost) anything: Videos, Webcams, RTSP stream, HTTP stream
* Easy iteration over video frames, particularly if iterating multiple times.
* Easy indexing/slicing of videos with [ ] operator (not currently supported for video streams)
* Loading in background thread by default. Alternatively you can pre-cache frames for faster repeated execution.
* More intuitive access to the internal video variables (fps, height, width, etc.)
* Apply image transforms to your output, or apply the transform to the whole video and save it to a file
* Compatibility with multiple versions of OpenCV (>= 3.0.0 and 2.X.Y)

## Usage

#### Example Initialization of VideoLoader() Objects
    vid = VideoLoader('myvideo.mp4')                                                #Load from video file
    webcam = VideoLoader(0)                                                         #Load from webcam
    largerWebcam = VideoLoader(0, height = 1080, width = 1920)                      #Force OpenCV to use larger dimensions

#### Iterate Over a VideoLoader() Object
    for frame in vid:                   #iterate over each frame in the video / stream
        #do some processing
    
#### Indexing and List Slicing
    frame100 = vid[100]                 #get the 100th frame of the video, [] not supported for video streams
    lastFrame = vid[-1]                 #negative indexes work too
    reversedVideoSpedUp = vid[::-2]     #List-like slicing. Use precache_frames for fast slicing on large slices

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
    #This VideoLoader loads images upside-down!
    vid_flipped = VideoLoader('myvideo.mp4', transform = np.flipud())

#### Applying image transforms to videos
    #This VideoLoader loads images upside-down!
    vid_flipped = VideoLoader('myvideo.mp4', transform = np.flipud())
    
    #save the flipped video as 'myvideo_flipped.mp4'
    vid_flipped.apply_transform_to_video(output_video_path = 'myvideo_flipped.mp4')
    
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
- [ ] Have VideoLoader slicing return iterator instead of list
- [ ] Smarter frame caching algorithm. Test tradeoffs between different frame caching methods for different use cases.
