# Project Title
Doc Inference

## Description
Doc Inference is a web application designed for processing invoices and converting PDF documents into images. It leverages the Quart framework for asynchronous operations and provides a RESTful API for interacting with its functionalities.

## Technologies Used
- Docker
- uv
- Quart
- Pydantic-ai


## Installation
To set up the project locally, follow these steps:
1. Clone the repository.
2. Navigate to the project directory.
3. Ensure you have Docker installed.
4. Run the following command to start the application:
   ```bash
   docker-compose up
   ```

## Usage
The application runs on port 5001. You can access the API endpoints at `http://localhost:5001`.

## API Endpoints
- **POST /invoice**: Process an invoice.

## Services
- **Invoice Service**: Handles invoice processing and data extraction.
- **PDF to Image Service**: Converts PDF files into image formats.

## Configuration
The application uses environment variables defined in the `.env` file and configuration files located in the `src/configs` directory. Ensure to set the necessary configurations before running the application.


## Run App
uv run hypercorn run_app:app --bind 127.0.0.1:5001