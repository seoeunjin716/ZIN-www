import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np


class MnistTest:
    def __init__(self):
        self.class_names = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

    def create_model(self) -> []:
        # Fashion-MNIST 데이터를 다운로드하고 전처리합니다.
        # transforms.ToTensor()는 PIL 이미지를 텐서로 변환하고 0-255 값을 0-1로 정규화합니다.
        transform = transforms.Compose([transforms.ToTensor()])

        # 학습 데이터셋 로드
        train_dataset = datasets.FashionMNIST(
            root="./data", train=True, download=True, transform=transform
        )

        # 테스트 데이터셋 로드
        test_dataset = datasets.FashionMNIST(
            root="./data", train=False, download=True, transform=transform
        )

        # 데이터를 numpy 배열로 변환 (시각화용)
        train_loader_all = DataLoader(train_dataset, batch_size=len(train_dataset))
        test_loader_all = DataLoader(test_dataset, batch_size=len(test_dataset))

        train_images, train_labels = next(iter(train_loader_all))
        test_images, test_labels = next(iter(test_loader_all))

        # 텐서를 numpy로 변환 (시각화용)
        train_images_np = train_images.numpy()
        train_labels_np = train_labels.numpy()
        test_images_np = test_images.numpy()
        test_labels_np = test_labels.numpy()

        # print('행: %d, 열: %d' % (train_images_np.shape[0], train_images_np.shape[1]))
        # print('행: %d, 열: %d' % (test_images_np.shape[0], test_images_np.shape[1]))

        # plt.figure()
        # plt.imshow(train_images_np[3].squeeze(), cmap='gray')
        # plt.colorbar()
        # plt.grid(False)
        # plt.show()

        # 이미지는 이미 0-1로 정규화되어 있음 (ToTensor가 처리)

        # 25개 이미지 시각화
        plt.figure(figsize=(10, 10))
        for i in range(25):
            plt.subplot(5, 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(train_images_np[i].squeeze(), cmap=plt.cm.binary)
            plt.xlabel(self.class_names[train_labels_np[i]])
        # plt.show()

        # 신경망 모델 구성
        # Flatten(input_shape=(28, 28)) -> Dense(128, activation='relu') -> Dense(10, activation='softmax')
        """
        relu ( Rectified Linear Unit 정류한 선형 유닛)
        미분 가능한 0과 1사이의 값을 갖도록 하는 알고리즘
        softmax
        nn (neural network )의 최상위층에서 사용되며 classification 을 위한 function
        결과를 확률값으로 해석하기 위한 알고리즘
        """
        model = FashionNet()

        # 손실 함수와 옵티마이저 정의
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # 데이터 로더 생성
        batch_size = 32
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        # learning
        num_epochs = 5
        for epoch in range(num_epochs):
            model.train()
            running_loss = 0.0
            for images, labels in train_loader:
                # 옵티마이저의 그래디언트 초기화
                optimizer.zero_grad()

                # 순전파: 모델에 입력을 전달하여 예측값 계산
                outputs = model(images)

                # 손실 계산
                loss = criterion(outputs, labels)

                # 역전파: 그래디언트 계산
                loss.backward()

                # 가중치 업데이트
                optimizer.step()

                running_loss += loss.item()

            print(
                f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}"
            )

        # test
        model.eval()
        correct = 0
        total = 0
        test_loss = 0.0

        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        test_acc = correct / total
        print(f"\n테스트 정확도: {test_acc:.4f}")

        # prediction
        model.eval()
        all_predictions = []
        with torch.no_grad():
            for images, _ in test_loader:
                outputs = model(images)
                # softmax 적용하여 확률값으로 변환
                probs = torch.nn.functional.softmax(outputs, dim=1)
                all_predictions.append(probs)

        predictions = torch.cat(all_predictions, dim=0).numpy()
        print(predictions[3])

        # 10개 클래스에 대한 예측을 그래프화
        arr = [predictions, test_labels_np, test_images_np]
        return arr

    def plot_image(self, i, predictions_array, true_label, img) -> []:
        print(" === plot_image 로 진입 ===")
        predictions_array, true_label, img = (
            predictions_array[i],
            true_label[i],
            img[i],
        )
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(img.squeeze(), cmap=plt.cm.binary)
        # plt.show()
        predicted_label = np.argmax(predictions_array)
        if predicted_label == true_label:
            color = "blue"
        else:
            color = "red"

        plt.xlabel(
            "{} {:2.0f}% ({})".format(
                self.class_names[predicted_label],
                100 * np.max(predictions_array),
                self.class_names[true_label],
            ),
            color=color,
        )

    @staticmethod
    def plot_value_array(i, predictions_array, true_label):
        predictions_array, true_label = predictions_array[i], true_label[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        thisplot = plt.bar(range(10), predictions_array, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(predictions_array)

        thisplot[predicted_label].set_color("red")
        thisplot[true_label].set_color("blue")


# 신경망 모델 정의
class FashionNet(nn.Module):
    def __init__(self):
        super(FashionNet, self).__init__()
        # Flatten: 28x28 이미지를 784로 펼침
        # Dense(128, activation='relu'): 784 -> 128
        self.fc1 = nn.Linear(28 * 28, 128)
        # Dense(10, activation='softmax'): 128 -> 10
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # 입력 이미지를 1차원 벡터로 변환 (배치 크기, 784)
        x = x.view(-1, 28 * 28)
        # 첫 번째 레이어: ReLU 활성화 함수 적용
        x = torch.relu(self.fc1(x))
        # 두 번째 레이어: 출력층 (softmax는 손실 함수에서 처리되거나 추론 시 적용)
        x = self.fc2(x)
        return x


if __name__ == "__main__":
    mnist_test = MnistTest()
    arr = mnist_test.create_model()
