import os
import tensorflow as tf
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data

class_list = [ '0',
               '1',
               '2',
               '3',
               '4',
               '5',
               '6',
               '7',
               '8',
               '9']

''' Model parameters '''
# It determines how quickly or how slowly you want to update the parameters.
# if the learning rate is too large, loss function will not converge.
learning_rate = 1e-3

# the number of training examples in one computation.
# the higher the batch size, the more memory space you'll need.
batch_size = 1000

max_iteration = 1000

display_step = 100
save_freq = 1000
savedir = 'savedir/'


''' Placeholder setup '''
images = tf.placeholder(tf.float32, [None, 784])
labels = tf.placeholder(tf.float32, [None, 10])



''' Weightss setup '''
weight = tf.Variable(tf.random_normal([784, 10], stddev=0.01), name='weight')
bias = tf.Variable(tf.random_normal([10], stddev=0.01), name='bias')


''' Model layer setup '''

logits = tf.add(tf.matmul(images, weight), bias)
output = tf.argmax(logits, axis=1)



''' Loss & optimizer, accuracy '''
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits))

accuracy = tf.reduce_mean(tf.cast(tf.equal(output, tf.argmax(labels, axis=1)), tf.float32))

optimize = tf.train.AdamOptimizer(learning_rate).minimize(loss)



''' Initializer & saver setup '''
init = tf.global_variables_initializer()
saver = tf.train.Saver()
if not os.path.exists(savedir):
    os.makedirs(savedir)



''' Import dataset '''
mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)



''' Create tensorflow session '''
sess = tf.Session()



''' Initialize weights & restore saved weights '''
sess.run(init)
try:
    saver.restore(sess, savedir+'model.ckpt')
except:
    pass



''' Train '''
batch_size = np.minimum(batch_size, mnist.train.images.shape[0]) # if batch_size>trainset, reduce batch_size
print('\n Training start')
for epoch in range(max_iteration):

    # random images & labels from train dataset
    batch_input, batch_labels = mnist.train.next_batch(batch_size)

    # compute loss & update weights
    _, training_loss, training_accuracy = sess.run([optimize, loss, accuracy], feed_dict={images:batch_input, labels:batch_labels})
    
    # print accuracy & save model
    if (epoch + 1) % display_step is 0:
        print(' epoch:', '%07d' % (epoch + 1), \
            '   loss =', '{:.6f}'.format(training_loss), \
            '   training accuracy =', '{:.4f}'.format(training_accuracy))
    if (epoch + 1) % save_freq is 0:
        save_path = saver.save(sess, savedir+'model.ckpt')
        print(" Model saved in file: %s" % save_path)

print(' Training done.')

save_path = saver.save(sess, savedir+'model.ckpt')
print(" Model saved in file: %s" % save_path)



''' Test '''
test_batch_size = np.minimum(batch_size, mnist.test.images.shape[0]) # if batch_size>testset, reduce test_batch_size
n_test_batch = int(mnist.test.images.shape[0] / test_batch_size)
test_accuracy = 0
for test_batch in range(n_test_batch):
    test_images = mnist.test.images[test_batch_size*test_batch:test_batch_size*(test_batch+1)]
    test_labels = mnist.test.labels[test_batch_size*test_batch:test_batch_size*(test_batch+1)]
    test_accuracy += sess.run(accuracy, feed_dict={images : test_images, labels : test_labels})
print('\n Test accuracy =', '{:.4f}'.format(test_accuracy / n_test_batch))
