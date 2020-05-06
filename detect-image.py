import sys
from absl import app, flags
from absl.flags import FLAGS
import object_detection.retinaNet as rn
import object_detection.yolo as yl

import os

# Program arguments
flags.DEFINE_string('algorithm', 'YOLOv3', 'Object Detection Algorithm')
flags.DEFINE_string('model', '', 'Object Detection Model')
flags.DEFINE_string('image', '/data/images/dog.jpg', 'Input image')
flags.DEFINE_string('output', './detections/', 'Path to output folder')
flags.DEFINE_list('images', '/data/images/dog.jpg', 'list with paths to input images')


flags.DEFINE_string('classes', './data/labels/coco.names', 'path to classes file')
flags.DEFINE_string('weights', './weights/yolov3.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('tfrecord', None, 'tfrecord instead of image')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')


def main(_argv):

    # Check if input image exists
    if not os.path.isfile(FLAGS.image):
        print("Cannot find image.")
        sys.exit()

    # Check if model exists
    if not os.path.isfile(FLAGS.model):
        print("Cannot find model.")
        sys.exit()

     # Object Detection for image
    if FLAGS.algorithm == "retinanet":
        print(FLAGS.algorithm)
        rn.retinanet_image(FLAGS.image,FLAGS.model,FLAGS.output)
    elif FLAGS.algorithm == "YOLOv3":
        print(FLAGS.algorithm)
        yl.yoloImage(FLAGS.image,FLAGS.model,FLAGS.output)
    elif FLAGS.algorithm == "tiny-YOLOv3":
        print(FLAGS.algorithm)
        yl.yoloImage(FLAGS.image,FLAGS.model,FLAGS.output)
    elif FLAGS.algorithm == "ssd":
        print(FLAGS.algorithm)
    elif FLAGS.algorithm == "faster-rcnn":
        print(FLAGS.algorithm)
    else:
        print("Select one of the following algorithms: retinanet, faster-rcnn, ssd, YOLOv3 and tiny-YOLOv3.")


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass



