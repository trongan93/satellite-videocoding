video_name="taipei_260_271"
video_input_path="/home/trongan93/Projects/github/satellite-videocoding/video-sequences/${video_name}.yuv"
echo ${video_input_path}
video_output_path="./video-sequences/${video_name}_encoded.mp4"

# encoding
# The manually mode of H.265/HEVC
# Ref at https://samuel.dalesjo.net/2018/01/06/gop-configuration-with-ffmpeg/ (GOP customization)
# and ref at https://video.stackexchange.com/questions/24680/what-is-keyint-and-min-keyint-and-no-scenecut
# Case 2
#keyint specifies the maximum length of the GOP, so the maximum interval between each keyframe, which remember that can be either an IDR frame or a non-IDR frame. I'm not completely sure but I think that by default ffmpeg will require every I-frame to be an IDR frame, so in practice you can use the terms IDR frame and I-frame interchangeably
#min-keyint specifies the minimum length of the GOP. This is because the encoder might decide that it makes sense to add a keyframe before the keyint value, so you can put a limit
#no-scenecut. When the encoder determines that there's been a scene cut, it may decide to insert an additional I-frame. The issue is that I-frames are very expensive if compared to other frame types, so when encoding for streaming you want to disable it.
ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx265 -x265-params "keyint=12:min-keyint=12:scenecut=0:bframes=0:b-adapt=0:qp=40" -c:a copy ${video_output_path}
# Check the PSNR
ffmpeg -i ${video_output_path} -s 2560x2560 -pix_fmt gray -r 1 -i ${video_input_path} -s 2560x2560 -pix_fmt gray -r 1 -filter_complex "psnr" -f null /dev/null