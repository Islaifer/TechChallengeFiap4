import yfinance as yf
import pandas as pd
import numpy as np
import torch
import joblib
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from model import NeuralNetwork, save_model
from train import train, evaluate

ticker_disney = "DIS"
start_date = "2020-01-01"

yesterday = datetime.now() - timedelta(days=1)
end_date = yesterday.strftime('%Y-%m-%d')

data = yf.download(ticker_disney, start=start_date, end=end_date)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

data.columns = [x for x in data.columns if x != 'Price']
data = data.reset_index(drop=True)

#print(data.head(15))
lines, columns = data.shape
print(f"Data size = {lines}")
print(f"Feature size = {columns}")

print("Splitting data to test (20%) and train (80%)")
y = data['Close']

split_index = int(lines * 0.8)

x_train_data = data[:split_index]
x_test_data  = data[split_index:]

y_train_data = y[:split_index].values.reshape(-1, 1)
y_test_data  = y[split_index:].values.reshape(-1, 1)

scaler_x = MinMaxScaler()
x_train_scaled = scaler_x.fit_transform(x_train_data)
x_test_scaled  = scaler_x.transform(x_test_data)

scaler_y = MinMaxScaler()
y_train_scaled = scaler_y.fit_transform(y_train_data)
y_test_scaled = scaler_y.transform(y_test_data)

def prepare_multi_steps_data(x_data, y_data, seq_len=5):
    x_finals, y_finals = [], []
    for i in range(len(x_data) - seq_len):
        x_finals.append(x_data[i:i+seq_len])
        y_finals.append(y_data[i+seq_len])
        
    return torch.FloatTensor(np.array(x_finals)), torch.FloatTensor(np.array(y_finals))

x_train, y_train = prepare_multi_steps_data(x_train_scaled, y_train_scaled, seq_len=90)
x_test, y_test   = prepare_multi_steps_data(x_test_scaled, y_test_scaled, seq_len=90)

model = NeuralNetwork(input_size = 5, output_size=1, num_layers = 10, hidden_size = 64)
train(model, x_train, y_train, epochs=50)
evaluate(model, x_test, y_test, scaler_y)

print("Saving model and scalers...")
save_model(model, "../../SavedModels/model.pth")
joblib.dump(scaler_x, "../../SavedModels/scaler_x.pkl")
joblib.dump(scaler_y, "../../SavedModels/scaler_y.pkl")

print("Finish Model Generate")