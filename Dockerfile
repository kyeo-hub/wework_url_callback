# 使用Python 3.9和Alpine作为基础镜像
FROM python:3.9-alpine

# 设置环境变量
ENV APP=/app

# 创建应用目录
RUN mkdir $APP
WORKDIR $APP

# 暴露Gunicorn监听的端口
EXPOSE 5000

# 将requirements.txt文件复制到容器内
COPY requirements.txt .

# 安装必要的依赖包，包括gunicorn、gevent、flask、pycrypto和pybase64
# 需要安装额外的编译工具以便在Alpine上正确构建某些依赖（如gevent）
RUN apk add --no-cache build-base libffi-dev musl-dev && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目源码到容器内
COPY . .

# 设置默认启动命令为运行Gunicorn，并指定配置文件
CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]
