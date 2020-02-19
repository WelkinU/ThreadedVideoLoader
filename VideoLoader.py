''' Implements a wrapper to OpenCV's VideoCapture, that behaves like a Python Object.
Should be compatible with all applicable OpenCV versions. Support for threading to speed up
video read operations.
'''

import cv2
import threading
import queue
import inspect

class VideoLoader():
    ''' Implements a wrapper to OpenCV's VideoCapture, that behaves like a Python Object.
    Should be compatible with all applicable OpenCV versions. Support for threading to speed up
    video read operations.
    '''

    def __init__(self, video_path, use_threading = True, max_queue_size = 20, image_transform = None, width = None, height = None):
        ''' Initialize Video Loader
        video_path {str} -- Filepath to the video (path/to/video.mp4). Alternatively, use 0 for webcam (or 1 for your second webcam).
        use_threading {bool} -- If True, uses background thread to pre-caches frames in memory for speed.
                                If False, uses standard VideoCapture to grab frames on the fly. (default {True})
        max_queue_size {int} -- Maximum number of frames to cache in memory. Used only when use_threading = True. (Default {20})
        image_transform {function} -- A convenience feature for applying an image->image transform function to all image output.
                                        Must be a function that accepts an only image for input.
                                        Leaving this as None means no transform is applied to output. (Default {None})
        width {int} -- Override the defualt OpenCV capture dimensions. Useful when OpenCV incorrectly detects webcam dimensions.
        height {int} -- Override the defualt OpenCV capture dimensions. Useful when OpenCV incorrectly detects webcam dimensions.
        '''

        self.cap = cv2.VideoCapture(video_path)
        self.video_path = video_path
        self.image_transform = image_transform

        '''video properties - for more see: https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
            Note the constants names changed between OpenCV versions. Versions >= 3 don't have the "CV_" at the beginning.
        '''
        if cv2.__version__[0] >= '3':
            #for OpenCV versions >= 3, they have the constant names without the "CV_" at the beginning
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_codec = self.cap.get(cv2.CAP_PROP_FOURCC)
            #self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if height is None:
                self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                self.height = height
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

            if width is None:
                self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            else:
                self.width = width
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

            self.pos_frames_number = cv2.CAP_PROP_POS_FRAMES
        else:
            #for OpenCV versions < 2, they have the constant names with an the "CV_" at the beginning
            self.fps = self.cap.get(cv2.CV_CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CV_CAP_PROP_FRAME_COUNT))
            self.video_codec = self.cap.get(cv2.CV_CAP_PROP_FOURCC)

            if height is None:
                self.height = int(self.cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT))
            else:
                self.height = height
                self.cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, height)

            if width is None:
                self.width = int(self.cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH))
            else:
                self.width = width
                self.cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH, width)

            self.pos_frames_number = cv2.CV_CAP_PROP_POS_FRAMES

        #handle threading
        self.use_threading = use_threading
        if self.use_threading:
            self.thread_started = False
            self.frame_queue = queue.Queue(maxsize = max_queue_size)
            self.start_thread()
            self.first_queue_full_warning_displayed = False

    def __getitem__(self,idx):
        ''' Magic Function so you can use the [] operator to index into this object
        Used only when the frames are stored ie. webcam not supported for this function.
        Assumes index is within +/- video frame count. If outside of that range, it raises an error. 
        '''
        if self.frame_count > idx >= -self.frame_count and isinstance(idx,int):
            cur_frame_pos = self.get_frame_position() #save current frame position so this method doesn't interfere with __iter__() or __next__()

            self.cap.set(self.pos_frames_number, idx%self.frame_count)
            ret,frame=self.cap.read()

            self.cap.set(self.pos_frames_number, cur_frame_pos) #reset current frame position so this method doesn't interfere with __iter__() or __next__()

            return self.apply_transform(frame)
        else:
            raise IndexError(
                f'''Frame Index is {idx}. Frame Index needs to be a int that is less than the number of frames in the video. 
                If Frame Index is negative, it must have an absolute value less than or equal to the frame count''')

    def __iter__(self):
        '''Magic Function so you can call this as an iterator. Ex: for frame in VideoLoader('myvideo.mp4')'''

        if self.use_threading:
            if not self.thread_started:
                self.start_thread()
            while self.thread_started:
                #print('position {}'.format(self.get_frame_position()))
                frame = self.frame_queue.get(block = True, timeout = 30) #timeout is in seconds
                if frame is None:
                    break
                else:
                    yield self.apply_transform(frame)
            self.stop_thread()
        else:
            ret = True
            while ret:
                ret,frame=self.cap.read()
                yield self.apply_transform(frame)
        self.cap.set(self.pos_frames_number, 0) #reset frame position to 0, in case __iter__() is called multiple times sequentially

    def __next__(self):
        '''Magic Function so you use the next() function on this object.'''
        if self.use_threading:
            frame = self.frame_queue.get(block = True, timeout = 30) #timeout is in seconds
            if frame is None:
                raise StopIteration
            else:
                yield self.apply_transform(frame)
        else:
            ret,frame=self.cap.read()        
            if ret >= self.frame_count:
                self.cap.set(self.pos_frames_number, 0)
                raise StopIteration
            else:
                return self.apply_transform(frame)

    def __repr__(self):
        '''Magic Function so you can use the print() function on this object.
        Using inspect to fix the triple commented string issue per this. Textwrap module didn't work due to leading line issue.
        https://stackoverflow.com/questions/1412374/how-to-remove-extra-indentation-of-python-triple-quoted-multi-line-strings/47417848#47417848
        '''
        ret = f'''-------------VideoLoader Object-------------
                    Video Source: {self.video_path}
                    Video Codec: {self.video_codec}
                    Threaded: {self.use_threading}
                    Image Transform: {"Yes" if self.image_transform else "No"}
                    Height: {self.height}
                    Width: {self.width}
                    Length: {self.frame_count}
                    FPS: {self.fps}
                    --------------------------------------------
                    '''
        return inspect.cleandoc(ret)

    def __len__(self):
        '''Magic Function so you can use the len() function on this object.'''
        return self.frame_count

    def __enter__(self):
        return self

    def __exit__(self):
        print('Releasing resources.')
        if self.use_threading:
            self.stop_thread()
        self.cap.release()

    def release(self):
        self.__exit__()

    def set(self, var1, var2):
        self.cap.set(var1, var2)           

    def get_frame_position(self):
        return self.cap.get(self.pos_frames_number)

    def apply_transform(self,frame):
        return frame if self.image_transform is None else self.image_transform(frame)

    #----------------------------------THREADING SPECIFIC FUNCTIONS----------------------------------
    def start_thread(self):
        if self.thread_started:
            print('Thread already started!')
            return

        self.thread_started = True
        self.thread = threading.Thread(target = self.update_thread, daemon = True, args =())
        self.thread.start()

    def update_thread(self):
        ret = True

        while ret and self.thread_started:
            ret, frame = self.cap.read()

            try:
                self.frame_queue.put(frame,block=True, timeout = 1) #timeout is in seconds, on last read, None is put into the Queue conveniently 
            except queue.Full:
                #Current behavior is that if the queue is full and the main process has not exited, then we start dropping frames
                if not self.thread_started:
                    break
                else:
                    if not self.first_queue_full_warning_displayed:
                        self.first_queue_full_warning_displayed=True
                        print('Warning background thread has filled up frame queue storage. Future frames may be dropped if input is a video stream.')

                        #continue attmpting the next frame into the queue until it's read by the main thread or the main thread has stopped
                        while self.thread_started:
                            try:
                                self.frame_queue.put(frame,block=True, timeout = 1)
                                break
                            except:
                                pass

        self.thread_started = False

    def stop_thread(self):
        self.thread_started = False
        self.thread.join()

if __name__ == '__main__':
    #webcam test - press q or esc to exit
    vid = VideoLoader(0)
    for frame in vid:
        cv2.imshow('Image',frame)
        if cv2.waitKey(1) in [27,ord('q')]:
            vid.release()
            break
