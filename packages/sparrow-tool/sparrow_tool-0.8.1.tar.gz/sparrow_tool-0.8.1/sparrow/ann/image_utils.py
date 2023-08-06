import torch
from torchvision import models
from torchvision.models.efficientnet import EfficientNet_B7_Weights
from torchvision import transforms


def get_model():
    torch_model = models.efficientnet_b7(weights=EfficientNet_B7_Weights.DEFAULT)
    torch_model = torch.nn.Sequential(*(list(torch_model.children())[:-1]))
    torch_model.to('cuda' if torch.cuda.is_available() else 'cpu')
    torch_model.eval()
    return torch_model


preprocess = transforms.Compose([
    transforms.Resize(size=224, interpolation=transforms.InterpolationMode.BICUBIC),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
