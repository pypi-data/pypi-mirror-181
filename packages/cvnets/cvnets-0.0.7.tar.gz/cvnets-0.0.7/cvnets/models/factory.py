import timm
import torch
from torch import nn


if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    def model():
        return NeuralNetwork()


def create_model(name, n_dim=None, pretrained=False):
    print(f"'device' is assigned as {device}")
    if name == "NeuralNetwork":
        model = NeuralNetwork.model().to(device)
    elif len(name):
        if n_dim is not None:
            model = timm.create_model(
                name, num_classes=n_dim, pretrained=pretrained).to(device)
        else:
            model = timm.create_model(name, pretrained=pretrained).to(device)
    return model
