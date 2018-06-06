#
#Created By 조성재
#
#retrain.py에서 만들어진 모델로 얼굴 이미지를 넣었을 때 누구와 가장 가까운지 예측,정확도와 함께 결과 추출
#
#

import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import numpy as np

tf.app.flags.DEFINE_string("output_graph", "/home/cho/PycharmProjects/CNN_face/workspace/famous_people_graph.pb", "location")
tf.app.flags.DEFINE_string("output_labels", "/home/cho/PycharmProjects/CNN_face/workspace/people_labels.txt", "datafile for studying")
tf.app.flags.DEFINE_boolean("show_image", True, "show image after predict image")
FLAGS = tf.app.flags.FLAGS

def main(_):
    labels = [line.rstrip() for line in tf.gfile.GFile(FLAGS.output_labels)]

    with tf.gfile.FastGFile(FLAGS.output_graph, 'rb') as fp:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(fp.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        logits = sess.graph.get_tensor_by_name('final_result:0')
        image = tf.gfile.FastGFile(sys.argv[1], 'rb').read()
        prediction = sess.run(logits, {'DecodeJpeg/contents:0': image})

    print('=== Predict Result ===')
    '''for i in range(len(labels)):
        name = labels[i]
        score = prediction[0][i]
        print('%s (%.2f%%)' % (name, score *100))'''

    top_result = int(np.argmax(prediction[0]))
    name = labels[top_result]
    score = prediction[0][top_result]
    print('%s (%.2f%%)' % (name, score *100))

    if FLAGS.show_image:
        img = mpimg.imread(sys.argv[1])
        plt.imshow(img)
        plt.show()

if __name__ == "__main__":
    tf.app.run()

