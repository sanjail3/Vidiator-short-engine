from elevenlabs import generate,save
import json
from dotenv import load_dotenv
import os
load_dotenv()
PAT = os.environ.get('CLARIFAI_TOKEN')
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2






USER_ID = 'openai'
APP_ID = 'tts'

MODEL_ID = 'openai-tts-1'
MODEL_VERSION_ID = 'fff6ce1fd487457da95b79241ac6f02d'

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

def generate_voice():
    with open('short_engine_dir/response.json', 'r') as script_file:
        script_data = json.load(script_file)

    text = ""

    for caption in script_data['captions']:
        text += caption['text'] + " "



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
                            raw=text
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
    output = post_model_outputs_response.outputs[0]






    save(output.data.audio.base64, filename="output.wav")
