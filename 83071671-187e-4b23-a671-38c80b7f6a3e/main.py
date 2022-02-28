# create your main function here
# run the necessary operaitons and return
import json
def entropy_main(event, context):
    # the input event is in a json string
    if type(event)==str:
        event = json.loads(event)
    return {"response": "this is my entropy function" }
