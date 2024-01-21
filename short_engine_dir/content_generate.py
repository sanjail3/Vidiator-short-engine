import os
import json
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from dotenv import load_dotenv

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
load_dotenv()

PAT = os.environ.get('CLARIFAI_TOKEN')

metadata = (('authorization', 'Key ' + PAT),)






def get_response(topic):

    USER_ID = 'openai'
    APP_ID = 'chat-completion'

    MODEL_ID = 'GPT-4'
    MODEL_VERSION_ID = os.environ.get('TEXT_MODEL_ID')
    RAW_TEXT = f'''Act as a video creator you are a video script witer and flim maker I will give you the topic write a video script  for the duration of 1 minute and {topic}  and you should also generate script for the video with 
                duration and also timstamps for each script your response should be like this keywordsearch for video in google and also give me the prompt for image to generate from DALL E and text this example note this in text give me only script of the video text with timestamps don't give other words like intro music
                it should give only JSON file no other words like here is yoour response like that only JSON response
                finally format in json file as per give prompt example json:

                captions:
                     start:
                     end:
                     text:
                     keyword:
                     prompt:


                '''

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT

                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    output = post_model_outputs_response.outputs[0]

    print("Completion:\n")
    print(output.data.text.raw)




    response_data = json.loads(output.data.text.raw)


    with open('short_engine_dir/response.json', 'w') as json_file:
        json.dump(response_data, json_file, indent=4)

    print(output)



# get_response("Nature")
