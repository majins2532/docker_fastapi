# Use the official FastAPI image as the base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set environment variables
ENV MODULE_NAME="main"
#ENV VARIABLE_NAME="variable_value"

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY ./main.py /app/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
