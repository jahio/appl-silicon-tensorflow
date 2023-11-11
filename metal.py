#
# See the accompanying readme.md file for more information.
#
# The objective of this script is to, after having set up your python/tensorflow
# environment, see if it picks up your Apple Metal GPU. Requires an Apple
# Silicon processor. May or may not be useful for detecting GPU usage on
# non-Apple devices, I have no idea since as I write this I'm -just- getting
# started on my Mac Studio.
#
# This script was shamelessly copied straight from Apple's documentation at:
#   https://developer.apple.com/metal/tensorflow-plugin/
#
# Be advised that Apple has had a "complex" history with the quality of their
# developer documentation (in my personal opinion), so if that 404's for you
# when you see it from the future, hit up the wayback machine if it hasn't been
# decimated by tyrannical bastards yet.
#
# Relevant:
#  - https://pypi.org/project/tensorflow-metal/
#  - https://pypi.org/project/tensorflow/
#  - https://www.tensorflow.org/install
#

import tensorflow as tf

cifar = tf.keras.datasets.cifar100
(x_train, y_train), (x_test, y_test) = cifar.load_data()
model = tf.keras.applications.ResNet50(
    include_top=True,
    weights=None,
    input_shape=(32, 32, 3),
    classes=100,)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5, batch_size=64)
