import os
import tensorflow as tf
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
import matplotlib.pyplot as plt

# Qt 플랫폼 플러그인 문제 해결을 위한 백엔드 설정
plt.switch_backend("Agg")

# 데이터셋 경로
dataset_path = "c:/Users/KNUT/train_medi"

# 데이터 증강 및 전처리
datagen = ImageDataGenerator(
    rescale=1.0 / 255, 
    rotation_range=40,  # 이미지 회전 범위
    width_shift_range=0.2,  # 이미지 수평 이동 범위
    height_shift_range=0.2,  # 이미지 수직 이동 범위
    shear_range=0.2,  # 이미지 전단 변환 범위
    zoom_range=0.2,  # 이미지 확대 범위
    horizontal_flip=True,  # 이미지 수평 반전
    fill_mode="nearest",  # 변환 중 생기는 빈 공간을 채우는 방식
    validation_split=0.2
)

train_datagen = datagen.flow_from_directory(
    dataset_path,
    target_size=(244, 244),
    batch_size=32,
    class_mode="binary",  # 이진 분류를 위해 'binary'로 변경
    subset="training",
)

validation_datagen = datagen.flow_from_directory(
    dataset_path,
    target_size=(244, 244),
    batch_size=32,
    class_mode="binary",  # 이진 분류를 위해 'binary'로 변경
    subset="validation",
)

# InceptionV3 모델 불러오기
base_model = InceptionV3(weights="imagenet", include_top=False)

# 모델 구조 쌓기
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation="relu")(x)
x = BatchNormalization()(x)  # BatchNormalization 추가
x = Dropout(0.5)(x)  # Dropout 추가
predictions = Dense(1, activation="sigmoid")(x)  # 이진 분류를 위해 1개의 뉴런과 sigmoid 활성화 함수 사용

# 최종 모델 정의
model = Model(inputs=base_model.input, outputs=predictions)

# 모델 컴파일
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 모델 학습
history = model.fit(
    train_datagen,
    epochs=30,
    validation_data=validation_datagen,
)

# 그래프 이미지를 저장할 폴더 경로
save_google_dir = "c:/Users/KNUT/images_gr"

# 학습 및 검증 정확도와 손실 값을 Python 리스트로 변환
def save_plot(history, save_google_dir):
    acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    # 디렉터리가 존재하지 않으면 생성합니다.
    if not os.path.exists(save_google_dir):
        os.makedirs(save_google_dir)

    # 학습 및 검증 정확도와 손실 그래프 그리기
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.legend(loc="lower right")
    plt.title("Training and Validation Accuracy")
    plt.savefig(os.path.join(save_google_dir, 'Validation_Accuracy3.png'))
    plt.close()

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss")
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.legend(loc="upper right")
    plt.title("Training and Validation Loss")
    plt.savefig(os.path.join(save_google_dir, 'Validation_Loss3.png'))
    plt.close()

    # 최종 학습 및 검증 정확도 출력
    print(f"Final Training Accuracy: {acc[-1] * 100:.2f}%")
    print(f"Final Validation Accuracy: {val_acc[-1] * 100:.2f}%")

# 그래프 이미지를 저장합니다
save_plot(history, save_google_dir)
