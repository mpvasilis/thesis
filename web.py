import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from tensorflow_libs.yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from tensorflow_libs.yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from tensorflow_libs.yolov3_tf2.utils import draw_outputs
from flask import Flask, request, Response, jsonify, send_from_directory, abort
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

import tensorflow_libs.tensorflowObjectDetection
import os
import matplotlib


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

classes_path = 'data/labels/coco.names'
weights_path = 'weights/yolov3.tf'
tiny = False
size = 416
output_path = './detections/'
num_classes = 80

if tiny:
    yolo = YoloV3Tiny(classes=num_classes)
else:
    yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path).expect_partial()
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')

app = Flask(__name__)


@app.route('/detectionsYolo', methods=['POST'])
def get_detections():
    raw_images = []
    images = request.files.getlist("images")
    image_names = []
    for image in images:
        image_name = image.filename
        image_names.append(image_name)
        image.save(os.path.join(os.getcwd(), image_name))
        img_raw = tf.image.decode_image(
            open(image_name, 'rb').read(), channels=3)
        raw_images.append(img_raw)

    num = 0

    response = []

    for j in range(len(raw_images)):
        responses = []
        raw_img = raw_images[j]
        num += 1
        img = tf.expand_dims(raw_img, 0)
        img = transform_images(img, size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo(img)
        t2 = time.time()
        print('time: {}'.format(t2 - t1))

        print('detections:')
        for i in range(nums[0]):
            print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                        np.array(scores[0][i]),
                                        np.array(boxes[0][i])))
            responses.append({
                "class": class_names[int(classes[0][i])],
                "confidence": float("{0:.2f}".format(np.array(scores[0][i]) * 100))
            })
        response.append({
            "image": image_names[j],
            "detections": responses
        })
        img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2BGR)
        img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        cv2.imwrite(output_path + 'detection' + str(num) + '.jpg', img)
        print('output saved to: {}'.format(output_path + 'detection' + str(num) + '.jpg'))

    for name in image_names:
        os.remove(name)
    try:
        return jsonify({"response": response}), 200
    except FileNotFoundError:
        abort(404)


@app.route('/imageYolo', methods=['POST'])
def get_image():
    image = request.files["images"]
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))
    img_raw = tf.image.decode_image(
        open(image_name, 'rb').read(), channels=3)
    img = tf.expand_dims(img_raw, 0)
    img = transform_images(img, size)

    t1 = time.time()
    boxes, scores, classes, nums = yolo(img)
    t2 = time.time()
    print('time: {}'.format(t2 - t1))

    print('detections:')
    for i in range(nums[0]):
        print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                    np.array(scores[0][i]),
                                    np.array(boxes[0][i])))
    img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
    img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
    cv2.imwrite(output_path + 'detection.jpg', img)
    _, img_encoded = cv2.imencode('.png', img)
    response = img_encoded.tostring()

    os.remove(image_name)

    try:
        return Response(response=response, status=200, mimetype='image/png')
    except FileNotFoundError:
        abort(404)

@app.route('/imageSSD', methods=['POST'])
def get_imageSSD():
    image = request.files["images"]
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))

    t1 = time.time()
    model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
    detection_model = tensorflow_libs.tensorflowObjectDetection.load_model(model_name)

    print(detection_model.inputs)

    image_np = np.array(tensorflow_libs.tensorflowObjectDetection.Image.open(os.path.join(os.getcwd(), image_name)))
    output_dict = tensorflow_libs.tensorflowObjectDetection.run_inference_for_single_image(detection_model, image_np)
    tensorflow_libs.tensorflowObjectDetection.vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        tensorflow_libs.tensorflowObjectDetection.category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=8)
    t2 = time.time()
    print('time: {}'.format(t2 - t1))
    cv2.imwrite(output_path + 'detection.jpg', image_np)
    print('output saved to: {}'.format(output_path + 'detection.jpg'))
    _, img_encoded = cv2.imencode('.png', image_np)
    response = img_encoded.tostring()
    os.remove(image_name)
    try:
        return Response(response=response, status=200, mimetype='image/png')
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)