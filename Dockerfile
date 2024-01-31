# 第一阶段：构建/安装
FROM python:3.9 AS builder

ENV APP /app
WORKDIR $APP

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# 第二阶段：生产环境镜像
FROM python:3.9-alpine

ENV APP /app
WORKDIR $APP

# 安装 gunicorn 及其依赖（包括 gcc 和 libc-dev）
RUN apk add --update --no-cache gcc libc-dev && \
    pip install --no-cache-dir gunicorn

# 将第一阶段构建的应用和依赖复制到此阶段
COPY --from=builder $APP .

EXPOSE 5000
CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]
