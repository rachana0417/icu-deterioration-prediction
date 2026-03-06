import numpy as np
import pandas as pd

# number of samples
samples = 2000

# sequence length
timesteps = 20

data = []
labels = []

for i in range(samples):

    hr = np.random.normal(85,5,timesteps)
    spo2 = np.random.normal(98,1,timesteps)
    rr = np.random.normal(16,2,timesteps)

    sequence = np.stack([hr,spo2,rr],axis=1)

    # deterioration condition
    if hr.mean()>95 or spo2.mean()<94 or rr.mean()>20:
        label = 1
    else:
        label = 0

    data.append(sequence)
    labels.append(label)

X = np.array(data)
y = np.array(labels)

np.save("X.npy",X)
np.save("y.npy",y)

print("Dataset created")
print("Shape:",X.shape)