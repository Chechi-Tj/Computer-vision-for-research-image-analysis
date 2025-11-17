import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import os
import tempfile
import zipfile

st.title("MOTAI – Automated Counter 🥚🪰")

# -----------------------------
# Define fixed thresholds
# -----------------------------
EGG_THRESHOLD = 0.45
FLY_THRESHOLD = 0.1   # you can set a different cutoff for flies if needed

# -----------------------------
# Model directory inside repo
# -----------------------------
MODEL_DIR = "models"

# -----------------------------
# Dropdown: what to count?
# -----------------------------
task = st.selectbox(
    "Choose what you want to count:",
    ["Eggs", "Flies"]
)

# -----------------------------
# Load the corresponding YOLO model
# -----------------------------
if task == "Eggs":
    model_path = os.path.join(MODEL_DIR, "eggs_best.pt")
    model = YOLO(model_path)
    CONF_THRESHOLD = EGG_THRESHOLD
    label_prefix = "egg"
else:
    model_path = os.path.join(MODEL_DIR, "flies_best.pt")
    model = YOLO(model_path)
    CONF_THRESHOLD = FLY_THRESHOLD
    label_prefix = "fly"

# -----------------------------
# Function to run inference
# -----------------------------
def run_inference(image: np.ndarray, model, threshold: float):
    results = model.predict(source=image, conf=threshold, save=False, verbose=False)
    filtered_boxes = [box for box in results[0].boxes if box.conf > threshold]
    count = len(filtered_boxes)
    annotated_img = results[0].plot()
    return count, annotated_img

# -----------------------------
# File uploader
# -----------------------------
uploaded_files = st.file_uploader(
    f"Upload one or more images to count {task.lower()}",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            image = np.array(Image.open(file).convert("RGB"))

            # Run inference with correct model + threshold
            count, annotated_img = run_inference(image, model, CONF_THRESHOLD)

            # Save annotated image
            annotated_path = os.path.join(temp_dir, f"annotated_{label_prefix}_{file.name}")
            cv2.imwrite(annotated_path, cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))

            # Record count
            results.append({"Filename": file.name, f"{task} Count": count})

        # Save CSV
        df = pd.DataFrame(results)
        csv_path = os.path.join(temp_dir, f"{label_prefix}_counts.csv")
        df.to_csv(csv_path, index=False)

        # Create ZIP file
        zip_path = os.path.join(temp_dir, f"MOTAI_{label_prefix}_results.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
            for img_file in os.listdir(temp_dir):
                if img_file.startswith("annotated_"):
                    zipf.write(os.path.join(temp_dir, img_file), img_file)

        # Download button
        with open(zip_path, "rb") as f:
            st.download_button(
                label=f"📥 Download {task.lower()} results (CSV + annotated images)",
                data=f,
                file_name=os.path.basename(zip_path),
                mime="application/zip"
            )