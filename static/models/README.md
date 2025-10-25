## ⚠️ Attribution & Licensing

This project relies on external libraries and pre-trained models. These files are **NOT** the original work of this project's author.

### 1. Face Detection Library

* **Component:** `face-api.js` (JavaScript Library)
* **Purpose:** Used for real-time face detection, landmark detection, and biometric scanning in the video feed.
* **Original Author:** Vincent Mühler (justadudewhohacks) and contributors (as well as Vlad Mandic for later versions).
* **Source:** [https://github.com/justadudewhohacks/face-api.js](https://github.com/justadudewhohacks/face-api.js)
* **License:** MIT License (See repository for full details)

### 2. Neural Network Models

The files located in the `static/models/` directory are pre-trained neural network weights.

* **Models:** `tiny_face_detector_model`, `face_landmark_68_model`
* **Purpose:** Provide the intelligence for the face detection and landmark algorithms.
* **Origin:** Derived from the models packaged with the `face-api.js` library.
* **License:** These models are typically governed by the same license as the library (MIT License) but are ultimately based on models trained using various public datasets.