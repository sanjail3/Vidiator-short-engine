import os
from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


def create_video():

    image_directory = "short_engine_dir/images"


    image_files = [f for f in os.listdir(image_directory) if f.endswith(".jpg")]
    image_files.sort()


    image_clips = []


    audio_duration = AudioFileClip("short_engine_dir/output.wav").duration
    image_count = len(image_files)
    image_duration = audio_duration / image_count


    width, height = 1080, 1980
    fade_duration = 1


    def slide_from_left_to_right(image_clip, frame_index):
        t = frame_index / image_clip.fps
        x_position = -1024 + (1920 * t / image_duration)
        scaled_clip = image_clip.resize((1080, 1980))
        return scaled_clip.set_position((x_position, 'center')).set_duration(1 / image_clip.fps)


    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        image_clip = ImageSequenceClip([image_path], fps=1 / image_duration)


        fadein_clip = fadein(image_clip, fade_duration)
        fadeout_clip = fadeout(image_clip, fade_duration)


        sliding_image_clips = [slide_from_left_to_right(fadein_clip, i) for i in range(int(fadein_clip.fps))]
        sliding_image_clips.append(fadeout_clip)

        image_clips.extend(sliding_image_clips)


    final_video = concatenate_videoclips(image_clips, method="compose")


    final_video = final_video.resize((1080, 1980))


    audio = AudioFileClip("short_engine_dir/output.wav")


    final_video = final_video.set_audio(audio)


    background_audio = AudioFileClip("short_engine_dir/background-music.mp3")


    if background_audio.duration > final_video.duration:
        background_audio = background_audio.subclip(0, final_video.duration)

    final_audio = CompositeAudioClip([audio.volumex(1.0), background_audio.volumex(0.2)])


    final_video = final_video.set_audio(final_audio)



    final_video.write_videofile("short_engine_dir/final_video_with_background.mp4", codec="libx264", fps=30)


