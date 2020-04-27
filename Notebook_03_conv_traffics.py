import tensorflow as tf

'''
50000 * 20 = 10^6 points
unique points = x / ln(x) = 72382 = input dimension = y
needs about y * 3 parameters to learn = 200000 in each layer

dropout
max pooling
global average pooling
1 0 1 0
0 0 0 0 - > 1 1
1 0 0 0 - > 1 0
0 0 0 0
'''

directions = 4
a_lat = 35.614201
b_lat = 35.790657
a_lng = 51.205000
b_lng = 51.493699
rho = .0007
resolution = round((b_lat - a_lat) / rho), round((b_lng - a_lng) / rho)
print(resolution)

model = tf.keras.models.Sequential([
    tf.keras.layers.ConvLSTM2D(filters=directions, kernel_size=(7, 7), input_shape=(1, *resolution, directions), padding='same', return_sequences=True),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.ConvLSTM2D(filters=directions * 16, kernel_size=(3, 3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Conv2D(filters=directions * 128, kernel_size=(3, 3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Conv2D(filters=directions, kernel_size=(3, 3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.LeakyReLU(),
])

model.summary()
# print(model(tf.random.normal((1, 1, resolution[0], resolution[1], 4))))
model.compile(loss=tf.keras.losses.mse, optimizer=tf.keras.optimizers.Adam(1e-4))
model.fit(tf.random.normal((1, 1, resolution[0], resolution[1], 4)), tf.random.normal((1, resolution[0], resolution[1], 4)))
