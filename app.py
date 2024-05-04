from flask import Flask, request, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load dataset
df = pd.read_csv('dataset_phishing.csv')

# Convert 'status' column to binary values
mapping = {'legitimate': 0, 'phishing': 1}
df['status'] = df['status'].map(mapping)

# Select relevant features
X = df[['length_url', 'length_hostname', 'nb_dots', 'nb_hyphens', 'nb_at', 'nb_qm', 'nb_and', 'nb_eq', 'nb_slash']]
y = df['status']

# Train the RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features = extract_features(url)
    prediction = predict_phishing(features)
    return str(prediction)

def extract_features(url):
    # Extract features from the URL (simplified for demonstration)
    length_url = len(url)
    length_hostname = url.count('/')
    nb_dots = url.count('.')
    nb_hyphens = url.count('-')
    nb_at = url.count('@')
    nb_qm = url.count('?')
    nb_and = url.count('&')
    nb_eq = url.count('=')
    nb_slash = url.count('/')
    return [length_url, length_hostname, nb_dots, nb_hyphens, nb_at, nb_qm, nb_and, nb_eq, nb_slash]

def predict_phishing(features):
    # Predict using the trained model
    prediction = rf.predict([features])
    return prediction[0]

if __name__ == '__main__':
    app.run(debug=True)
