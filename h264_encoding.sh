video_name="taipei_260_271"
video_input_path="/home/trongan93/Projects/github/satellite-videocoding/video-sequences/${video_name}.yuv"
echo ${video_input_path}
video_output_path="./video-sequences/${video_name}_encoded.mp4"

# encoding
## Ref at https://forum.videohelp.com/threads/397557-ffmpeg-luma-only
## The default mode of H.264
## Case 1
#ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx264 -c:a copy ${video_output_path}
## Check the PSNR
#ffmpeg -i ${video_output_path} -s 2560x2560 -pix_fmt gray -r 1 -i ${video_input_path} -s 2560x2560 -pix_fmt gray -r 1 -filter_complex "psnr" -f null /dev/null

# The manually mode of H.264
# Ref at https://samuel.dalesjo.net/2018/01/06/gop-configuration-with-ffmpeg/ (GOP customization)
# Case 2
ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx264 -x264-params keyint=4:min-keyint=4:scenecut=0:bframes=0:b-adapt=0:b-adapt=0:open-gop=1 -c:a copy ${video_output_path}
# Check the PSNR
ffmpeg -i ${video_output_path} -s 2560x2560 -pix_fmt gray -r 1 -i ${video_input_path} -s 2560x2560 -pix_fmt gray -r 1 -filter_complex "psnr" -f null /dev/null