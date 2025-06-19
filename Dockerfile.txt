FROM python:3.10-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 fonts-liberation libappindicator3-1 xdg-utils \
    libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || true \
    && apt-get -f install -y \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json" | grep -A 1 $CHROME_VERSION | grep -oP '\d+\.\d+\.\d+\.\d+') && \
    wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$DRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64*

# Set display env for headless Chrome
ENV DISPLAY=:99

# Copy project
WORKDIR /tests
COPY . /tests

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run tests
CMD ["pytest", "testcases.py"]