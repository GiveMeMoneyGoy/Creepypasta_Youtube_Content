# video_generator.py



from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from PIL import Image, ImageDraw, ImageFont

from openai import OpenAI
from pathlib import Path
from mutagen.mp3 import MP3
from pydub import AudioSegment

import random, os, textwrap, sys, subprocess



# functions

# function that creates .mp3 of text using OpenAI tts API
def call_openai_tts(text, cache_dir_fp, result_fp):
   
    # initialize client
    client = OpenAI(api_key = "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")

    # split into strings of 4096 chars (openAI tts request character limit)
    request_strings = textwrap.wrap(text, 4096)
    mp3_fps_list = []
    for n_string in range(0, len(request_strings)):
    
        # send request for each string
        response = client.audio.speech.create(

            model = "tts-1",
            voice = "onyx",
            input = request_strings[n_string]
        )

        # write fragmented .mp3s in cache dir
        mp3_fp = f"{cache_dir_fp}/speech_p_{n_string}.mp3"
        mp3_fps_list.append(mp3_fp)
        cache_mp3_fp = Path(mp3_fp)
        response.stream_to_file(cache_mp3_fp)

    # create AudioSegment obj for all sounds, from first element in list
    og_sound = AudioSegment.from_mp3(mp3_fps_list[0])

    # for each fragmented .mp3
    for audio_fp in mp3_fps_list:

        # except for the first
        if audio_fp == mp3_fps_list[0]: continue
            
        # get AudioSegment obj from .mp3 audio fp
        this_sound = AudioSegment.from_mp3(audio_fp)

        # append to universal AudioSegment obj
        og_sound = og_sound.append(this_sound, crossfade = 1500)

    # cleanup
    for audio_fp in mp3_fps_list:
        os.system(f"rm {audio_fp}")
    

    # save universal AudioSegment obj
    og_sound.export(result_fp)

 
# function that generates video
def generate_video(script_str, bg_video_fp, bg_audio_fp, casette_audio_fp, cache_dir_fp, result_fp):


    # create .mp3 of creepypasta script using tts
    vid_nar_fp = cache_dir_fp + "/vid_narration.mp3"
    call_openai_tts(script_str, cache_dir_fp, vid_nar_fp)  

 
    ### get audio

    ## narration audio

    # audio of script .mp3 speech
    speech_audio = (AudioFileClip(vid_nar_fp)\
                    .volumex(1.8))

    ## background audio (music)

    # background audio
    bg_audio = (AudioFileClip(bg_audio_fp)\
                .audio_loop(duration = speech_audio.duration + 8)\
                .audio_fadein(3)\
                .audio_fadeout(3)\
                .volumex(0.18))

    ## audio of casette insert
    casette_audio = (AudioFileClip(casette_audio_fp)\
                    .volumex(0.25))


    # get video
    bg_video = (VideoFileClip(bg_video_fp, audio = False)\
        .loop(duration = speech_audio.duration + 8)\
        .fadein(3)\
        .fadeout(3))


    # compose and build
    res_video = CompositeVideoClip([bg_video])
    res_audio = CompositeAudioClip([bg_audio.set_start(1),\
                                    speech_audio.set_start(4),\
                                    casette_audio.set_start(1)])
    res_video.audio = res_audio


    # write video
    res_video.write_videofile(result_fp)

    # cleanup
    os.system("rm " + vid_nar_fp)

# function that creates a thumbnail
def generate_thumbnail(thumbnail_bg_fp, horror_font_fp, thumbnail_text, result_fp):

    # get image from filepath and make RGBA
    img = Image.open(thumbnail_bg_fp)
    rgbimg = Image.new("RGBA", img.size)
    rgbimg.paste(img)
    img = rgbimg

    # get image width and height
    img_w, img_h = img.size

    # get font and text width and height
    text_height = 100
    fnt = ImageFont.truetype(horror_font_fp, text_height)


    # split text into 30 char lines, get length of longest line and total text height
    lines = textwrap.wrap(thumbnail_text, 30)
    text = ""
    longest_line = 0
    text_total_height = text_height * len(lines)
    for line in lines:
        text += line
        text += "\n"
        if (fnt.getlength(line) > longest_line): longest_line = fnt.getlength(line)

    # calculate distances of text so that it is roughly centered and slightly up
    text_begg_left = (img_w - longest_line) / 2
    text_begg_top = (img_h - text_total_height) / 2 - text_total_height / 10

    # draw
    d = ImageDraw.Draw(img)
    d.multiline_text((text_begg_left, text_begg_top), text, font = fnt, fill = (255, 0, 0))

    # save
    img.save(result_fp)
