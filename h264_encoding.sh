video_name="taipei_260_271"
video_input_path="/home/trongan93/Projects/github/satellite-videocoding/video-sequences/${video_name}.yuv"
echo ${video_input_path}
video_output_path="./video-sequences/${video_name}_encoded.mp4"

# encoding
# Ref at https://forum.videohelp.com/threads/397557-ffmpeg-luma-only
# The default mode of H.264
ffmpeg -y -f rawvideo -vcodec rawvideo -pix_fmt gray -s 2560x2560 -r 1 -i ${video_input_path} -codec:v libx264 -c:a copy ${video_output_path}

# Check the psnr
#ffmpeg -i ${video_input_path} -i ${video_output_path} -filter_complex "psnr" -f null /dev/null
#ffmpeg -i ${video_output_path} -i ${video_input_path} "[0:v]scale=2560x2560,format=pix_fmts=gray,fps=fps=1; [1:v]scale=2560x2560,format=pix_fmts=gray,fps=fps=1; [1v][0v]psnr" -f null /dev/null
ffmpeg -i ${video_output_path} -s 2560x2560 -pix_fmt gray -r 1 -i ${video_input_path} -s 2560x2560 -pix_fmt gray -r 1 -filter_complex "psnr" -f null /dev/null
