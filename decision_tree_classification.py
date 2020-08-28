# importing the datasets
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


# importing the dataset
dataset = pd.read_csv('datas.csv')

# importing the datasets
X = dataset.iloc[:, [0, 1,2,3,4,5,6]].values
y = dataset.iloc[:, 7].values
#print(len(X))

# Desicion Tree Classification

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Calculating the accuracy measure
accuracy_score(y_test, y_pred)

# Calculating the F-score
f1_score(y_test, y_pred, average='macro')



# Here I will import the test dataset and check the accuracy on that.
dataset_test = pd.read_csv("data.csv")
X_test = dataset_test.iloc[:, [0, 1,2,3,4,5,6]].values
#print(len(X_test))
y_test = dataset_test.iloc[:,7].values
X_test = sc.transform(X_test)
y_pred = classifier.predict(X_test)
print(y_pred.tolist())
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))
