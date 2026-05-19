FROM python:3.11-slim

WORKDIR /app

# Copia requirements primeiro (cache melhor)
COPY requirements-without-torch.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir \
  torch==2.12.0+cpu \
  torchvision==0.27.0+cpu \
  torchaudio==2.11.0+cpu \
  --index-url https://download.pytorch.org/whl/cpu

# Copia o código do servidor
COPY Server/ /app/Server/

WORKDIR /app/Server

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]