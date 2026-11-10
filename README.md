# House Price Predictor

A machine learning web app that predicts house prices from property features. A scikit-learn regression model is served through a FastAPI backend, and a vanilla JavaScript frontend builds its input form dynamically from the model's feature list.

![Python](https://img.shields.io/badge/Python-3.8+-21262d?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-21262d?style=flat-square&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-21262d?style=flat-square&logo=scikitlearn&logoColor=white)

![App screenshot](docs/screenshot.png)
<!-- FILL IN: add a screenshot of the form and a prediction result at docs/screenshot.png -->

## Model

| | |
|---|---|
| **Dataset** | [FILL IN: name, source link, number of rows and features] |
| **Final model** | Gradient Boosting Regressor |
| **Other models compared** | [FILL IN: e.g. Linear Regression, Random Forest] |
| **R²** | [FILL IN] |
| **RMSE** | [FILL IN] |

Training and evaluation are in [`notebooks/training.ipynb`](notebooks/training.ipynb).
<!-- FILL IN: add your training notebook to the repo and keep this link, or remove the line -->

## How it works

1. The model, optional scaler and feature names are loaded from `saved_models/` at startup.
2. The frontend requests `/features` and generates one input field per model feature.
3. The form is submitted to `/predict`, which applies the scaler (if present), runs the model and returns the predicted price.

## Project structure

```
house_price_app/
├── main.py              # FastAPI application
├── requirements.txt
├── notebooks/           # Training and evaluation
├── saved_models/
│   ├── best_model.pkl
│   ├── scaler.pkl       # optional
│   └── feature_names.pkl
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Getting started

```bash
git clone https://github.com/NikhilForge/AI-House-Price-Recommendation-System.git
cd AI-House-Price-Recommendation-System

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 for the app and http://127.0.0.1:8000/docs for the interactive API docs.

The app expects `best_model.pkl` and a feature names file (`feature_names.pkl` or `feature_names.txt`) in `saved_models/` or the project root. `scaler.pkl` is used if present.

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/features` | Feature names and metadata used to build the form |
| POST | `/predict` | Returns a price prediction for the submitted features |
| GET | `/model-info` | Information about the loaded model |
| GET | `/health` | Confirms the app is running and the model is loaded |

**Example request**

```json
POST /predict
{
  "features": {
    "OverallQual": 7,
    "GrLivArea": 1500,
    "TotalBsmtSF": 1000
  }
}
```

**Example response**

```json
{
  "predicted_price": 250000.50,
  "formatted_price": "$250,000.50",
  "model_name": "GradientBoostingRegressor"
}
```

## Using your own model

The model must be saved with `joblib.dump(model, "best_model.pkl")`, expose a `predict()` method that accepts a NumPy array, and have its feature names saved alongside it. If features were scaled during training, include the fitted scaler as `scaler.pkl`.

## Limitations

- The model only predicts well for houses similar to its training data.
- Predictions are estimates, not valuations.

## Roadmap

- [ ] Store prediction history
- [ ] Add feature importance chart
- [ ] Compare multiple models in the UI

## License

MIT
