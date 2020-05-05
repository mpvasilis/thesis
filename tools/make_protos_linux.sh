echo "Making Protos..."
protoc ../object_detection/object_detection/protos/*.proto --python_out=.
echo "Finished"
