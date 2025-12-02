import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import requests
from datetime import datetime

# Download model from your release (only once)
@st.cache_resource
def load_model():
    model_path = "my_preschool_ai.h5"
    if not os.path.exists(model_path):
        with st.spinner("Downloading your AI model (30–60 sec, only first time)..."):
            url = "https://github.com/Shafreena236/preschool-ai-website/releases/download/v1/my_preschool_ai.h5"
            r = requests.get(url)
            with open(model_path, "wb") as f:
                f.write(r.content)
    return tf.keras.models.load_model(model_path)

model = load_model()

st.set_page_config(page_title="2 Nursery AI", page_icon="pencil")
st.title("2 Nursery Worksheet AI Evaluator")
st.caption("Upload any worksheet → get instant score")

teacher = st.text_input("Teacher Name")
student = st.text_input("Student Name")
uploaded = st.file_uploader("Upload worksheet photo", type=["jpg","jpeg","png"])

if uploaded and teacher and student:
    image = Image.open(uploaded).convert("RGB")
    img = image.resize((224,224))
    arr = np.array(img)[None,...]/255.0
    
    pred = model.predict(arr, verbose=0)
    score = np.argmax(pred) + 1

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, use_column_width=True)
    with col2:
        st.metric("Score", f"{score}/5")
        skill = "Well Skilled" if score >= 4 else "Approaching Secure" if score == 3 else "Needs Practice"
        st.write(f"**Skill Level**: {skill}")
        if score == 5: st.balloons()

    if st.button("Save Result"):
        os.makedirs("saved", exist_ok=True)
        image.save(f"saved/{student}_{score}_{datetime.now().strftime('%d%b')}.jpg")
        st.success("Saved successfully!")

st.caption("Your personal AI evaluator ❤️")
