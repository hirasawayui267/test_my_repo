# publish the layer
import subprocess
import os
import json
# there should only be one layer
layer_name = os.environ.get('LAYER_NAME')
should_publish_layer = os.environ.get('SHOULD_PUBLISH_LAYER')
function_name = os.environ.get('FUNCTION_NAME')

print("env vars ,", layer_name, should_publish_layer, function_name)
def publish_layer_and_update_function_config():
    # simply publish the function
    print("update function code")
    result = subprocess.run([f"aws lambda update-function-code --function-name {function_name} --zip-file fileb://deployment.zip"], stdout=subprocess.STDOUT, shell=True)
    print("update function code result", result)

    if should_publish_layer:
        print("publishing built layer...")
        result = subprocess.run([f"""aws lambda publish-layer-version --layer-name {layer_name} --compatible-architectures x86_64 --zip-file fileb://layer.zip --compatible-runtimes python3.8"""],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        # result = subprocess.run([f"""aws lambda publish-layer-version --layer-name {layer_name} --content S3Bucket=costack-layers,S3Key={function_id}/deployment.zip --compatible-architectures x86_64 --compatible-runtimes python3.8"""],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print(result)
        result = result.stdout.decode('utf-8')
        result_json = json.loads(result)
        print("result is ", result_json)
        layer_version_arn = result_json['LayerVersionArn']
        print("layer version arn is ", layer_version_arn)

        # update the configuration of the function
        print("updating funciton configuration with the new layer")
        # need to know the names of the functions --> function_name, handler
        result = subprocess.run([f"aws lambda update-function-configuration --function-name {function_name} --layers {layer_version_arn}"], stdout=subprocess.PIPE, shell=True)
        result = result.stdout.decode('utf-8')
        print("update funciton configuration result: ",result)




if __name__ == "__main__":
    publish_layer_and_update_function_config()
