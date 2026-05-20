import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Clases
emociones = ["angry", "fear", "happy", "sad", "surprise", "neutral"]

# Transformaciones
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor()
])

#  RUTAS 
train_path = "C:/Users/moise/OneDrive/Escritorio/fer2013/train"
test_path  = "C:/Users/moise/OneDrive/Escritorio/fer2013/test"

# Cargar datos
train_data = datasets.ImageFolder(train_path, transform=transform)
test_data  = datasets.ImageFolder(test_path, transform=transform)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader  = DataLoader(test_data, batch_size=32)

# Modelo
class EmotionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 10 * 10, 128),
            nn.ReLU(),
            nn.Linear(128, len(emociones))
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

model = EmotionModel()

# Entrenamiento
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5  

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for images, labels in train_loader:
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")


model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"🎯 Precisión en test: {accuracy:.2f}%")

# Guardar modelo
torch.save(model.state_dict(), "model.pth")

print("✅ Modelo entrenado y evaluado")