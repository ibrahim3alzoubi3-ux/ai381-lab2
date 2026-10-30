import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA = "churn_v1.csv"

df = pd.read_csv(DATA)

df = df.rename(columns={
    "monthly_fee": "monthly_charges"
})

print("Dataset loaded successfully!")
print(df.shape)

numeric = ["tenure_months", "monthly_charges", "support_calls"]
categorical = ["contract", "internet_service"]

X = df[numeric + categorical]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Data split completed!")

model = Pipeline([
    ("prep", ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])),
    ("clf", LogisticRegression(max_iter=1000)),
])

model.fit(X_train, y_train)

print("Model trained successfully!")

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print("F1:", round(f1, 3))
print("AUC:", round(auc, 3))

joblib.dump(model, "model.joblib")
print("Model saved successfully!")