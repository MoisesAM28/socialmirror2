import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# 🔥 Transformaciones PRO
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])

# Dataset
dataset = datasets.ImageFolder("dataset", transform=transform)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

print("Clases:", dataset.classes)

# 🔥 MODELO PREENTRENADO
model = models.resnet18(weights="DEFAULT")

# Congelar capas (IMPORTANTE)
for param in model.parameters():
    param.requires_grad = False

# Solo entrenar última capa
model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# 🔥 ENTRENAMIENTO
for epoch in range(10):
    total_loss = 0

    for imgs, labels in loader:
        optimizer.zero_grad()

        outputs = model(imgs)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

torch.save(model.state_dict(), "model_resnet.pth")

print("✅ Modelo PRO entrenado")