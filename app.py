import streamlit as st
import subprocess

st.set_page_config(page_title="AI Virtual Mouse", layout="centered")
st.title("🖱️ AI Virtual Mouse (OpenCV Only)")

st.markdown("""
Control your system mouse using only your **hand gestures** via webcam:

- 🟦 Move index finger → move cursor  
- 🤏 Pinch index & thumb → left click

> Press `ESC` to stop the virtual mouse window.
""")

if st.button("🚀 Start Virtual Mouse"):
    subprocess.run(["python3", "mouse_controller.py"])
