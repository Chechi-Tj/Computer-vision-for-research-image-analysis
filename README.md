# MOTAI – Automated Counter for Flies and Eggs

### YOLO-powered image detection and counting tool for research

MOTAI is a lightweight computer-vision tool designed for biological researchers. It automates the counting of Drosophila flies and eggs from images using YOLO models.

### ⚠️ Note: This app requires OpenCV (cv2) and can only be run locally. It is not compatible with Streamlit Cloud or other online hosting platforms.

## 🚀 Features

- Detects and counts Drosophila eggs and adult flies
- Works with single or multiple uploaded images
- Outputs:
  - Annotated images with bounding boxes
  - A CSV file with image-wise counts
  - A ZIP file containing all results

📂 Repository Structure

Computer-vision-for-research-image-analysis/  
│  
├── app/  
│      └── app.py             # Streamlit app  
│  
├── models/  
│   ├── best_eggs.pt       # YOLO model for eggs  
│   └── best_flies.pt      # YOLO model for flies  
│  
├── demo_images/           # Small sample images for testing  
│   ├── egg_sample1.jpg  
│   └── fly_sample1.jpg  
│  
├── requirements.txt       # Python dependencies  
└── README.md  

Note: Full training datasets are not included to keep the repository lightweight.

## 🖥️ Installation (Local Only)
- ### Clone the repository  
git clone https://github.com/Chechi-Tj/Computer-vision-for-research-image-analysis.git  
cd Computer-vision-for-research-image-analysis

- ### Create a virtual environment (recommended)  
python3 -m venv venv  
source venv/bin/activate   # Linux / Mac  
venv\Scripts\activate      # Windows  

- ### Install dependencies  
pip install -r requirements.txt


Make sure your system has Python 3.10–3.12 for compatibility with OpenCV and YOLO.

## ▶️ Running the App Locally

### From the project root:  
streamlit run app/app.py

The app will open in your default browser
