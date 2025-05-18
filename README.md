# CBT Therapy Advisor API

A FastAPI application that uses OpenAI's fine-tuned models to provide Cognitive Behavioral Therapy (CBT) technique recommendations based on patient information.

## Overview

This API serves as the backend for the CBT Therapy Advisor application. It leverages fine-tuned OpenAI models to:

1. Analyze patient information
2. Recommend appropriate CBT techniques
3. Provide implementation guidance based on the patient's profile
4. Suggest possible diagnoses

## Technical Stack

- **Framework**: FastAPI
- **AI Models**: Fine-tuned OpenAI GPT models
- **Python**: 3.8+
- **Deployment**: Compatible with Render (configured via render.yml)

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key.

## Running the API
with Uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### GET /
Returns a health check message.

### POST /api/completion
Analyzes patient information and returns personalized CBT techniques.

**Request body:**
```json
{
  "prompt": "Patient information including personal details, presenting problem, etc.",
  "model": "ft:gpt-4o-mini-2024-07-18:personal:cbt-clf-v1:BYBtmgda:ckpt-step-126",
  "temperature": 0.2
}
```

**Response:**
```json
{
  "data": [
    {
      "name": "CBT technique name",
      "description": "Description of the technique",
      "implementation": "Implementation plan tailored to patient",
      "possible_diagnosis": "Possible diagnoses (comma-separated)"
    },
    {
      "name": "Another technique",
      "description": "...",
      "implementation": "...",
      "possible_diagnosis": "..."
    }
  ]
}
```

## How It Works

1. The API processes patient information using a fine-tuned GPT model to identify applicable CBT techniques
2. For each identified technique, it generates a personalized implementation plan
3. It also suggests possible diagnoses based on the patient information
4. All data is returned in a structured JSON format

## API Documentation

FastAPI automatically generates interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Data Privacy

- This API processes sensitive patient information
- No patient data is stored by the API
- All communications should be secured in production environments 