# Hair Classifier Lambda

This project contains a serverless function to classify hairstyles using an ONNX model.

## Files

- `lambda_function.py`: The main Lambda function code.
- `solve_homework_v2.py`: Script to test the model locally.
- `Dockerfile`: Docker configuration for deployment.
- `requirements.txt`: Python dependencies.
- `hair_classifier_empty.onnx`: The machine learning model.

## Deployment

To build and run the Docker container:

```bash
docker build -t hair-classifier .
docker run -p 8080:8080 hair-classifier
```

## Usage

The Lambda function expects a JSON event with a `url` field pointing to an image.

```json
{
  "url": "https://example.com/image.jpg"
}
```
