#!/bin/bash

# get the functions and just build the layers
# build the handlers for the functions
# deploy my lambda with the handlers
# zip the entire folder and deploy to lambda?
zip -r deployment.zip src &>/dev/null
# deploy the deployment file and upload to aws
aws lambda update-function-code --function-name costack-auto-test --zip-file fileb://deployment.zip
echo "deploy success"
