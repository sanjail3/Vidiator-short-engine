from faster_whisper import WhisperModel
import json
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip, ColorClip
import os


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"



TextClip.PATH_TO_IMAGEMAGICK = 'ImageMagick-7.0.11-Q16-HDRI/magick.exe'




model_size = "small"
model = WhisperModel(model_size)

segments, info = model.transcribe("short_engine_dir/output.wav", word_timestamps=True)
segments = list(segments)

wordlevel_info = []

for segment in segments:
    for word in segment.words:
        start_v = float(word.start)
        end_v = float(word.end)
        wordlevel_info.append({'start': start_v, 'end': end_v, 'word': word.word})

with open('short_engine_dir/data.json', 'w') as f:
    json.dump(wordlevel_info, f, indent=4)

with open('short_engine_dir/data.json', 'r') as f:
    wordlevel_info_modified = json.load(f)


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"





def split_text_into_lines(data):

    MaxChars = 25
    #maxduration in seconds
    MaxDuration = 2.5
    #Split if nothing is spoken (gap) for these many seconds
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0
    line_chars = 0


    for idx,word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)


        # Check if adding a new word exceeds the maximum character count or duration
        new_line_chars = len(temp)

        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx>0:
          gap = word_data['start'] - data[idx-1]['end']
          # print (word,start,end,gap)
          maxgap_exceeded = gap > MaxGap
        else:
          maxgap_exceeded = False


        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0
                line_chars = 0


    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles


linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)

for line in linelevel_subtitles:
  json_str = json.dumps(line, indent=4)
<<<<<<< HEAD

=======
 
>>>>>>> 1e2f697b458914ba6c2331653d587beba3ecfcd8


def create_caption(textJSON, framesize,font = "Aerial",color='white', highlight_color='yellow',stroke_color='black',stroke_width=1.5):
    wordcount = len(textJSON['textcontents'])
    full_duration = textJSON['end']-textJSON['start']

    word_clips = []
    xy_textclips_positions =[]

    x_pos = 0
    y_pos = 0
    line_width = 0  # Total width of words in the current line
    frame_width = framesize[0]
    frame_height = framesize[1]

    x_buffer = frame_width*1/10

    max_line_width = frame_width - 2 * (x_buffer)

    fontsize = int(frame_height * 0.055) #7.5 percent of video height

    space_width = ""
    space_height = ""

    for index,wordJSON in enumerate(textJSON['textcontents']):
      duration = wordJSON['end']-wordJSON['start']
      word_clip = TextClip(wordJSON['word'], font = font,fontsize=fontsize, color=color,stroke_color=stroke_color,stroke_width=stroke_width).set_start(textJSON['start']).set_duration(full_duration)
      word_clip_space = TextClip(" ", font = font,fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
      word_width, word_height = word_clip.size
      space_width,space_height = word_clip_space.size
      if line_width + word_width+ space_width <= max_line_width:
            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos,
                "y_pos": y_pos,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width, y_pos))

            x_pos = x_pos + word_width+ space_width
            line_width = line_width+ word_width + space_width
      else:
            # Move to the next line
            x_pos = 0
            y_pos = y_pos+ word_height+10
            line_width = word_width + space_width

            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos,
                "y_pos": y_pos,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width , y_pos))
            x_pos = word_width + space_width


      word_clips.append(word_clip)
      word_clips.append(word_clip_space)


    for highlight_word in xy_textclips_positions:

      word_clip_highlight = TextClip(highlight_word['word'], font = font,fontsize=fontsize, color=highlight_color,stroke_color=stroke_color,stroke_width=stroke_width).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
      word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
      word_clips.append(word_clip_highlight)

    return word_clips,xy_textclips_positions



def generate_captions(video_name):
    input_video = VideoFileClip(video_name)
    frame_size = input_video.size

    all_linelevel_splits = []

    for line in linelevel_subtitles:
        out_clips, positions = create_caption(line, frame_size)

        max_width = 0
        max_height = 0

        for position in positions:
            # print (out_clip.pos)
            # break
            x_pos, y_pos = position['x_pos'], position['y_pos']
            width, height = position['width'], position['height']

            max_width = max(max_width, x_pos + width)
            max_height = max(max_height, y_pos + height)

        color_clip = ColorClip(size=(int(max_width * 1.3), int(max_height * 1.1)),
                               color=(64, 64, 64))
        color_clip = color_clip.set_opacity(.8)
        color_clip = color_clip.set_start(line['start']).set_duration(line['end'] - line['start'])

        # centered_clips = [each.set_position('center') for each in out_clips]

        clip_to_overlay = CompositeVideoClip([color_clip] + out_clips)
        clip_to_overlay = clip_to_overlay.set_position("bottom")

        all_linelevel_splits.append(clip_to_overlay)

    input_video_duration = input_video.duration

    final_video = CompositeVideoClip([input_video] + all_linelevel_splits)

    final_video = final_video.set_audio(input_video.audio)

    final_video.write_videofile("output_video.mp4", fps=24, codec="libx264", audio_codec="aac")






