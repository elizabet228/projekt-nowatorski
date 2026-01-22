# ===== STAGE 1: build =====
FROM python:3.12 AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===== STAGE 2: runtime =====
FROM python:3.12
WORKDIR /app
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
