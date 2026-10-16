import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:

    Xy = load_diabetes(as_frame=True)

    # pyrefly: ignore[missing-attribute]
    X = Xy.frame.drop(columns=["target"])

    # pyrefly: ignore[missing-attribute]
    y = Xy.frame["target"] # acts as a "progression index" (higher = worse)
    
    print("------")
    print(f"Data points: {X.shape[0]}")
    print("------")
    print(f"Columns: {X.columns}")
    print("------")
    print(f"First 5: {X.head()}")
    print("------")
    print(f"Description: {y.describe()}")
    print("------")
    print(f"Head: {y.head()}")
    print("------")
    
    return X, y

def prepare_model(X: pd.DataFrame, y: pd.Series):
    
    model = LinearRegression()
    kfold = KFold(n_splits=5, shuffle=True, random_state=0)
    r2_scores = cross_val_score(model, X, y, cv=kfold, scoring="r2")
    print(f"R2 Scores: {r2_scores}")
    mean_squared_error_scores = cross_val_score(model, X, y, cv=kfold, scoring="neg_mean_squared_error")
    print(f"Mean squared error scores: {mean_squared_error_scores}")
    model.fit(X, y)
    
    return model


#@memfile("/app/data/results.json")
#def save_to_file():

def main():
    X, y = load_dataset()
    model: LinearRegression = prepare_model(X, y)
    row = pd.DataFrame([[0.2, -0.044642, -0.051474, -0.026328, -0.008449,
                     -0.019163, 0.074412, -0.039493, -0.068332, -0.092204], [-0.001882, -0.044642, -0.051474, -0.026328, -0.008449,
                     -0.019163, 0.074412, -0.039493, -0.068332, -0.092204]],
                   columns=X.columns)
    print(f"Prediction: {model.predict(row)}")
    
if __name__ == "__main__":
    main()