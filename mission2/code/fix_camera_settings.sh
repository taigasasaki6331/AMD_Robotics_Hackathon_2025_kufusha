#!/bin/bash
# カメラのホワイトバランス・露出を固定するスクリプト

# 設定値（必要に応じて調整）
WB_TEMP_ARM=3200           # ホワイトバランス温度 (2800-6500)
EXPOSURE_ARM=70           # 露出時間 (1-5000)

echo "=== カメラ設定を固定します ==="

# video_arm
echo "[video_arm]"
v4l2-ctl -d /dev/video_arm --set-ctrl=white_balance_automatic=0
v4l2-ctl -d /dev/video_arm --set-ctrl=white_balance_temperature=$WB_TEMP_ARM
v4l2-ctl -d /dev/video_arm --set-ctrl=auto_exposure=1
v4l2-ctl -d /dev/video_arm --set-ctrl=exposure_time_absolute=$EXPOSURE_ARM
v4l2-ctl -d /dev/video_arm --set-ctrl=exposure_dynamic_framerate=0
echo "  WB: manual ($WB_TEMP_ARM K), Exposure: manual ($EXPOSURE_ARM)"_ARM

# video_front (露出制御なし)
echo "[video_front]"
v4l2-ctl -d /dev/video_front --set-ctrl=white_balance_automatic=0
echo "  WB: manual (温度設定なし), Exposure: 制御不可"

# video_top
WB_TEMP_TOP=3700           # ホワイトバランス温度 (2800-6500)
EXPOSURE_TOP=60           # 露出時間 (1-5000)
echo "[video_top]"
v4l2-ctl -d /dev/video_top --set-ctrl=white_balance_automatic=0
v4l2-ctl -d /dev/video_top --set-ctrl=white_balance_temperature=$WB_TEMP_TOP
v4l2-ctl -d /dev/video_top --set-ctrl=auto_exposure=1
v4l2-ctl -d /dev/video_top --set-ctrl=exposure_time_absolute=$EXPOSURE_TOP
v4l2-ctl -d /dev/video_top --set-ctrl=exposure_dynamic_framerate=0
echo "  WB: manual ($WB_TEMP_TOP K), Exposure: manual ($EXPOSURE_TOP)"_TOP

echo ""
echo "=== 設定完了 ==="
echo "現在の設定を確認するには:"
echo "  v4l2-ctl -d /dev/video_arm --list-ctrls"
