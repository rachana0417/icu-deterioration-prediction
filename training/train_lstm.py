import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

print("Loading time-series dataset...")

df = pd.read_csv("data/timeseries_dataset.csv")

data = df.values

# Convert to tensor
X = torch.tensor(data, dtype=torch.float32)

# Dummy labels for now (hackathon prototype)
y = torch.randint(0, 2, (len(X),))

# Reshape for LSTM
X = X.unsqueeze(-1)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

print("Dataset prepared")

class LSTMModel(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=32, batch_first=True)
        self.fc = nn.Linear(32, 1)
    
    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return out

model = LSTMModel()

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

print("Training model...")

for epoch in range(5):
    
    for X_batch, y_batch in loader:
        
        preds = model(X_batch).squeeze()
        
        loss = criterion(preds, y_batch.float())
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print(f"Epoch {epoch+1} Loss:", loss.item())

print("Training complete")

torch.save(model.state_dict(), "models/lstm_model.pth")

print("Model saved in models/lstm_model.pth")