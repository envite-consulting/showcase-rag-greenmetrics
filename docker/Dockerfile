# Python 3.12 base image
FROM python:3.12-slim@sha256:d75c4b6cdd039ae966a34cd3ccab9e0e5f7299280ad76fe1744882d86eedce0b

# Install curl
RUN apt-get update && apt-get install -y curl

WORKDIR /src

# Install Python packages
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app into the image
COPY src/app /src/app

# Copy scripts and small showcase data. Persistent volumes can override these
# paths at runtime.
COPY src/scripts /src/scripts
COPY src/data /src/data

# FastAPI port
EXPOSE 8000

# Start the API with uvicorn
CMD ["uvicorn", "app.api_client:app", "--host", "0.0.0.0", "--port", "8000"]
