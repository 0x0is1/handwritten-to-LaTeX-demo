import glob

import cv2
import torchvision.transforms as transforms
from PIL import Image

from learner.resnet18_vgg16 import HandwrittenSymbolsClassifier

model_name = "resnet34"  # or 'vgg16' biggest 'resnet50' 'resnet34' and  'resnet18' smallest

classifier = HandwrittenSymbolsClassifier(
    root_dir="./learner/datasets/extracted_images/",
    epochs=5,
    batch_size=64,  # for vgg16 and resnet50 use 32 otherwise 64
    model_type=f"{model_name}",
)

try:
    classifier.load_model(f"./learner/models/test_{model_name}.torch")
    print("Model loaded successfully")
except Exception as e:
    try:
        classifier.train()
        classifier.save_model("./learner/models/", f"test_{model_name}.torch")
        classifier.load_model(f"./learner/models/test_{model_name}.torch")
        print("Model trained and saved successfully")
    except Exception as e:
        print(e)


# testing

transformtosize = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
image_paths = glob.glob("extracted_characters/bec2e9415f294141a33a6a589432d364/**/*", recursive=True)

for image_path in image_paths:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(image, (45, 45), interpolation=cv2.INTER_AREA)
    if len(resized_image.shape) == 3:
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = resized_image

    _, bw_image = cv2.threshold(gray_image, 220, 256, cv2.THRESH_BINARY)

    cv2.imwrite(image_path, bw_image)
    prediction = classifier.predict(image_path=image_path)
    print(f"Prediction for {image_path}: {prediction}")
    # it should come cos,Beta,equalto,exclamation, three