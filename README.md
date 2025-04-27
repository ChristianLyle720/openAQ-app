# OpenAQ Air Quality App

This is a simple Flask application that uses the OpenAQ API to display air quality information for various locations. The app is designed to be deployed on Google App Engine.

## Project Structure

```
openaq-app/
├── app.py                 # Main Flask application
├── app.yaml               # Google App Engine configuration
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css          # CSS styling
└── templates/
    ├── index.html         # Location selection page
    ├── location.html      # Location details page
    └── error.html         # Error handling page
```

## Setup Instructions

1. **Create the project structure:**

   Create the directories needed for the project:

   ```bash
   mkdir -p openaq-app/static openaq-app/templates
   ```

2. **Copy the files:**

   Copy all the files provided to their respective locations in the project structure.

3. **Install dependencies:**

   ```bash
   cd openaq-app
   pip install -r requirements.txt
   ```

4. **Run locally:**

   ```bash
   python app.py
   ```

   The app will be available at http://127.0.0.1:8080

5. **Deploy to Google App Engine:**

   ```bash
   gcloud init  # If not already initialized
   gcloud app deploy
   ```

## API Key

The application uses an OpenAQ API key which is hardcoded in the app.py file. In a production environment, it's recommended to use environment variables for sensitive information.

## Features

- Select from a list of location IDs (500, 1000, 1500, ..., 8000)
- View detailed location information and metadata
- Display latest air quality measurements from each sensor at the location
- View measurement values with timestamps
- Air Quality Index (AQI) categorization for PM2.5, PM10, and Ozone measurements
- Color-coded AQI indicators for easy interpretation
- Explanatory information about AQI categories and their health implications
- Error handling for API issues or missing data
- Responsive design with clean styling
