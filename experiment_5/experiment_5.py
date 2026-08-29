import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
data = pd.read_csv("logistic_data.csv")

# Display the dataset
print("Dataset:")
print(data)
# Display the first 5 rows
print("\nFirst 5 Rows:")
print(data.head())

# Display dataset shape
print("\nDataset Shape:")
print(data.shape)

# Display dataset information
print("\nDataset Information:")
data.info()

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())
# Define features
X = data[["Hours_Studied", "Attendance", "Previous_Score"]]

# Define target variable
y = data["Pass"]

# Display features
print("\nFeatures (X):")
print(X.head())

# Display target
print("\nTarget Variable (y):")
print(y.head())
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Display the size of training and testing data
print("\nTraining Data Shape:")
print(X_train.shape)

print("\nTesting Data Shape:")
print(X_test.shape)

print("\nTraining Target Shape:")
print(y_train.shape)

print("\nTesting Target Shape:")
print(y_test.shape)
# Create StandardScaler object
scaler = StandardScaler()

# Fit the scaler on training data and transform it
X_train_scaled = scaler.fit_transform(X_train)

# Transform testing data using the same scaler
X_test_scaled = scaler.transform(X_test)

# Display scaled training data
print("\nScaled Training Data:")
print(X_train_scaled)

# Display scaled testing data
print("\nScaled Testing Data:")
print(X_test_scaled)
# Create the Logistic Regression model
model = LogisticRegression()

# Train the model using scaled training data
model.fit(X_train_scaled, y_train)

print("\nLogistic Regression Model Trained Successfully!")
# Make predictions using the trained model
y_pred = model.predict(X_test_scaled)

# Display actual and predicted values
print("\nActual Values:")
print(y_test.values)

print("\nPredicted Values:")
print(y_pred)
# Calculate model accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)

# Display classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
# Create confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Create confusion matrix visualization
plt.figure(figsize=(6, 5))
plt.imshow(cm)
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.xticks([0, 1], ["Fail (0)", "Pass (1)"])
plt.yticks([0, 1], ["Fail (0)", "Pass (1)"])

# Add values inside the confusion matrix
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i, j]),
                 ha="center", va="center", fontsize=14)

plt.tight_layout()

# Save the graph
plt.savefig("confusion_matrix.png")

print("\nConfusion matrix graph saved as confusion_matrix.png")
