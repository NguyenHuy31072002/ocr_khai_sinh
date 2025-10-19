# FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install -y \
#     build-essential wget curl git ffmpeg \
#     libgl1 libglib2.0-0 python3.10 python3.10-dev python3.10-distutils python3.10-venv \
#     && rm -rf /var/lib/apt/lists/*

# RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
#     python3.10 get-pip.py && rm get-pip.py

# RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
#     ln -sf /usr/bin/python3.10 /usr/bin/python3

# WORKDIR /workspace

# COPY setup.txt .
# RUN pip install --upgrade pip && pip install -r setup.txt


# COPY . .

# EXPOSE 8000

# CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]






FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3.10-distutils \
    python3-pip build-essential ffmpeg git libgl1 libglib2.0-0

RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    python -m pip install --upgrade pip

WORKDIR /workspace
COPY setup.txt .
RUN pip install -r setup.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
