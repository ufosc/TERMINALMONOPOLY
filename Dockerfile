FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Helps with printing
ENV PYTHONUNBUFFERED=1 

# Make port 80 available to the world outside this container
EXPOSE 3131

# Run the server banker.py when the container launches
CMD ["python", "banker.py"]