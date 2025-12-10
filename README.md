# Hair Classifier

**Repository:** https://github.com/DaniloBlancoMotta/hair_classifier

## Table of Contents
- [Problem Description](#problem-description)
- [Objectives](#objectives)
- [Files](#files)
- [Deployment](#deployment)
- [Usage](#usage)

## Problem Description
This project aims to classify hairstyles (Straight vs Curly) using deep learning models. The solution is deployed as a serverless function.

## Objectives
1. Data Preparation and Cleaning
2. Feature Engineering
3. Model Training
4. Model Evaluation
5. Deployment

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
