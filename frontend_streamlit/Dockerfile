# Base image
FROM python:3.12.2-slim

# Working directory
WORKDIR /app

# Copy files
COPY ./ /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
