#!/bin/bash

# get the functions and just build the layers
# build the handlers for the functions
# deploy my lambda with the handlers
# zip the entire folder and deploy to lambda?
# build the layers...
if [ -f "requirements.txt" ]; then
    echo "detect requirements.txt."
    echo "automatically build layer"
    python3.8 -m venv entropy-env
    echo "done building virtual env..."
    echo "activate virtual env"
    . entropy-env/bin/activate
    python3.8 -m pip install -r requirements.txt
    deactivate
    mkdir python
    cd python
    mkdir lib
    cd ..
    cp -r entropy-env/lib/python3.8 python/lib/
    ls
    zip -r layer.zip python &>/dev/null
    ls
    echo "zipped env"
    # clean up the folder end
    echo "clean up the folder, remove entropy-env and python zip folder"
    rm -r entropy-env
    rm -r python
    echo "publish layer version..."
    # should actually use the project resource id to construct the layers
    # should link the layer with the function
    export SHOULD_PUBLISH_LAYER=1
fi

zip -r deployment.zip src &>/dev/null
# deploy the deployment file and upload to aws
# the following should be done by python scripts for convenience

# aws lambda publish-layer-version --layer-name $LAYER_NAME --compatible-architectures x86_64 --zip-file fileb://layer.zip --compatible-runtimes python3.8
# aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://deployment.zip

# use python
python3.8 deploy_helper.py
echo "deploy success"
