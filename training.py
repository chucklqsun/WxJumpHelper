import os
import numpy as np
# from tensorflow import set_random_seed
# set_random_seed(2)
import tensorflow as tf
import cv2
from tensorflow.python.saved_model import signature_constants
_DEFAULT_SERVING_KEY = signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY


WIDTH = 56*2
HEIGHT= 56*2


def file_extension(path):
    return os.path.splitext(path)[1]


def list_files(path, ext='', depth=999):
    files_list = []
    path_depth = path.count(os.sep)
    for subdir, dirs, files in os.walk(path, topdown=True):
        if subdir.count(os.sep) - path_depth < depth:
            for f in files:
                if ext == '':
                    files_list.append(os.path.join(subdir, f))
                elif file_extension(f) == ext:
                    files_list.append(os.path.join(subdir, f))
    return files_list


def serving_input_receiver_fn():
    inputs = {'x': tf.placeholder(tf.float32, [HEIGHT*WIDTH])}
    return tf.estimator.export.ServingInputReceiver(inputs, inputs)


def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""
    # Input Layer
    # Reshape X to 4-D tensor: [batch_size, width, height, channels]
    # images are 28x28 pixels, and have one color channel
    input_layer = tf.reshape(features["x"], [-1, HEIGHT, WIDTH, 1])

    # Convolutional Layer #1
    # Computes 32 features using a 5x5 filter with ReLU activation.
    # Padding is added to preserve width and height.
    # Input Tensor Shape: [batch_size, 28, 28, 1]
    # Output Tensor Shape: [batch_size, 28, 28, 32]
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #1
    # First max pooling layer with a 2x2 filter and stride of 2
    # Input Tensor Shape: [batch_size, 28, 28, 32]
    # Output Tensor Shape: [batch_size, 14, 14, 32]
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Convolutional Layer #2
    # Computes 64 features using a 5x5 filter.
    # Padding is added to preserve width and height.
    # Input Tensor Shape: [batch_size, 14, 14, 32]
    # Output Tensor Shape: [batch_size, 14, 14, 64]
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #2
    # Second max pooling layer with a 2x2 filter and stride of 2
    # Input Tensor Shape: [batch_size, 14, 14, 64]
    # Output Tensor Shape: [batch_size, 7, 7, 64]
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Flatten tensor into a batch of vectors
    # Input Tensor Shape: [batch_size, 7, 7, 64]
    # Output Tensor Shape: [batch_size, 7 * 7 * 64]
    pool2_flat = tf.reshape(pool2, [-1, int(HEIGHT/4) * int(HEIGHT/4) * 64])

    # Dense Layer
    # Densely connected layer with 1024 neurons
    # Input Tensor Shape: [batch_size, 7 * 7 * 64]
    # Output Tensor Shape: [batch_size, 1024]
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)

    # Add dropout operation; 0.6 probability that element will be kept
    dropout = tf.layers.dropout(
        inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits layer
    # Input Tensor Shape: [batch_size, 1024]
    # Output Tensor Shape: [batch_size, 10]
    logits = tf.layers.dense(inputs=dropout, units=1100)
    # logits = tf.layers.dense(inputs=dense, units=1100)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }
    export_output = {_DEFAULT_SERVING_KEY: tf.estimator.export.PredictOutput(predictions)}
    if mode == tf.estimator.ModeKeys.PREDICT:
      return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions,export_outputs=export_output)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
      train_op = optimizer.minimize(
          loss=loss,
          global_step=tf.train.get_global_step())
      return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def main(unused_argv):

    data_set = list_files("/Users/bartowski/tmp/data/wxjump/train", ".png")
    train_data = []
    train_labels = []
    eval_data = []
    eval_labels = []

    print(data_set)
    for i in range(0, len(data_set)):
        delay = os.path.splitext(os.path.basename(data_set[i]))[0].split("_")[1]
        # reader = tf.WholeFileReader()
        # filename_queue = tf.train.string_input_producer(["./screenshot.png"])
        # key, value = reader.read(filename_queue)
        # my_img = tf.image.decode_png(value, channels=4)  # use png or jpg decoder based on your files.
        # my_img = tf.slice(my_img, [0, 0, 0], [-1, -1, 3])
        # my_img.set_shape([1920, 1080, 3])
        # resized_image = tf.image.resize_images(my_img, [28, 28])
        # resized_image = tf.image.rgb_to_grayscale(resized_image, name=None)
        # resized_image = tf.reshape(resized_image, [-1])

        image = cv2.imread(data_set[i])
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(grey_image, (HEIGHT, WIDTH))
        for m in range(0, len(resized_image)):
            for n in range(0, len(resized_image[m])):
                resized_image[m][n] = resized_image[m][n]/255.0

        resized_image = np.array(resized_image).flatten()

        train_data.append(resized_image)
        train_labels.append(delay)
        eval_data.append(resized_image)
        eval_labels.append(delay)

    train_data = np.array(train_data, dtype=np.float32)
    train_labels = np.asarray(train_labels, dtype=np.int32)
    eval_data = np.array(eval_data, dtype=np.float32)
    eval_labels = np.asarray(eval_labels, dtype=np.int32)

    # Load training and eval data
    # mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    # train_data = mnist.train.images  # Returns np.array
    # train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    # eval_data = mnist.test.images  # Returns np.array
    # eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    print(train_data)
    print(train_labels.shape)

    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="./model")

    # Set up logging for predictions
    # Log the values in the "Softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=200,
        hooks=[logging_hook])

    # Evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

    full_model_dir = mnist_classifier.export_savedmodel(export_dir_base="./model",
                                                        serving_input_receiver_fn=serving_input_receiver_fn)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
