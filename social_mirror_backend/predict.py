import torch
import torch.nn as nn
import cv2
from torchvision import transforms
from PIL import Image

print("🔥 USANDO MODELO CNN ENTRENADO 🔥")

emociones = ["angry","disgust","fear","happy","sad","surprise","neutral"]

# ==============================
# 🧠 MODELO (IGUAL AL ENTRENAMIENTO)
# ==============================
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

# ==============================
# 🧠 CARGAR MODELO
# ==============================
model = EmotionModel()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

print("✅ Modelo CNN cargado")

# ==============================
# 🧠 TRANSFORMACIONES
# ==============================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48,48)),
    transforms.ToTensor()
])

# ==============================
# 🧠 DETECCIÓN DE ROSTRO
# ==============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detectar_cara(imagen_path):
    img = cv2.imread(imagen_path)

    if img is None:
        print("❌ No se pudo cargar la imagen")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("⚠️ No se detectó rostro")
        return None

    # Tomar la cara más grande
    faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
    (x, y, w, h) = faces[0]

    rostro = gray[y:y+h, x:x+w]

    return rostro

# ==============================
# 🚀 PREDICCIÓN
# ==============================
def predecir_emocion(imagen_path):
    try:
        print("\n📸 Nueva imagen:", imagen_path)

        rostro = detectar_cara(imagen_path)

        if rostro is None:
            return "neutral", "No se detectó rostro"

        # Convertir a PIL
        img = Image.fromarray(rostro)

        # Transformaciones
        img = transform(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            output = model(img)

            prob = torch.softmax(output, dim=1)
            confianza, pred = torch.max(prob, 1)

        emocion = emociones[pred.item()]
        confianza_valor = confianza.item()

        print("😊 EMOCION:", emocion)
        print("📊 CONFIANZA:", confianza_valor)

        # 🔥 FILTRO PARA MEJORAR RESULTADOS
        if confianza_valor < 0.6:
            emocion = "neutral"

        return emocion, f"{emocion} ({confianza_valor:.2f})"

    except Exception as e:
        print("💥 ERROR:", e)
        return "neutral", "Error al procesar imagen"