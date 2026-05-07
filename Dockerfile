# Hugging Face Space (Docker SDK)
# 정적 파일을 7860 포트로 서빙. URL은 hyojin22c-course3-ai.hf.space
FROM python:3.11-alpine
WORKDIR /app
COPY index.html style.css data.js scoring.js app.js ./
EXPOSE 7860
CMD ["python3", "-m", "http.server", "7860"]
