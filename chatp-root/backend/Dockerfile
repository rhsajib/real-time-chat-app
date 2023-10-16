# Use an official Python runtime as a parent image
FROM python:3.11.6-alpine

# Set environment variables 
# prevent pip to check its version for upgrade
# ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
# prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1 
# ensure python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app


# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire FastAPI application to the container
COPY . .

# which port the app will use
EXPOSE 8000

# Start the FastAPI app with --reload (for development)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Start the FastAPI app without --reload (for production)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


