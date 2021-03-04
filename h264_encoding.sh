video_name="taipei_260_271"
video_input_path="/home/trongan93/Projects/github/satellite-videocoding/video-sequences/${video_name}.yuv"
echo ${video_input_path}
video_output_path="./video-sequences/${video_name}_encoded.mp4"

#encoding
#ffmpeg -hide_banner -y -f image2 -c:v rawvideo -pix_fmt bayer_rggb8 -s:v 1920x1200 -r 3 -start_number 0 -i "${TEST_RAW_DATA_CASE1_RAW_8bit}/%d.bin" -c:v libx264 -vframes 268 "${TEST_RAW_DATA_CASE1_ENCODED_VIDEO}/output.mp4"
#ffmpeg -f rawvideo -pix_fmt gray -s 2560x2560 -r 12 -i ${video_input_path} -c:v libx264 ${video_output_path}

#Ref at https://forum.videohelp.com/threads/397557-ffmpeg-luma-only
ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx264 -c:a copy ${video_output_path}