video_name="taipei_260_271"
video_input_path="/home/trongan93/Projects/github/satellite-videocoding/video-sequences/${video_name}.yuv"
echo ${video_input_path}
video_output_path="./video-sequences/${video_name}_encoded.mp4"

# encoding
# Ref at https://forum.videohelp.com/threads/397557-ffmpeg-luma-only
# The default mode of H.264
ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx264 -c:a copy ${video_output_path}