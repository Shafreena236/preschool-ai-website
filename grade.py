import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from datetime import datetime
import requests

# Download model from GitHub Release (runs only once)
@st.cache_resource
def load_model():
    model_path = "my_preschool_ai.h5"
    if not os.path.exists(model_path):
        with st.spinner("Downloading your AI model for the first time... (30–60 sec)"):
            url = "https://github.com/Shafreena236/preschool-ai-website/releases/download/v1/my_preschool_ai.h5"
            r = requests.get(url, stream=True)
            with open(model_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    return tf.keras.models.load_model(model_path)

model = load_model()

# App UI
st.set_page_config(page_title="2 Nursery AI Evaluator", page_icon="pencil")
st.title("2 Nursery Worksheet AI Evaluator")
st.caption("Made with love for teachers")

teacher")

teacher = st.text_input("Teacher Name")
student = st.text_input("Student Name")
class_name = st.selectbox("Class", ["Playgroup", "Nursery", "LKG", "UKG"])

uploaded = st.file_uploader("Upload worksheet photo", type=["jpg","jpeg","png"])

if uploaded and teacher and student:
    image = Image.open(uploaded).convert("RGB")
    img = image.resize((224,224))
    arr = np.array(img)[None,...]/255.0
    
    with st.spinner("AI is evaluating..."):
        pred = model.predict(arr, verbose=0)
        score = np.argmax(pred)+1

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, use_column_width=True)
    with col2:
        st.metric("Score", f"{score}/5", delta=None)
        if score >= 5:
            st.balloons()
            st.success("Excellent! Super star!")
        elif score >= 4:
            st.success("Very good!")
        elif score >= 3:
            st.info("Good effort!")
        else:
            st.warning("Needs more practice")

        st.write(f"**Skill Level**: {'Well Skilled' if score >= 4 else 'Approaching Secure' if score == 3 else 'Needs Practice'}")

    if st.button("Save Result"):
        os.makedirs("saved", exist_ok=True)
        image.save(f"saved/{student}_{score}of5_{datetime.now().strftime('%d%b')}.jpg")
        st.success("Saved!")

st.markdown("---")
st.caption("Your personal AI teacher assistant • Built by Shafreena")
