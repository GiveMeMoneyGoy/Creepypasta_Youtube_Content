# main.py



from datetime import datetime
import os, sys, random



### vars

## python scripts

# main dir filepath
MAIN_DIR_FP = "/home/aryan/Documents/creepypasta_yt_content"

# video module filepath, import py scripts
video_module_fp = MAIN_DIR_FP + "/video_module"
sys.path.insert(1, video_module_fp)
import video_generator

## resources

# bg video
background_video_dir_fp = MAIN_DIR_FP + "/resources/background_video"

# bg audio
background_audio_dir_fp = MAIN_DIR_FP + "/resources/background_audio"
casette_audio_fp = MAIN_DIR_FP + "/resources/casette_insert.mp3"

# thumnails
thumbnails_dir_fp = MAIN_DIR_FP + "/resources/thumbnail_images"

# fonts
horror_fonts_dir_fp = MAIN_DIR_FP + "/resources/horror_fonts"

# video scripts
scripts_dir_fp = MAIN_DIR_FP + "/resources/video_scripts"
awaiting_dir_fp = scripts_dir_fp + "/awaiting"
finished_dir_fp = scripts_dir_fp + "/finished"

# cache dir
cache_dir_fp = MAIN_DIR_FP + "/cache"

# output dir
output_dir_fp = MAIN_DIR_FP + "/output"



# execute

if (len(os.listdir(awaiting_dir_fp)) == 0): sys.exit("Nothing in ./resources/video_scripts/awaiting/, exiting...")

# create output directory for videos
now_str = datetime.now().strftime("%y-%m-%d_%H:%M:%S")
output_vids_dir_fp = output_dir_fp + "/" + now_str
os.system("mkdir " + output_vids_dir_fp)
n_videos_genned = 0

# for every script dir in /resources/video_scripts/awaiting/
for script_dir_name in os.listdir(awaiting_dir_fp):

    # randomize
    bg_video_fp = background_video_dir_fp + "/" + random.choice(os.listdir(background_video_dir_fp))
    bg_audio_fp = background_audio_dir_fp + "/" + random.choice(os.listdir(background_audio_dir_fp))
    thumbnail_bg_fp = thumbnails_dir_fp + "/" + random.choice(os.listdir(thumbnails_dir_fp))
    horror_font_fp = horror_fonts_dir_fp + "/" + random.choice(os.listdir(horror_fonts_dir_fp))

    # get text of script and title
    video_script_dir_fp = awaiting_dir_fp + "/" + script_dir_name
    with open(video_script_dir_fp + "/script.txt", "r") as script_file:
        video_script_text = script_file.read()
    with open(video_script_dir_fp + "/title.txt", "r") as title_file:
        video_script_title = title_file.read()

    # create directory in output directory for this specific video
    n_videos_genned += 1
    specific_vid_dir_fp = output_vids_dir_fp + "/" + str(n_videos_genned)
    os.system("mkdir " + specific_vid_dir_fp)

    # generate video
#    video_generator.generate_video(video_script_text, bg_video_fp, bg_audio_fp, casette_audio_fp, cache_dir_fp, specific_vid_dir_fp + "/vid.mp4")
    video_generator.generate_video("This is a test for the new audio method. I am speaking right now or something.", bg_video_fp, bg_audio_fp, casette_audio_fp, cache_dir_fp, specific_vid_dir_fp + "/vid.mp4")

    # generate thumbnail
    video_generator.generate_thumbnail(thumbnail_bg_fp, horror_font_fp, video_script_title, specific_vid_dir_fp + "/thumbnail.png")

    # move script dir to /finished/
    os.system(f"mv '{video_script_dir_fp}' '{finished_dir_fp}'")
