import json
import boto3
import requests

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        image_url = body['image_url']
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing image_url in request body'})
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in request body'})
        }
    
    rekognition_client = boto3.client('rekognition')
    
    try:
        image_response = requests.get(image_url)
        image_data = image_response.content
        
        moderation_response = rekognition_client.detect_moderation_labels(
            Image={'Bytes': image_data},
            MinConfidence=75
        )
        
        moderation_labels = moderation_response['ModerationLabels']
        
        formatted_response = {}
        for label in moderation_labels:
            name = label['Name']
            flag_level = label['TaxonomyLevel']
            confidence = label['Confidence']
            formatted_response[name] = {
                'flag_level': flag_level,
                'confidence': confidence
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps(formatted_response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
