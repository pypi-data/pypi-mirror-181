# Model Assisted Labeling Toolkit

Malt allows users to quickly create labeled images from a video with the help of a predefined model. Creating good training data for object recognition is an iterative process, and malt is designed to speed up each iteration. The typical malt workflow will go as follows:

- Create a sparsely trained Tensorflow Lite Model
- Load and scan through a video to find object positions that are unfamiliar to the model and label those frames
- Adjust the auto-generated bounding boxes to perfectly fit the target object
- Save the labeled frames as images
- Train a new model
- Load the new model and a new video
- Repeat the process

## Install & Launch Malt
> pip3 install maltk
> malt or python3 -m malt

