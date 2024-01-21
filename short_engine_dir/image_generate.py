import os
import requests
import json
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from dotenv import load_dotenv
import base64

load_dotenv()

CLARIFAI_API_KEY = os.environ.get('CLARIFAI_TOKEN')

metadata = (('authorization', 'Key ' + CLARIFAI_API_KEY),)




if CLARIFAI_API_KEY is None:
    raise ValueError("Clarifai API key is not set. Set the CLARIFAI_API_KEY environment variable.")


with open('short_engine_dir/response.json', 'r') as script_file:
    script_data = json.load(script_file)

def generate_image_for_video():
    prompt_list = []

    for caption in script_data['captions']:
        if len(caption['prompt']) > 0:
            prompt_list.append(caption['prompt'])


    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)


    USER_ID = 'openai'
    APP_ID = 'dall-e'

    MODEL_ID = 'DALL-E'
    MODEL_VERSION_ID = 'f1756115761940bd820e61383de79351'
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    for i, prompt in enumerate(prompt_list):
        # Make a Clarifai API call
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=prompt
                                # url=TEXT_FILE_URL
                                # raw=file_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0].data.image.base64

        image_filename = f"short_engine_dir/images/generated_image_{i}.jpg"
        with open(image_filename, 'wb') as f:
            f.write(output)



