docker build -t my-streamlit-app .
docker run -p 8501:8501 --env-file .env my-streamlit-app