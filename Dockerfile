# Step 1: Use a lightweight Python base image
FROM python:3.10-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy requirements first (for caching)
COPY requirements.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the project files
COPY . /app

# Step 6: Expose Streamlit port
EXPOSE 8501

# Step 7: Environment variable for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true

# Step 8: Command to run your app
CMD ["streamlit", "run", "streamlit_app_pro.py"]