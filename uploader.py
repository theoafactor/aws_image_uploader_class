import boto3 
import base64

s3 = boto3.client("s3")

def lambda_handler(event, context):
    
    ## Get the data sent to the lambda function
    ## the needed data from the client are: 
    ## 1. image to be uploaded 
    ## 2. the user id of the image to be uploaded
    ## 3. type of image to tbe uploaded 

    user_id = event.get("user_id")
    imagebase64 = event.get("image")

    original_image = base64.b64decode(imagebase64)
    


    s3.put_object(Bucket="cyclocore2", Key="images", Body=original_image)


    return {
        "message": "Image uploaded successfully"
    }


