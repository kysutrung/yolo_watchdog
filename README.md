![Photo01](https://github.com/kysutrung/multi_zones_safety_assistant_camera/blob/main/mediaa/light_theme_banner.png)

# YOLO Watchdog

Machine Learning Applied Multi-Zone Safety Supervisor Assistant Camera System Project

Keyword: yolov8, esp now, python app, hardware design.

## 📑 Project Description

Building a smart surveillance camera system base on YOLO algorithm. Able to detect the presence of prohibited (weapon, lighter, liquid can, human....) and indispensable objects (protective gear, human who run machine....) in each area at a location (factory, construction site, work place...) for safety reasons. Sending notification to remote monitor unit via ESP NOW. Helps those who work as a safety supervisor to work more effectively.

## ❓ What & Why YOLO Algorithm
__YOLO__ (You Only Look Once) is a real-time object detection algorithm that identifies objects in images or video frames with high speed and accuracy. Unlike traditional methods that scan an image in multiple passes, YOLO processes the entire image in a single forward pass, making it very efficient.

It’s ideal for surveillance cameras due to its real-time detection speed and ability to track multiple objects efficiently.
![Photo01](https://github.com/kysutrung/multi_zones_safety_assistant_camera/blob/main/mediaa/light_theme_banner.png)

## ❓ What & Why ESP-NOW
__ESP-NOW__ is a wireless communication protocol developed by Espressif for direct, low-power, peer-to-peer communication between devices, without the need for a Wi-Fi network. It uses the same 2.4GHz frequency as Wi-Fi but allows devices to send small packets of data to each other instantly, with minimal delay. It supports broadcasting to multiple devices and has a range similar to Wi-Fi.
![Photo01](https://github.com/kysutrung/multi_zones_safety_assistant_camera/blob/main/mediaa/light_theme_banner.png)

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
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## 🛠️ Prototype 001

## 👏 Acknowledgements

## 📞 Support
If you have any questions or suggestions, feel free!!!
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
