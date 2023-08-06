import torch
import numpy as np
import cv2
from time import time

import pandas as pd
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2

class PigDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using Opencv2.
    """

    def __init__(self, capture_index, model_name, ratio=0.2, distance_between_pixel=5):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.capture_index = capture_index
        self.model = self.load_model(model_name)
        self.ratio = ratio
        self.n = 0
        self.round = 1
        self.data = [0, 0]
        self.data_interest = [0, 0] 
        self.pre_frame = 0
        self.post_frame = 0
        self.distance_between_pixel = distance_between_pixel
        self.classes = ["Other", "Sleep", "Stand"]
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def get_video_capture(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
      
        return cv2.VideoCapture(self.capture_index)

    def load_model(self, model_name):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame) 
        #n_pig = results.xyxyn[0].shape[0]
        #info = results.xyxy[0].pandas()
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= self.ratio:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                if self.class_to_label(labels[i]) == "Other":
                    bgr = (0, 0, 0)
                elif self.class_to_label(labels[i]) == "Stand":
                    bgr = (0, 255, 0)
                else:
                    bgr = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame
    
    def create_data(self, frame):
        result = self.model(frame).pandas().xyxy[0]
        result['n'] = np.arange(0, result.shape[0])
        if self.round < 3:
            self.pre_frame = result
            self.post_frame = result
            self.round += 1
        elif self.round > 2 & result.shape[0] > 1:
            self.pre_frame = self.post_frame
            self.post_frame = result
            self.round += 1
        self.data[0] = self.pre_frame
        self.data[1] = self.post_frame

        self.data_interest[0] = self.data[self.n]
        self.data_interest[1] = self.data[self.n+1]
        #print(self.data_interest[0].shape)
        #print(self.data_interest[0]['xmin'].iloc[0])
        for i in range(self.data_interest[0].shape[0]):
           for j in range(self.data_interest[1].shape[0]):
              if abs(self.data_interest[0]['xmin'].iloc[i] - self.data_interest[1]['xmin'].iloc[j]) < self.distance_between_pixel:
                  if self.data_interest[0]['n'].iloc[i] != self.data_interest[1]['n'].iloc[j]:
                      self.data_interest[1]['n'].iloc[j] = self.data_interest[0]['n'].iloc[i]
        #print(self.data)
        #print("data_interest[0]: ", data_interest[0])
        return self.data_interest[1]

    def detect(self):
        stream = self.get_video_capture()
        assert stream.isOpened()
        fps = FPS().start()
        n = False
        while True:
            (grabbed, frame) = stream.read()
            frame = imutils.resize(frame, width=450)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
            start_time = time()

            data = self.create_data(frame)
            #if len(data) > 1:
                #print(data)
            results = self.score_frame(frame)
            
            frame = self.plot_boxes(results, frame)
            
            end_time = time()
            for i in range(len(data)): #str(data['n'].iloc[i])
                cv2.putText(frame, str(data['n'].iloc[i]), (int(data['xmax'].iloc[i]), int(data['ymin'].iloc[i])), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                #print(data['xmin'].iloc[i])
            #cv2.putText(frame, f'FPS: {int(fps)}', (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            fps.update()
      
        stream.release()
