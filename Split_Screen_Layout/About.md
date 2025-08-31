# Split-Screen Layout

My wife is preparing for OET Exam, and computer based exam will have Reading Part into Split-Screen Layout.

I want a split-screen layout where the left side shows a long passage (scrollable), and the right side shows all the questions (also scrollable). There are a few ways to achieve this depending on whether you want a web-based solution (HTML/CSS/JS) or a Python-based solution (like using Flask, Streamlit, or Tkinter).

Here I am going with Streamlit.

## 🔧 How it Works

1. Upload your PDF.

2. It extracts text using PyPDF2 (Extracts text from the uploaded PDF).

3. Looks for "Questions" keyword to split passage vs. questions (you can adjust this if your PDF uses another word, like "Q1").
   - Splits everything at the "QUESTIONS" keyword.
   - Formats Text A–D as the passage.
   - Detects numbered questions (1., 2. …) and puts them in a list

4. Displays left/right scrollable columns (passage vs. questions).

5. Each question gets its own answer box.


# How to Run

## Option 1 : Local
```sh
# Make sure you have installed the required libraries.
pip install streamlit PyPDF2

# Or
pip install -r requirements.txt
```

Then run the App
```sh
streamlit run split_screen.py
```


## Option 2 : In Docker
```sh
cd /Users/tripathimachine/Desktop/Apps/GitHub_Repo/Python-Playground/Split_Screen_Layout

docker build -t split-screen-app .

# RUn the Docker Container
docker run -p 8501:8501 split-screen-app
```

## Option 3 : Local in Virtual Env.

```sh
conda deactivate

conda create -n splitscreen_venv python=3.10

# Activate
conda activate splitscreen_venv

pip install -r requirements.txt

streamlit run split_screen.py
```