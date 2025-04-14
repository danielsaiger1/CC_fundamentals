from ultralytics import YOLO

# Modell laden (z. B. ein klassifiziertes Modell wie yolov8n-cls.pt)
model = YOLO('yolo11n-cls.pt')

# Vorhersage
results = model('dog.jpg')

# Ausgabe der Top-1-Klasse
for result in results:
    print(f"Bild: {result.path}")
    print(f"Klasse: {result.names[result.probs.top1]}")
    print(f"Top-1 Wahrscheinlichkeit: {result.probs.top1conf:.2f}")
