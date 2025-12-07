# AMD_Robotics_Hackathon_2025_CookPastaAndRingABell

## Team Information

**Team:** *11, Kenta Konagaya(kufusha.Inc), Taiga Sasaki(kufusha.Inc)*

**Summary:** *We operate a robotics business focused on prototype development and contract development of autonomous mobile robots, as well as system integration for collaborative robots.　(https://www.kufusha.com/)*

## Judging Criteria

### 1. Mission 2 Description (10 points)

Pour a single serving of pasta from a cup into a pasta strainer inside a pot. Return the cup to its designated position. Start the timer (the timer screen turns red and the timer starts). Wait until the timer finishes. When the timer goes off and the screen turns green, transfer the pasta from the strainer to a dish. Ring a bell to signal that the pasta is ready, and the task is complete.

Note: We originally wanted to automate the timer as well, but ran out of time.

### 2. Creativity (30 points)

### Camera Placement
Camera positioning is critical. Consider the following:
1. **Overhead camera**: Can you see the entire workspace?
2. **Side camera**: Can you clearly see the bell handle and the cup being grasped?
3. **Wrist camera**: Is the grasping moment clearly visible?

Carefully determine camera positions to ensure all elements are visible. (We spent about 1 hour just deciding on camera placement.)

#### Camera View Check
We used the following command to check all camera views simultaneously:
```bash
./fix_camera_settings.sh && gst-launch-1.0 \
    compositor name=comp sink_0::xpos=0 sink_1::xpos=640 sink_2::xpos=1280 ! videoconvert ! autovideosink \
    v4l2src device=/dev/video_top ! 'image/jpeg, width=640, height=480, framerate=30/1' ! jpegdec ! videoconvert ! comp.sink_0 \
    v4l2src device=/dev/video_front ! 'image/jpeg, width=640, height=480, framerate=30/1' ! jpegdec ! videoconvert ! comp.sink_1 \
    v4l2src device=/dev/video_arm ! 'image/jpeg, width=640, height=480, framerate=30/1' ! jpegdec ! videoconvert ! comp.sink_2
```

**Camera view screenshot:**

![Camera View](https://github.com/user-attachments/assets/21928376-049c-4234-8425-3e8e1afef314)

### 3. Technical implementations (20 points)

#### Demo Videos

- [AMD Robotics Hackathon 2025 11 kufusha cook pasta n ring bell 1](https://youtu.be/OSZ5TECSqkU)
- [AMD Robotics Hackathon 2025 11 kufusha cook pasta n ring bell 2](https://youtu.be/MVNBf38YdK4)
- [AMD Robotics Hackathon 2025 11 kufusha cook pasta n ring bell 3](https://youtu.be/ZfiCscT35pU)

#### How To Reproduce

##### Environment Setup
We recommend replicating the environment as closely as possible since no additional equipment was used. Pay attention to details such as cup thickness, cup color, and pot angle.

###### USB Device Rules (udev)
To ensure consistent device naming for cameras and robot arms, copy the udev rules file and reload:
```bash
sudo cp mission2/code/99-usb-cameras.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

This creates the following symbolic links:
| Device | Symlink | Description |
|--------|---------|-------------|
| UGREEN Camera | `/dev/video_top` | Overhead camera |
| UGREEN Camera 2K | `/dev/video_front` | Front/side camera |
| USB2.0_CAM1 | `/dev/video_arm` | Wrist camera |
| Serial 5AE6058593 | `/dev/tty_leader` | Leader arm |
| Serial 5AE6054125 | `/dev/tty_follower` | Follower arm |

#### Kitchen Timer (Separate PC)
The `kitchen_timer.py` script should be run on a **separate PC with a display** that the robot can see. This timer displays:
- **White screen**: Waiting to start (press any key to begin)
- **Red screen**: Countdown in progress (3 minutes)
- **Green screen**: Timer finished (robot should transfer pasta)

```bash
# Run on the timer display PC (requires pygame)
pip install pygame
python mission2/code/kitchen_timer.py
```

The robot uses vision to detect the screen color change from red to green.


**Camera setup photos:**

| | | |
|:---:|:---:|:---:|
| ![Setup 1](https://github.com/user-attachments/assets/de33cebc-9eb9-41cb-a317-28529349358a) | ![Setup 2](https://github.com/user-attachments/assets/f13f5c5f-f292-4cf8-ad66-5a0cee0a5d58) | ![Setup 3](https://github.com/user-attachments/assets/9b1a132d-56ee-43f2-ada9-f8e164204620) |
| ![Setup 4](https://github.com/user-attachments/assets/efb0178f-cea7-4969-b2bf-2ec0df071bb2) | ![Setup 5](https://github.com/user-attachments/assets/876c232a-669c-4205-b556-cee62a77db81) | ![Setup 6](https://github.com/user-attachments/assets/4dcb9e62-8385-40d5-9c89-ee04c2f56fe2) |
| ![Setup 7](https://github.com/user-attachments/assets/0663f50e-ec2a-4c06-b4e4-f1720a3a6029) | | |

### Data Collection
We focused on the following points:
1. All movements should be smooth, with sufficient margin for arm range of motion and object manipulation
2. When grasping with the wrist camera, ensure the target object is always visible in the camera
3. We shortened the timer to less than 3 minutes to ensure proper waiting for the color change

### Training
Training was performed with the following configuration:
```bash
lerobot-train \
  --dataset.repo_id=kfstiger/cook_pasta_n_ring_a_bell \
  --batch_size=64 \
  --steps=40000 \
  --save_freq=2000 \
  --output_dir=outputs/train/act_so101_pasta_bell_40ksteps \
  --job_name=act_so101_pasta_bell_40ksteps \
  --policy.device=cuda \
  --policy.type=act \
  --policy.push_to_hub=false \
  --wandb.enable=true
```

### Inference
No special configuration required.

### 4. Ease of use (10 points)

- Since we used commercially available ingredients and cooking utensils, I believe that if we can actually boil the pasta, we will be able to achieve pasta serving.
- Although pasta was used in this project, it is thought that this approach can be applied to other foods that require similar cooking methods (such as rice and ramen).
- For this implementation, we used the lerobot scripts as is.

## Delivery URL

- **Dataset:** https://huggingface.co/datasets/kfstiger/cook_pasta_n_ring_a_bell
- **Model:** https://huggingface.co/kfstiger/cook_pasta_n_ring_a_bell/tree/main

## Related Blog Posts

- [Dual-arm work with Otter Arm](https://www.kufusha.com/works/robotics/w005327/)
- [SmolVLA](https://www.kufusha.com/works/robotics/w006559/)

Directory Tree of this repo,

<template>
    
```terminal
AMD_Robotics_Hackathon_2025_ProjectTemplate-main/
├── README.md
└── mission
    ├── code
    │   └── <code and script>
    └── wandb
        └── <latest run directory copied from wandb of your training job>
```

The `latest-run` is generated by wandb of your training job. Please copy it under the wandb sub direcotry of you Hackathon Repo.

The whole dir of `latest-run` looks like that,

```terminal
$ tree outputs/train/smolvla_so101_2cube_30k_steps/wandb/
outputs/train/smolvla_so101_2cube_30k_steps/wandb/
├── debug-internal.log -> run-20251029_063411-tz1cpo59/logs/debug-internal.log
├── debug.log -> run-20251029_063411-tz1cpo59/logs/debug.log
├── latest-run -> run-20251029_063411-tz1cpo59
└── run-20251029_063411-tz1cpo59
    ├── files
    │   ├── config.yaml
    │   ├── output.log
    │   ├── requirements.txt
    │   ├── wandb-metadata.json
    │   └── wandb-summary.json
    ├── logs
    │   ├── debug-core.log -> /dataset/.cache/wandb/logs/core-debug-20251029_063411.log
    │   ├── debug-internal.log
    │   └── debug.log
    ├── run-tz1cpo59.wandb
    └── tmp
        └── code
```

**NOTES**

1. The `latest-run` is the soft link, please make sure to copy the real target directory it linked with all sub dirs and files.
2. Only provide(upload) the wandb of yourlast success pre-trained model for the Mission.
