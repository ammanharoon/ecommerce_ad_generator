FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config.yaml . 

# Download the base model (T5-base) from Hugging Face
# This creates the model directory structure
RUN python -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; \
    model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-base'); \
    tokenizer = T5Tokenizer. from_pretrained('google/flan-t5-base'); \
    model.save_pretrained('./models/checkpoints/final_model'); \
    tokenizer.save_pretrained('./models/checkpoints/final_model')"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/models/checkpoints/final_model

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]