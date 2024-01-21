import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS

import streamlit as st
from short_engine_dir.content_generate import get_response
from short_engine_dir.image_generate import generate_image_for_video
from short_engine_dir.image_editing import create_video
from short_engine_dir.voice_generation import generate_voice
from short_engine_dir.caption_generate import generate_captions
from moviepy.editor import VideoFileClip



st.set_page_config(layout="wide")

ClarifaiStreamlitCSS.insert_default_css(st)

def generate_video(content_topic):
    get_response(content_topic)
    generate_image_for_video()
    generate_voice()
    create_video()
    generate_captions("short_engine_dir/final_video_with_background.mp4")

def short_engine():
    st.image('assets/logo.png')
    st.title("Short Video Engine")
    content_topic = st.text_input("Enter the content topic:")
    if st.button("Generate Video"):
        st.info("Please wait, generating video...")
        generate_video(content_topic)
        st.success("Video generated successfully!")


        final_video_path = "short_engine_dir/output_video.mp4"
        video_clip = VideoFileClip(final_video_path)
        st.video(final_video_path, format="video/mp4", start_time=0)


if __name__ == "__main__":
    short_engine()
