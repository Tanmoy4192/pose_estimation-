<h1>Pose Estimation and Correction Engine</h1>

<h2>Overview</h2>
<p>
This project implements a <b>real-time pose estimation and correction system</b> for a guided yoga exercise using <b>MediaPipe Pose Landmarker</b>.
</p>

<p>
The system detects body landmarks from a webcam stream and evaluates whether the user is performing the posture correctly using <b>rule-based logic</b>.
</p>

<p>The goal of this assignment was to:</p>

<ul>
<li>Understand pose estimation concepts</li>
<li>Detect body landmarks in real time</li>
<li>Implement pose correction logic</li>
<li>Guide a user through a timed exercise cycle</li>
</ul>

<hr>

<h2>Exercise Description</h2>

<p>The exercise performed in this system is:</p>

<ol>
<li>Stand erect with feet <b>6 inches (≈15 cm) apart</b></li>
<li>Lift both hands above the head to full stretch</li>
<li>Join the palms and fingers together</li>
<li>Keep arms <b>close to the ears</b></li>
<li>Hold the posture for <b>four breaths (~12 seconds)</b></li>
<li>Bring the arms down to the thighs</li>
<li>Rest for <b>two breaths (~6 seconds)</b></li>
<li>Repeat the cycle</li>
</ol>

<p>The system monitors these conditions and provides <b>real-time feedback</b>.</p>

<hr>

<h2>Pose Estimation Concepts</h2>

<p>
Pose estimation detects <b>human body keypoints (landmarks)</b> from an image.
</p>

<p>Examples of landmarks include:</p>

<ul>
<li>Shoulders</li>
<li>Elbows</li>
<li>Wrists</li>
<li>Hips</li>
<li>Knees</li>
<li>Ankles</li>
</ul>

<p>Each landmark includes:</p>

<ul>
<li>X coordinate</li>
<li>Y coordinate</li>
<li>Visibility / confidence score</li>
</ul>

<p>
These landmarks allow geometric relationships between body joints to be computed.
</p>

<hr>

<h2>How CNN Models Detect Joints</h2>

<p>Modern pose estimation models use <b>Convolutional Neural Networks (CNNs)</b>.</p>

<p>The general process works as follows:</p>

<ol>
<li>The input image is processed by a CNN.</li>
<li>The network predicts <b>heatmaps</b> for each body joint.</li>
<li>Each heatmap represents the probability that a joint exists at a pixel location.</li>
<li>The highest probability location in the heatmap is selected as the joint position.</li>
</ol>

<p>
Confidence scores indicate the reliability of each landmark detection.
</p>

<hr>

<h2>Framework Comparison</h2>

<table border="1">
<tr>
<th>Framework</th>
<th>Keypoints</th>
<th>Performance</th>
<th>Hardware</th>
<th>Integration</th>
<th>Notes</th>
</tr>

<tr>
<td>MediaPipe</td>
<td>33</td>
<td>Real-time</td>
<td>CPU</td>
<td>Easy</td>
<td>Lightweight and optimized</td>
</tr>

<tr>
<td>MoveNet</td>
<td>17</td>
<td>Real-time</td>
<td>CPU/GPU</td>
<td>Moderate</td>
<td>TensorFlow based</td>
</tr>

<tr>
<td>OpenPose</td>
<td>25+</td>
<td>Slower</td>
<td>GPU recommended</td>
<td>Complex</td>
<td>Highly accurate</td>
</tr>

<tr>
<td>Detectron2</td>
<td>Flexible</td>
<td>Slower</td>
<td>GPU</td>
<td>Complex</td>
<td>Research-focused</td>
</tr>

</table>

<hr>

<h2>Framework Selection</h2>

<p>
<b>MediaPipe Pose Landmarker</b> was selected because:
</p>

<ul>
<li>Provides <b>33 body landmarks</b></li>
<li>Optimized for <b>real-time CPU performance</b></li>
<li>Easy Python integration</li>
<li>Lightweight and suitable for interactive applications</li>
<li>Includes tracking and smoothing functionality</li>
</ul>

<p>
Since the goal of this assignment is <b>pose correction rather than model training</b>, MediaPipe allows fast and reliable implementation.
</p>

<hr>

<h2>System Architecture</h2>

<pre>
main.py
│
├── pose_engine.py
│   Pose detection and skeleton drawing
│
├── correct_engine.py
│   Pose correction logic and repetition tracking
│
└── utils.py
    Mathematical utilities for angle and distance calculation
</pre>

<p><b>Processing Pipeline</b></p>

<pre>
Webcam Frame
      ↓
MediaPipe Pose Detection
      ↓
Landmark Extraction
      ↓
Pose Correction Engine
      ↓
User Feedback
</pre>

<hr>

<h2>Pose Correction Logic</h2>

<h3>Feet Distance</h3>

<p>The exercise requires feet approximately <b>15 cm apart</b>.</p>

<p>
Pixel distances vary depending on camera distance, so body-relative normalization is used:
</p>

<pre>
ratio = feet_distance / shoulder_width
</pre>

<p>Accepted range:</p>

<pre>
0.40 ≤ ratio ≤ 0.55
</pre>

<p>
Using shoulder width ensures the measurement remains <b>scale-independent</b>.
</p>

<hr>

<h3>Arm Straightness</h3>

<p>Arm straightness is measured using the elbow angle.</p>

<p>The angle between three points is calculated using the vector dot product formula:</p>

<pre>
cos(θ) = (BA · BC) / (|BA| |BC|)
</pre>

<p>Where:</p>

<ul>
<li>B = elbow</li>
<li>A = shoulder</li>
<li>C = wrist</li>
</ul>

<p>The final angle is calculated using:</p>

<pre>
θ = arccos(...)
</pre>

<p>Arms are considered straight when:</p>

<pre>
angle > 165°
</pre>

<hr>

<h3>Arms Above Head</h3>

<pre>
wrist_y < shoulder_y
</pre>

<hr>

<h3>Arms Close to Ears</h3>

<pre>
distance(wrist, ear) < 0.3 × shoulder_width
</pre>

<hr>

<h3>Palms Joined</h3>

<pre>
distance(left_wrist, right_wrist) < 0.2 × shoulder_width
</pre>

<hr>

<h2>Exercise State Machine</h2>

<pre>
IDLE → HOLDING → RESTING → REP++
</pre>

<p><b>Holding Phase</b></p>
<p>User maintains the posture for approximately <b>12 seconds</b>.</p>

<p><b>Rest Phase</b></p>
<p>Arms lowered to thighs for approximately <b>6 seconds</b>.</p>

<p><b>Repetition Counter</b></p>
<p>A repetition is counted after completing one full hold + rest cycle.</p>

<hr>

<h2>Features</h2>

<ul>
<li>Real-time pose detection</li>
<li>Skeleton visualization</li>
<li>Pose correction feedback</li>
<li>Hold timer</li>
<li>Rest timer</li>
<li>Repetition counter</li>
<li>Landmark coordinate output</li>
<li>FPS display</li>
</ul>

<hr>

<h2>Installation</h2>

<pre>
pip install mediapipe opencv-python numpy
</pre>

<hr>

<h2>Model File</h2>

<p>Download the MediaPipe Pose Landmarker model:</p>

<pre>
pose_landmarker_heavy.task
</pre>

<p>
Official source:
</p>

<p>
https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
</p>

<p>
Place the file in the project root directory.
</p>

<hr>

<h2>Running the Project</h2>

<pre>
python main.py
</pre>

<p>Press <b>Q</b> to exit the program.</p>

<hr>

<h2>Author</h2>

<p><b>Tanmoy Samanta</b></p>
