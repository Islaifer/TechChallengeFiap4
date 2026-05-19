import torch
import torch.nn as nn
from app.core.config import settings
import joblib

model = None
def get_neural_network():
    global model
    if model is None:
        model = NeuralNetwork(input_size = 5, output_size=1, num_layers = 10, hidden_size = 64)
        model.load_state_dict(torch.load(settings.MODEL_PATH))

    return model

x_scaler = None
def get_x_scaler():
    global x_scaler
    if x_scaler is None:
        x_scaler = joblib.load(settings.X_SCALER_PATH)
    return x_scaler

y_scaler = None
def get_y_scaler():
    global y_scaler
    if y_scaler is None:
        y_scaler = joblib.load(settings.Y_SCALER_PATH)
    return y_scaler

class NeuralNetwork(nn.Module):
    def __init__(self, input_size = 1, output_size=1, num_layers = 4, hidden_size = 32):
        super().__init__()
        
        self.lstm = nn.LSTM(input_size=input_size, num_layers=num_layers, hidden_size=hidden_size, batch_first=True)

        self.linear = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        output, _ = self.lstm(x)

        output = output[:, -1, :]
        output = self.linear(output)

        return output