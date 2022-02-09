FROM python:3.8-slim-buster

# Timezone
ENV TZ=Asia/Shanghai

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app

# Set environment variables
ENV HOME=/usr/src/app

CMD python3 main.py --host '127.0.0.1' --port 25542
