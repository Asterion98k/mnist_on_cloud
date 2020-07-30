
FROM python:3.5.6

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY app.py /app/
COPY requirements.txt /app/

# Install packages from requirements.txt
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 8080
EXPOSE 8848

# Run app.py at container launch
CMD ["python", "app.py"]