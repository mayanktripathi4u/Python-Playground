1. Create "server.py"
2. Create "client.py"
3. Create "dockerfile"
4. Build Docker Image
```bash
docker build -t iris-app .

docker images
```
5. Run Docker Container - which will run the FastAPI and expose the Port 8000.
```bash
docker run -p 8000:8000 iris-app
```
6. Run Streamlit App - to run user-interface. 
```bash
streamlit run client.py
```
1. Browse the URL "localhost:8501"
