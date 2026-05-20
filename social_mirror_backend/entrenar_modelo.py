import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

#  Rutas
train_dir = r"C:\Users\moise\OneDrive\Escritorio\fer2013\train"
test_dir = r"C:\Users\moise\OneDrive\Escritorio\fer2013\test"

#  Transformaciones
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48,48)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])

def main():
    print("📦 Cargando dataset...")

    # 📦 Dataset
    train_data = datasets.ImageFolder(train_dir, transform=transform)
    test_data = datasets.ImageFolder(test_dir, transform=transform)

    print(f"✅ Imágenes de entrenamiento: {len(train_data)}")
    print(f"✅ Imágenes de prueba: {len(test_data)}")

    #  DataLoader 
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_data, batch_size=32, num_workers=0)

    #  Modelo CNN
    class EmotionModel(nn.Module):
     def __init__(self):
        super(EmotionModel, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 7)
        )

    
     def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

    #  Configuración
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️ Usando dispositivo: {device}")

    model = EmotionModel().to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0005)

    #  ENTRENAMIENTO
    epochs = 30

    print("🚀 Iniciando entrenamiento...")

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            if batch_idx % 100 == 0:
                print(f"Epoch {epoch+1} | Batch {batch_idx} | Loss: {loss.item():.4f}")

        print(f"🔥 Epoch {epoch+1} completado | Loss total: {total_loss:.2f}")

    #  EVALUACIÓN
    print("🧪 Evaluando modelo...")

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"\n🎯 Precisión en test: {accuracy:.2f}%")

    #  GUARDAR MODELO
    torch.save(model.state_dict(), "model.pth")
    print("💾 Modelo guardado como model.pth")



if __name__ == "__main__":
    main()