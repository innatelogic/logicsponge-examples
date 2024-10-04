import torch
import zmq
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

port = 5555
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(f"tcp://localhost:{port}")

THRESHOLD = 0.5

# Generate 1000 samples with 2 features and labels 1 and 0
X = torch.randn(1000, 2)
y = (X[:, 0] + X[:, 1] > 0).float()

# Split into training and test sets (80% train, 20% test)
train_size = int(0.8 * X.size(0))
test_size = X.size(0) - train_size
X_train, X_test = torch.split(X, [train_size, test_size])
y_train, y_test = torch.split(y, [train_size, test_size])

# Create DataLoader for the training data
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)


class LogisticRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 1)

    def forward(self, x):
        return torch.sigmoid(self.linear(x))


model = LogisticRegressionModel()
criterion = nn.BCELoss()  # Binary Cross-Entropy Loss
optimizer = optim.SGD(model.parameters(), lr=0.01)  # type: ignore

for epoch in range(1000):
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        optimizer.zero_grad()  # Zero the parameter gradients

        # Forward pass
        outputs = model(inputs).squeeze()
        loss = criterion(outputs, labels)

        # Backward pass and optimize
        loss.backward()
        optimizer.step()

        # Accumulate loss
        running_loss += loss.item()

        # Calculate accuracy
        predicted = (outputs > THRESHOLD).float()
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    # Print loss and accuracy per epoch
    current_loss = running_loss / len(train_loader)
    accuracy = 100 * correct / total
    socket.send_json({"epoch": epoch + 1, "loss": current_loss, "accuracy": accuracy})
    print(f"Epoch {epoch + 1}, Loss: {current_loss:.4f}, Accuracy: {accuracy:.2f}%")
