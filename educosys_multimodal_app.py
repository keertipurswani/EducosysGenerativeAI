import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

from pyngrok import ngrok
public_url = ngrok.connect(8502).public_url
print(f"Public url :  {public_url}")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)

st.title("AI Image Generator")
user_prompt = st.text_input("What do you want to generate image for?")

if st.button("Generate Image"):
    if not user_prompt:
        st.warning("Please enter the prompt!")
    else:
        try:
            with st.spinner("Generating image..."):
                response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
            
            st.subheader("Generated Image")
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    st.write(part.text)
                elif part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    st.image(image)
                
        except Exception as e:
            st.error("Error generating image")

st.title("AI Image Caption Generator")

uploaded_image = st.file_uploader("Upload an image for caption generation", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating caption..."):
                response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["What is this image?", image])
                st.subheader("Generated Caption:")
                st.write(response.text)
        except Exception as e:
            st.error("Error generating caption")

st.title("AI YouTube Video Summarizer")
youtube_url = st.text_input("Enter YouTube Video URL")

if st.button("Summarize Video"):
    if not youtube_url:
        st.warning("No YouTube URL Present!")
    else:
        try:
            with st.spinner("Generating summary..."):
                response = client.models.generate_content(
                    model='models/gemini-2.0-flash',
                    contents=types.Content(
                        parts=[
                            types.Part(text='Can you summarize this video?'),
                            types.Part(
                                file_data=types.FileData(file_uri=youtube_url)
                            )
                        ]
                    )
                )
            st.subheader("Video Summary")
            st.write(response.text)
        except Exception as e:
            st.error("Error generating summary")
        


