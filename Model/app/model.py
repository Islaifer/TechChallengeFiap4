import torch
import torch.nn as nn

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
    

def save_model(model: NeuralNetwork, path):
    torch.save(model.state_dict(), path)