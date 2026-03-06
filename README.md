<!DOCTYPE html>
<html>
<head>

</head>


<body>


<h1>Pose Estimation and Correction Engine</h1>

<p>
This project was developed as part of the internship technical assignment.
The objective of the assignment was to understand how human pose estimation works
and then build a simple posture correction system using rule-based logic.
</p>

<p>
The system detects the human body pose through the webcam, extracts body landmarks,
analyzes the posture, and provides feedback when the posture is incorrect.
</p>

<p>
Instead of training a machine learning model, the project focuses on understanding
pose detection and applying logical rules to guide the user through a stretching exercise.
</p>



<div class="section">

<h2>Exercise Implemented</h2>

<p>
The exercise implemented in this project is a simple overhead stretch.
</p>

<p>
The instructions for the exercise are:
</p>

<ul>

<li>Stand straight.</li>
<li>Keep the feet approximately 15 cm apart.</li>
<li>Raise both arms above the head.</li>
<li>Join the palms and fingers together.</li>
<li>Keep the arms close to the ears.</li>
<li>Hold the posture for a few seconds.</li>
<li>Bring the arms down to the thighs and rest.</li>

</ul>

<p>
This movement repeats multiple times and the system observes whether the user performs
each step correctly.
</p>

</div>



<div class="section">

<h2>Understanding Pose Estimation</h2>

<p>
Pose estimation is a computer vision technique used to detect human body joints
from images or videos.
</p>

<p>
Instead of detecting objects, the model detects important points on the body.
These points are called landmarks or keypoints.
</p>

<p>
Examples of landmarks include shoulders, elbows, wrists, hips, knees, and ankles.
</p>

<p>
Once these landmarks are detected, they can be connected to form a skeleton
representation of the human body.
</p>

<p>
This skeleton structure allows us to analyze body movement and measure angles
between joints.
</p>

</div>



<div class="section">

<h2>How Pose Estimation Models Work</h2>

<p>
Most pose estimation systems are built using Convolutional Neural Networks (CNNs).
CNNs are deep learning models designed to understand patterns in images.
</p>

<p>
Instead of directly predicting joint coordinates, the network produces something
called heatmaps.
</p>

<p>
A heatmap represents the probability that a particular body joint exists
at each location in the image.
</p>

<p>
For example, one heatmap is produced for the left shoulder,
another heatmap for the right elbow, another for the wrist, and so on.
</p>

<p>
The brightest point in each heatmap represents the most likely position of that joint.
</p>

<p>
Each detected landmark also has a confidence score which indicates how confident
the model is about the detection.
</p>

<p>
After detecting all landmarks, the system connects them to form the skeleton.
</p>

</div>



<div class="section">

<h2>Frameworks Studied</h2>

<p>
Before implementing the system, several pose detection frameworks were researched.
</p>

<ul>

<li>MediaPipe</li>
<li>MoveNet</li>
<li>OpenPose</li>
<li>Detectron2</li>

</ul>

<h3>OpenPose</h3>

<p>
OpenPose is highly accurate and widely used in research.
However it usually requires GPU acceleration and is relatively heavy
for simple real-time applications.
</p>

<h3>Detectron2</h3>

<p>
Detectron2 is a powerful research framework developed by Facebook.
It supports many tasks but is more complex to set up and configure.
</p>

<h3>MoveNet</h3>

<p>
MoveNet is very fast and optimized for real-time applications,
but integration for this specific Python-based workflow
was slightly less straightforward.
</p>

<h3>MediaPipe</h3>

<p>
MediaPipe provides efficient real-time pose detection,
runs well on CPU, and is easy to integrate with Python.
</p>

</div>



<div class="section">

<h2>Why MediaPipe Was Selected</h2>

<p>
MediaPipe was selected because it offers a good balance between accuracy,
performance, and ease of use.
</p>

<p>
It provides 33 body landmarks which are more than sufficient for analyzing
arms, shoulders, and feet positions required for the exercise.
</p>

<p>
Another advantage is that MediaPipe works efficiently on CPU
and does not require GPU acceleration.
</p>

<p>
Since the goal of the assignment was to build intuition and implement
pose correction logic rather than train a model,
MediaPipe was a practical and reliable choice.
</p>

</div>



<div class="section">

<h2>Project Architecture</h2>

<p>
The project is organized into modular components.
Each module handles a specific responsibility.
</p>

<ul>

<li><b>main.py</b> – application entry point and main loop</li>
<li><b>camera.py</b> – webcam capture</li>
<li><b>pose_engine.py</b> – pose detection using MediaPipe</li>
<li><b>pose_similarity.py</b> – compares user pose with reference pose</li>
<li><b>reference_analyzer.py</b> – extracts pose from reference video</li>
<li><b>workout_controller.py</b> – posture correction rules and rep counting</li>
<li><b>video_controller.py</b> – controls reference exercise video</li>
<li><b>utils.py</b> – mathematical helper functions</li>
<li><b>ui_renderer.py</b> – drawing UI elements and messages</li>

</ul>

<p>
This modular structure keeps the system organized and makes it easier
to maintain or extend in the future.
</p>

</div>



<div class="section">

<h2>Angle Calculation Logic</h2>

<p>
Angles between joints are important for posture analysis.
</p>

<p>
For example, to check whether the arms are straight,
the elbow angle must be calculated.
</p>

<p>
This angle is formed by three points:
</p>

<pre>
shoulder → elbow → wrist
</pre>

<p>
The elbow acts as the vertex of the angle.
</p>

<p>
The angle is calculated using vector mathematics and the dot product formula.
The cosine of the angle between the two vectors is computed
and converted into degrees.
</p>

<p>
If the angle is close to 180 degrees,
the arm is considered straight.
</p>

</div>



<div class="section">

<h2>Pose Correction Rules</h2>

<p>
The correction system checks several posture conditions.
</p>

<ul>

<li>Feet must be slightly apart</li>
<li>Arms must be straight</li>
<li>Hands must be above the head</li>
<li>Palms must be joined</li>
<li>Arms must stay close to the ears</li>

</ul>

<p>
If any of these conditions are not satisfied,
the system displays a correction message
and pauses the reference exercise video.
</p>

<p>
Once the user corrects the posture,
the video resumes.
</p>

</div>



<div class="section">

<h2>Threshold Selection</h2>

<p>
Threshold values were chosen based on geometric reasoning.
</p>

<p>
For example, perfectly straight arms would form a 180 degree angle,
but pose estimation models rarely detect exactly 180 degrees due to
small prediction errors.
</p>

<p>
Therefore angles greater than approximately 165 degrees are treated
as straight arms.
</p>

<p>
Similarly, distance thresholds are selected relative to body proportions
instead of fixed pixel values whenever possible.
</p>

</div>



<div class="section">

<h2>How the System Works</h2>

<p>
The workflow of the system is as follows:
</p>

<ol>

<li>The webcam captures frames continuously.</li>
<li>MediaPipe detects body landmarks from the image.</li>
<li>The skeleton is drawn on the screen.</li>
<li>The system extracts relevant joints such as shoulders, elbows, wrists, and ankles.</li>
<li>Angles and distances between joints are calculated.</li>
<li>The pose correction rules analyze whether the posture is correct.</li>
<li>If the posture is incorrect, a correction message is displayed.</li>

</ol>

</div>



<div class="section">

<h2>How to Run the Project</h2>

<p>
Follow these steps to run the application.
</p>

<h3>1. Install Dependencies</h3>

<pre>
pip install mediapipe opencv-python numpy
</pre>

<h3>2. Download the MediaPipe Pose Model</h3>

<p>
Download the pose landmarker model from the MediaPipe website
and place it in the project folder.
</p>

<h3>3. Run the Application</h3>

<pre>
python main.py
</pre>

<p>
The webcam will start and the system will begin detecting poses.
</p>

</div>



<div class="section">

<h2>Possible Future Improvements</h2>

<ul>

<li>Support multiple exercises</li>
<li>Add pose scoring instead of binary feedback</li>
<li>Use temporal smoothing to stabilize landmarks</li>
<li>Add voice feedback</li>
<li>Support multi-person detection</li>

</ul>

</div>



<div class="section">

<h2>Conclusion</h2>

<p>
This project demonstrates how pose estimation can be combined
with rule-based logic to build an exercise guidance system.
</p>

<p>
By understanding how landmarks are detected and how joint angles
can be calculated, it becomes possible to analyze human posture
and provide real-time feedback.
</p>

<p>
Even without training new models, pose estimation frameworks
make it possible to build practical applications
such as fitness trainers and rehabilitation assistants.
</p>

</div>



</body>
</html>
