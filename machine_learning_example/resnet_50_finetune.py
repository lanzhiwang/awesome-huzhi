# -*- coding:utf-8 -*-
import time
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint
from keras.applications.resnet50 import ResNet50

# dimensions of our images.
img_width, img_height = 224, 256

train_data_dir = "/home/root01/shuwo/ResNet-on-shuwo/data/keras/train_cate"
validation_data_dir = "/home/root01/shuwo/ResNet-on-shuwo/data/keras/test_cate"
# mapping file dir to category
classes = ["0", "1", "2", "3", "4", "5"]
# the number of training images
nb_train_samples = 165560  # 162086#161725 #159039
# the number of validation images
nb_validation_samples = 55801  # 55397#55286
# training epoch
nb_epoch = 40
batch_size = 32
# fine-tune with ResNet50
base_model = ResNet50(weights="imagenet", include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
predictions = Dense(len(classes), activation="softmax")(x)

# this is the model we will train
model = Model(input=base_model.input, output=predictions)

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
# for i, layer in enumerate(base_model.layers):
#     print(i, layer.name)

# freeze early layer without training
for layer in model.layers[:36]:
    layer.trainable = False
for layer in model.layers[36:]:
    layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
model.compile(
    optimizer=SGD(lr=0.001, momentum=0.9, decay=1e-6),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# prepare data augmentation configuration
train_datagen = ImageDataGenerator(
    # featurewise_center=True,
    rotation_range=0.0,  # 整数，数据提升时图片随机转动的角度
    width_shift_range=0.0,  # 浮点数，图片宽度的某个比例，数据提升时图片水平偏移的幅度
    height_shift_range=0.0,  # 浮点数，图片高度的某个比例，数据提升时图片竖直偏移的幅度
    shear_range=0.2,  # 浮点数，剪切强度（逆时针方向的剪切变换角度）
    zoom_range=0.2,  # 浮点数，随机缩放的幅度
    cval=0.0,  #
    horizontal_flip=True,  # 水平翻转
    rescale=1.0 / 255,  # 对图像按照指定的尺度因子, 进行放大或缩小
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

# generate image from dir
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    classes=classes,
    target_size=(img_height, img_width),
    batch_size=batch_size,
)

# generate image from dir
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    classes=classes,
    target_size=(img_height, img_width),
    batch_size=batch_size,
)

checkpointer = ModelCheckpoint(
    filepath="/home/root01/shuwo/ResNet-on-shuwo/output/012345_weight180314.hdf5",
    verbose=1,
    save_best_only=True,
)

# fine-tune the model
start = time.time()
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples / batch_size,
    epochs=nb_epoch,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples / batch_size,
    callbacks=[checkpointer],
)

print("Done in %.2f s." % (time.time() - start))
