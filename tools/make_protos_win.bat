@echo off
echo "Making Protos..."
"C:\Users\Vasilis\Downloads\protoc-3.11.4-win64\bin\protoc.exe" ../tensorflow_libs/object_detection/protos/*.proto --python_out=.
echo "Finished"
