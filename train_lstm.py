import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

# Load dataset
X = np.load("X.npy")
y = np.load("y.npy")

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# -------------------------
# LSTM MODEL
# -------------------------

class LSTMModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=3,
            hidden_size=64,
            num_layers=2,
            batch_first=True
        )

        self.fc = nn.Linear(64,1)

        self.sigmoid = nn.Sigmoid()

    def forward(self,x):

        out,_ = self.lstm(x)

        out = out[:,-1,:]

        out = self.fc(out)

        out = self.sigmoid(out)

        return out


model = LSTMModel()

criterion = nn.BCELoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# -------------------------
# TRAIN MODEL
# -------------------------

epochs = 15

for epoch in range(epochs):

    total_loss = 0

    for xb,yb in loader:

        pred = model(xb).squeeze()

        loss = criterion(pred,yb)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} Loss {total_loss:.4f}")

# -------------------------
# SAVE MODEL
# -------------------------

torch.save(model.state_dict(),"icu_lstm_model.pth")

print("Model saved")