# Dockerfile-flask

# Simply inherit the Python 3 image.
FROM python:3.9

# Set an environment variable
ENV APP /app

# Create the directory
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# We copy the rest of the codebase into the image
COPY . .

# Finally, we run uWSGI with the ini file
CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]