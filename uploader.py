import boto3
import base64
import json
import time


## create the s3 client 
s3 = boto3.client("s3")

bucket_name = "cyclocore1" ## bucket name should come from API secret manager 

def lambda_handler(event, context): 
    ## This code expects the client to send data in the form of JSON
    ## the structure of the request is expected in this format: 

    ## event contains all the important data coming from the client
    user_id = event.get("user_id")
    image_base64 = event.get("profile_image")
    content_type = event.get("profile_image_content_type")


    allowed_types = ["image/png", "image/jpg", "image/jpeg", "image/tiff"]


    image_decoded = None

    ## decode the image base64
    if image_base64: 
        image_decoded = base64.b64decode(image_base64)
    else: 
        return {
            "message": "No image was uploaded", 
            "code": "no-image-error",
            "data": None
        }
    
    if not content_type:
        return {
            "message": "Profile image content type is required",
            "code": "no-content-type-image-error",
            "data": None
        }
    

    if content_type not in allowed_types: 
        return {
            "message": "Profile image type not allowed",
            "code": "invalid-image-type",
            "data": None
        }
    
    image_size = getImageSize(image_decoded)

    if image_size > 5:
        return {
            "message": "Image too large",
            "code": "invalid-image-size",
            "data": None
        }
    

    timestamp = int(time.time())

    ## create where the image should be uploaded to 
    upload_location = f"profiles/{user_id}/{timestamp}"

    ## store the image 
    upload_feedback = s3.put_object(Bucket=bucket_name, Key=upload_location, Body=image_decoded, ContentType=content_type)

    if upload_feedback["ResponseMetadata"]["HTTPStatusCode"] == 200:

        ## construct the url and send back
        image_url = f"http://{bucket_name}.s3.amazonaws.com/{upload_location}"

        return {
            "message": "Image uploaded successfully", 
            "code": "success",
            "data": {
                "image_url": image_url
            }
        }
    
    else: 
        return {
            "message": "An error ocurred while attempting to upload",
            "code": "error",
            "data": None
        }




def getImageSize(image_byte):
    image_byte_length = len(image_byte)

    image_size_mb = int(image_byte_length / (1024 * 1024))

    return image_size_mb


