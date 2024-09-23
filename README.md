![Photo01](https://github.com/kysutrung/multi_zones_safety_assistant_camera/blob/main/mediaa/light_theme_banner.png)

# YOLO Watchdog

Machine Learning Applied Multi-Zone Safety Supervisor Assistant Camera System Project

Keyword: yolov8, esp now, python app, hardware design.

## 📑 Project Description

Building a smart surveillance camera system base on YOLO algorithm. Able to detect the presence of prohibited (weapon, lighter, liquid can, human....) and indispensable objects (protective gear, human who run machine....) in each area at a location (factory, construction site, work place...) for safety reasons. Sending notification to remote monitor unit via ESP NOW. Helps those who work as a safety supervisor to work more effectively.

## ❓ What & Why YOLO Algorithm
__YOLO__ (You Only Look Once) is a real-time object detection algorithm that identifies objects in images or video frames with high speed and accuracy. Unlike traditional methods that scan an image in multiple passes, YOLO processes the entire image in a single forward pass, making it very efficient.

It’s ideal for surveillance cameras due to its real-time detection speed and ability to track multiple objects efficiently.

<br>

<p align="center"><strong>Image Processor Unit Algorithm Diagram</strong></p>

![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/image_processor_diagram.png)

## ❓ What & Why ESP-NOW
__ESP-NOW__ is a wireless communication protocol developed by Espressif for direct, low-power, peer-to-peer communication between devices, without the need for a Wi-Fi network. It uses the same 2.4GHz frequency as Wi-Fi but allows devices to send small packets of data to each other instantly, with minimal delay. It supports broadcasting to multiple devices and has a range similar to Wi-Fi.

<br>

<p align="center"><strong>Remote Monitor Unit Algorithm Diagram</strong></p>

![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/remote_monitor_diagram.jpg)

## 💻 List of Features (working on process)
__Image Processing Unit__
- [x] Objects detection with custom dataset trained model
- [x] Send notification via ESP NOW

__Remote Monitor Unit__
- [x] Receive notification via ESP NOW
- [x] Alert depend on setting
- [ ] Expansion Port

__Window PC App (ESP NOW UNIT needed)__
- [ ] Whole system work right in Windows OS
- [ ] Control UI
- [ ] Display images processed

## 📥 Installation Guide
### 1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement libraries. Check if pip is installed, install if not.

```bash
pip --version
```

__For YOLOv5__

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

__For YOLOv8__

```bash
git clone https://github.com/ultralytics/ultralytics
cd ultralytics
pip install -r requirements.txt
```

__For YOLO training and Python programming__

OpenCV for work with image data from camera. Pyserial for send data via USB port.

```bash
pip install opencv-python
pip install pyserial
```
Check if Pytorch is installed. Find the installation command suitable for your machine on [the official Pytorch website](https://pytorch.org/get-started/locally/) if your machine does not have it installed.

```bash
import torch
print(torch.__version__)   # Kiểm tra phiên bản
print(torch.cuda.is_available())   # Kiểm tra CUDA có khả dụng không
```

__For Raspberry Pi__

[How to install YOLOv8 requirement on Raspberry Pi](https://youtu.be/XzhTq-nk8GQ?si=78NhyxwTwYLjlhmm)

[How to run a program on startup for Raspberry Pi](https://youtu.be/Gl9HS7-H0mI?si=B7nPfKp_ZTQQLSHU) (make sure your Raspberry Pi is set up to run without a display.)

### 2. Train your own YOLO.

Our found some quick but effective video tutorials for you:

[How to train YOLOv8 with custom dataset using your local PC](https://youtu.be/gRAyOPjQ9_s?si=JTgtRKwl3u6fy0oe)

[How to capture and label training data to improve object detection model accuracy using labelImg tool](https://youtu.be/v0ssiOY6cfg?si=RaRrdKB-cuZYgdFo)

[How to fix labelImg crashing while selecting create rect box](https://youtu.be/5jHPuwo8z1o?si=pQSAGxQLbj22FRrF)

### 3. Device Setup

This is how these code work in our system design, you can do the way you want.

__Camera Unit__

"Capture and process image" part - copy [image_processor code](https://github.com/kysutrung/yolo_watchdog/tree/main/image_processor) to sd card of Raspberry Pi, make sure it is in the same folder as the YOLO weight file.

"Notification sender" part - load ESP32 dev board with [alert_sender code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_sender)

__Remote Monitor Unit__

ESP32 Custom Remote Monitor device - load with [custom_remote_monitor code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_receiver/custom_remote_monitor)

or

M5StickCplus2 IOT device - load with [m5stick_receiver code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_receiver/m5_stick_device/m5stick_receiver)

<br>

<p align="center"><strong>System Design Diagram</strong></p>

![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/system_design_diagram.png)

## 🛠️ Prototype 001

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/yolo_cam_prj1.jpg" alt="Mô tả 1" width="500"/>
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/yolo_cam_prj.jpg" alt="Mô tả 2" width="500"/>
</p>



## 👏 References

[Ultralytics](https://github.com/ultralytics/ultralytics) - YOLO

[TheCodingBug](https://www.youtube.com/@TheCodingBug) - YOLO

[Edje Electronics](https://www.youtube.com/@EdjeElectronics) -YOLO

[Freedomwebtech](https://github.com/freedomwebtech) - Raspberry Pi

[Sam Westby](https://www.youtube.com/@SamWestbyTech) - Raspberry Pi

[Big-Bratan](https://github.com/Big-Bratan) - M5stick UI

## 📞 Support
If you have any questions or suggestions, feel free!!!
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
