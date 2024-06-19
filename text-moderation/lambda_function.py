import json
import boto3

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        text = body['text']
        
        comprehend = boto3.client('comprehend')
        
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        
        return {
            'statusCode': 200,
            'body': json.dumps(response["SentimentScore"])
        }
    
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing text in request body'})
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
