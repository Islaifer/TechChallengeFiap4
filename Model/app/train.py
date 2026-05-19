import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error

from model import NeuralNetwork

def train(model: NeuralNetwork, x_train, y_train, epochs=50):
    print("Start model training")
    print("Preparing criterion and optimizer algoritm")
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Prepare train dataset")
    dataset = TensorDataset(x_train, y_train)
    loader = DataLoader(
        dataset,
        batch_size=30,
        shuffle=True
    )

    print(f"Start train with {epochs} epochs")
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for x_batch, y_batch in loader:
            optimizer.zero_grad() 
            output = model(x_batch) 
            loss = criterion(output, y_batch) 
            #loss = criterion(scaler.inverse_transform(output), scaler.inverse_transform(y_batch)) 
            loss.backward() 
            optimizer.step()

            epoch_loss += loss.item() * x_batch.size(0)

        loss_mean = epoch_loss / len(loader.dataset)

        print(f"Epoch[{epoch}/{epochs}] Loss Mean = {loss_mean:.4f}")

    print("Finish train model")


def evaluate(model: NeuralNetwork, x_test, y_test, scaler):
    print("Start model test")
    model.eval()

    predicts = []
    real_values = []

    print("Prepare test dataset")
    dataset = TensorDataset(x_test, y_test)
    loader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=False
    )

    print("Start tests")
    with torch.no_grad():
        for x_batch, y_batch in loader:
            result = model(x_batch)

            predicts.append(scaler.inverse_transform(result.numpy()))
            real_values.append(scaler.inverse_transform(y_batch.numpy()))

    predicts = np.vstack(predicts)
    real_values = np.vstack(real_values)

    mape = mean_absolute_percentage_error(real_values, predicts) 
    mae = mean_absolute_error(real_values, predicts)
    mse = mean_squared_error(real_values, predicts)
    rmse = np.sqrt(mse)

    print(" --- TEST RESULT ---")
    print(f"MAPE: {(mape * 100):.2f}%")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(" -------------------")
    
