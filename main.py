"""
FastAPI Backend for House Price Prediction
HIGH-IMPACT FEATURES VERSION + PRICE RECOMMENDATIONS
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import joblib
import numpy as np
import pandas as pd
import os
import json

app = FastAPI(
    title="House Price Prediction API",
    description="AI-powered house price prediction - High-Impact Features + Recommendations",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
scaler = None
feature_names = []
feature_info = {}

USER_INPUT_FEATURES = [
    'location_type',
    'overall_quality',
    'overall_condition',
    'house_style',
    'bedrooms',
    'bathrooms',
    'house_sqft',
    'lot_sqft',
    'year_built',
    'basement_sqft',
    'basement_finish',
    'garage_type',
    'year_renovated',
]

LOCATION_TYPES = {
    'downtown': {
        'label': 'Downtown / City Center',
        'description': 'Urban core, close to everything',
        'multiplier': 1.3,
        'neighborhood_code': 6
    },
    'suburban_premium': {
        'label': 'Premium Suburban (Gated/Upscale)',
        'description': 'High-end residential, excellent schools',
        'multiplier': 1.25,
        'neighborhood_code': 15
    },
    'suburban_standard': {
        'label': 'Standard Suburban Residential',
        'description': 'Family-friendly neighborhoods',
        'multiplier': 1.0,
        'neighborhood_code': 12
    },
    'near_school': {
        'label': 'Near School/University',
        'description': 'Walking distance to schools',
        'multiplier': 1.1,
        'neighborhood_code': 5
    },
    'near_shopping': {
        'label': 'Near Shopping/Commercial',
        'description': 'Close to malls and shopping centers',
        'multiplier': 1.05,
        'neighborhood_code': 7
    },
    'near_park': {
        'label': 'Near Park/Recreation',
        'description': 'Green spaces and outdoor areas',
        'multiplier': 1.08,
        'neighborhood_code': 8
    },
    'waterfront': {
        'label': 'Waterfront/Lakeside',
        'description': 'Near water bodies',
        'multiplier': 1.35,
        'neighborhood_code': 13
    },
    'historic': {
        'label': 'Historic District/Old Town',
        'description': 'Historic areas, older homes',
        'multiplier': 0.85,
        'neighborhood_code': 17
    },
    'developing': {
        'label': 'Developing Area',
        'description': 'New development, growing area',
        'multiplier': 0.95,
        'neighborhood_code': 11
    },
    'rural': {
        'label': 'Rural/Countryside',
        'description': 'Away from city, large lots',
        'multiplier': 0.75,
        'neighborhood_code': 10
    },
    'industrial': {
        'label': 'Near Industrial/Commercial Zone',
        'description': 'Mixed use, some industrial',
        'multiplier': 0.7,
        'neighborhood_code': 9
    },
}

SMART_DEFAULTS = {
    'MSSubClass': 60,
    'MSZoning': 3,
    'Street': 1,
    'Alley': 0,
    'LotShape': 3,
    'LandContour': 3,
    'Utilities': 3,
    'LotConfig': 4,
    'LandSlope': 0,
    'Condition1': 2,
    'Condition2': 2,
    'BldgType': 0,
    'RoofStyle': 1,
    'RoofMatl': 1,
    'Exterior1st': 12,
    'Exterior2nd': 12,
    'MasVnrType': 1,
    'MasVnrArea': 100,
    'ExterQual': 2,
    'ExterCond': 2,
    'Foundation': 2,
    'BsmtQual': 2,
    'BsmtCond': 2,
    'BsmtExposure': 1,
    'BsmtFinType1': 2,
    'BsmtFinType2': 5,
    'BsmtFinSF1': 500,
    'BsmtFinSF2': 0,
    'BsmtUnfSF': 500,
    'Heating': 2,
    'HeatingQC': 2,
    'CentralAir': 1,
    'Electrical': 4,
    'LowQualFinSF': 0,
    'BsmtFullBath': 0,
    'BsmtHalfBath': 0,
    'HalfBath': 1,
    'KitchenAbvGr': 1,
    'KitchenQual': 2,
    'Functional': 6,
    'Fireplaces': 1,
    'FireplaceQu': 2,
    'GarageType': 1,
    'GarageYrBlt': 2000,
    'GarageFinish': 2,
    'GarageQual': 2,
    'GarageCond': 2,
    'PavedDrive': 2,
    'WoodDeckSF': 100,
    'OpenPorchSF': 50,
    'EnclosedPorch': 0,
    '3SsnPorch': 0,
    'ScreenPorch': 0,
    'PoolArea': 0,
    'PoolQC': 0,
    'Fence': 0,
    'MiscFeature': 0,
    'MiscVal': 0,
    'MoSold': 6,
    'YrSold': 2024,
    'SaleType': 8,
    'SaleCondition': 4,
}

USER_FIELD_INFO = {
    'location_type': {
        'label': 'Location Type',
        'type': 'select',
        'options': [
            {'value': key, 'label': info['label']}
            for key, info in LOCATION_TYPES.items()
        ],
        'default': 'suburban_standard',
        'description': 'What type of area? (CRITICAL FACTOR!)',
        'icon': '📍'
    },
    'overall_quality': {
        'label': 'Overall Quality',
        'type': 'select',
        'options': [
            {'value': 1, 'label': '1 - Very Poor'},
            {'value': 2, 'label': '2 - Poor'},
            {'value': 3, 'label': '3 - Fair'},
            {'value': 4, 'label': '4 - Below Average'},
            {'value': 5, 'label': '5 - Average'},
            {'value': 6, 'label': '6 - Above Average'},
            {'value': 7, 'label': '7 - Good'},
            {'value': 8, 'label': '8 - Very Good'},
            {'value': 9, 'label': '9 - Excellent'},
            {'value': 10, 'label': '10 - Very Excellent'},
        ],
        'default': 7,
        'description': 'Material & finish quality (TOP PREDICTOR!)',
        'icon': '⭐'
    },
    'overall_condition': {
        'label': 'Overall Condition',
        'type': 'select',
        'options': [
            {'value': 1, 'label': '1 - Very Poor'},
            {'value': 2, 'label': '2 - Poor'},
            {'value': 3, 'label': '3 - Fair'},
            {'value': 4, 'label': '4 - Below Average'},
            {'value': 5, 'label': '5 - Average'},
            {'value': 6, 'label': '6 - Above Average'},
            {'value': 7, 'label': '7 - Good'},
            {'value': 8, 'label': '8 - Very Good'},
            {'value': 9, 'label': '9 - Excellent'},
            {'value': 10, 'label': '10 - Very Excellent'},
        ],
        'default': 5,
        'description': 'Current condition rating',
        'icon': '🏠'
    },
    'house_style': {
        'label': 'House Style',
        'type': 'select',
        'options': [
            {'value': 'ranch', 'label': 'Ranch / Single Story'},
            {'value': 'two_story', 'label': 'Two Story'},
            {'value': 'split_level', 'label': 'Split Level'},
            {'value': 'tri_level', 'label': 'Tri-Level'},
            {'value': 'bungalow', 'label': 'Bungalow'},
        ],
        'default': 'two_story',
        'description': 'Architectural style',
        'icon': '🏡'
    },
    'bedrooms': {
        'label': 'Number of Bedrooms',
        'type': 'number',
        'min': 1,
        'max': 10,
        'step': 1,
        'default': 3,
        'description': 'How many bedrooms?',
        'icon': '🛏️'
    },
    'bathrooms': {
        'label': 'Number of Bathrooms',
        'type': 'number',
        'min': 1,
        'max': 8,
        'step': 0.5,
        'default': 2,
        'description': 'Full + half (e.g., 2.5)',
        'icon': '🚿'
    },
    'house_sqft': {
        'label': 'House Size (sq ft)',
        'type': 'number',
        'min': 500,
        'max': 10000,
        'step': 50,
        'default': 1800,
        'description': 'Total living area (MAJOR FACTOR!)',
        'icon': '📐'
    },
    'lot_sqft': {
        'label': 'Lot Size (sq ft)',
        'type': 'number',
        'min': 1000,
        'max': 50000,
        'step': 500,
        'default': 10000,
        'description': 'Land area',
        'icon': '🌳'
    },
    'year_built': {
        'label': 'Year Built',
        'type': 'number',
        'min': 1900,
        'max': 2025,
        'step': 1,
        'default': 2005,
        'description': 'Construction year',
        'icon': '📅'
    },
    'basement_sqft': {
        'label': 'Basement Size (sq ft)',
        'type': 'number',
        'min': 0,
        'max': 3000,
        'step': 50,
        'default': 1000,
        'description': '0 if no basement',
        'icon': '🏗️'
    },
    'basement_finish': {
        'label': 'Basement Finish Level',
        'type': 'select',
        'options': [
            {'value': 'none', 'label': 'No Basement'},
            {'value': 'unfinished', 'label': 'Completely Unfinished'},
            {'value': 'partial', 'label': 'Partially Finished (50%)'},
            {'value': 'mostly', 'label': 'Mostly Finished (75%)'},
            {'value': 'full', 'label': 'Fully Finished (100%)'},
        ],
        'default': 'partial',
        'description': 'Basement finish level (HIGH IMPACT!)',
        'icon': '🔨'
    },
    'garage_type': {
        'label': 'Garage Type',
        'type': 'select',
        'options': [
            {'value': 'none', 'label': 'No Garage'},
            {'value': 'carport', 'label': 'Carport'},
            {'value': 'detached', 'label': 'Detached Garage'},
            {'value': 'attached', 'label': 'Attached Garage'},
            {'value': 'builtin', 'label': 'Built-in Garage'},
        ],
        'default': 'attached',
        'description': 'Garage type (affects value!)',
        'icon': '🚗'
    },
    'year_renovated': {
        'label': 'Last Renovation Year',
        'type': 'number',
        'min': 1900,
        'max': 2025,
        'step': 1,
        'default': 2010,
        'description': 'Never? Use year built',
        'icon': '🔧'
    },
}


def load_model_and_features():
    global model, scaler, feature_names, feature_info

    try:
        model_path = "saved_models/best_model.pkl"
        scaler_path = "saved_models/scaler.pkl"
        features_pkl_path = "saved_models/feature_names.pkl"

        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
        elif os.path.exists("best_model.pkl"):
            model = joblib.load("best_model.pkl")
            print("✅ Model loaded from best_model.pkl")
        else:
            raise FileNotFoundError("Model file not found!")

        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print(f"✅ Scaler loaded from {scaler_path}")
        elif os.path.exists("scaler.pkl"):
            scaler = joblib.load("scaler.pkl")
            print("✅ Scaler loaded from scaler.pkl")
        else:
            print("⚠️ Scaler not found")
            scaler = None

        if os.path.exists(features_pkl_path):
            feature_names = joblib.load(features_pkl_path)
            print(f"✅ Features loaded from {features_pkl_path}")
        elif os.path.exists("feature_names.pkl"):
            feature_names = joblib.load("feature_names.pkl")
            print("✅ Features loaded from feature_names.pkl")
        else:
            raise FileNotFoundError("Feature names file not found!")

        feature_info = USER_FIELD_INFO
        print(f"\n📊 Model features: {len(feature_names)}")
        print(f"👤 User input fields: {len(USER_INPUT_FEATURES)}")
        print(f"📍 Location types: {len(LOCATION_TYPES)}")
        print(f"🎯 Model: {type(model).__name__}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


load_model_and_features()


def map_user_input_to_model_features(user_input):
    model_features = SMART_DEFAULTS.copy()

    location_type = user_input.get('location_type', 'suburban_standard')
    location_info = LOCATION_TYPES.get(location_type, LOCATION_TYPES['suburban_standard'])

    overall_quality    = int(user_input.get('overall_quality', 7))
    overall_condition  = int(user_input.get('overall_condition', 5))
    house_style        = user_input.get('house_style', 'two_story')
    bedrooms           = int(user_input.get('bedrooms', 3))
    bathrooms          = float(user_input.get('bathrooms', 2))
    house_sqft         = int(user_input.get('house_sqft', 1800))
    lot_sqft           = int(user_input.get('lot_sqft', 10000))
    year_built         = int(user_input.get('year_built', 2005))
    basement_sqft      = int(user_input.get('basement_sqft', 1000))
    basement_finish    = user_input.get('basement_finish', 'partial')
    # kitchen_quality defaults to 3 (Average) — not shown in UI
    kitchen_quality    = 3
    garage_type        = user_input.get('garage_type', 'attached')
    year_renovated     = int(user_input.get('year_renovated', year_built))
    # stories defaults to 2 — not shown in UI
    stories            = 2

    full_bath = int(bathrooms)
    half_bath = int((bathrooms % 1) * 2)

    basement_finish_ratios = {
        'none': 0.0, 'unfinished': 0.0,
        'partial': 0.5, 'mostly': 0.75, 'full': 1.0
    }
    finish_ratio  = basement_finish_ratios.get(basement_finish, 0.5)
    bsmt_fin_sf1  = int(basement_sqft * finish_ratio)
    bsmt_unf_sf   = int(basement_sqft * (1 - finish_ratio))

    basement_finish_quality = {
        'none': 0, 'unfinished': 1,
        'partial': 2, 'mostly': 3, 'full': 4
    }
    bsmt_qual = basement_finish_quality.get(basement_finish, 2)

    garage_cars_map = {
        'none': 0, 'carport': 1,
        'detached': 2, 'attached': 2, 'builtin': 2
    }
    garage_cars = garage_cars_map.get(garage_type, 2)
    garage_area = garage_cars * 250

    garage_type_code = {
        'none': 0, 'carport': 6,
        'detached': 2, 'attached': 1, 'builtin': 0
    }
    garage_type_value = garage_type_code.get(garage_type, 1)

    house_style_map = {
        'ranch': 5, 'two_story': 1,
        'split_level': 3, 'tri_level': 4, 'bungalow': 5
    }
    house_style_value = house_style_map.get(house_style, 1)

    if house_style == 'ranch':
        floor_1st = house_sqft
        floor_2nd = 0
    elif house_style == 'two_story':
        floor_1st = int(house_sqft * 0.55)
        floor_2nd = int(house_sqft * 0.45)
    else:
        floor_1st = int(house_sqft * 0.65)
        floor_2nd = int(house_sqft * 0.35)

    mappings = {
        'Neighborhood':    location_info['neighborhood_code'],
        'OverallQual':     overall_quality,
        'OverallCond':     overall_condition,
        'KitchenQual':     kitchen_quality,
        'BedroomAbvGr':    bedrooms,
        'FullBath':        full_bath,
        'HalfBath':        half_bath,
        'GrLivArea':       house_sqft,
        'LotArea':         lot_sqft,
        'LotFrontage':     int(lot_sqft ** 0.5),
        'YearBuilt':       year_built,
        'YearRemodAdd':    year_renovated,
        'TotalBsmtSF':     basement_sqft,
        'BsmtFinSF1':      bsmt_fin_sf1,
        'BsmtUnfSF':       bsmt_unf_sf,
        'BsmtQual':        bsmt_qual,
        'BsmtFinType1':    bsmt_qual,
        'GarageYrBlt':     year_built,
        'GarageCars':      garage_cars,
        'GarageArea':      garage_area,
        'GarageType':      garage_type_value,
        'GarageQual':      min(4, max(1, int(overall_quality / 2.5))) if garage_cars > 0 else 0,
        'HouseStyle':      house_style_value,
        '1stFlrSF':        floor_1st,
        '2ndFlrSF':        floor_2nd,
        'TotRmsAbvGrd':    bedrooms + 3,
        'ExterQual':       min(4, max(1, int(overall_quality / 2.5))),
        'HeatingQC':       min(4, max(1, int(overall_quality / 2.5))),
        'TotalSF':         house_sqft + basement_sqft,
        'HouseAge':        2024 - year_built,
        'YearsSinceRemod': 2024 - year_renovated,
        'TotalBathrooms':  full_bath + (half_bath * 0.5),
        'TotalPorchSF':    150,
    }

    for feature, value in mappings.items():
        if feature in feature_names:
            model_features[feature] = value

    return model_features, location_info['multiplier']


# ========================
# RECOMMENDATION ENGINE
# ========================

def compute_recommendations(price: float) -> dict:
    lower = price * 0.9
    upper = price * 1.1

    if price < 150000:
        market_insight = "Budget Property"
        market_icon    = "🏚️"
        market_color   = "budget"
    elif price <= 300000:
        market_insight = "Fairly Priced"
        market_icon    = "🏠"
        market_color   = "fair"
    else:
        market_insight = "Premium Property"
        market_icon    = "🏰"
        market_color   = "premium"

    if price < lower:
        suggestion      = "Great Deal — below market range"
        suggestion_icon = "🤑"
        suggestion_type = "deal"
    elif price <= upper:
        suggestion      = "Fair Price — within market range"
        suggestion_icon = "✅"
        suggestion_type = "fair"
    else:
        suggestion      = "Slightly Expensive — above market range"
        suggestion_icon = "⚠️"
        suggestion_type = "expensive"

    return {
        "range_lower":      lower,
        "range_upper":      upper,
        "range_lower_fmt":  f"${lower:,.0f}",
        "range_upper_fmt":  f"${upper:,.0f}",
        "market_insight":   market_insight,
        "market_icon":      market_icon,
        "market_color":     market_color,
        "suggestion":       suggestion,
        "suggestion_icon":  suggestion_icon,
        "suggestion_type":  suggestion_type,
        "tips": [
            f"💰 Good deal if listed below {f'${lower:,.0f}'}",
            f"✅ Fair price between {f'${lower:,.0f}'} – {f'${upper:,.0f}'}",
            f"🔴 Expensive if above {f'${upper:,.0f}'}",
        ]
    }


# ========================
# PYDANTIC MODELS
# ========================

class PredictionInput(BaseModel):
    features: Dict[str, Any]


class PredictionOutput(BaseModel):
    predicted_price:   float
    formatted_price:   str
    model_name:        str
    confidence:        str
    location_impact:   Optional[str] = None
    range_lower:       float
    range_upper:       float
    range_lower_fmt:   str
    range_upper_fmt:   str
    market_insight:    str
    market_icon:       str
    market_color:      str
    suggestion:        str
    suggestion_icon:   str
    suggestion_type:   str
    tips:              List[str]


# ========================
# API ENDPOINTS
# ========================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<html><body><h1>Frontend not found</h1></body></html>"


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "user_input_fields": len(USER_INPUT_FEATURES),
        "location_types": len(LOCATION_TYPES)
    }


@app.get("/features")
async def get_features():
    return {
        "features": USER_INPUT_FEATURES,
        "feature_info": USER_FIELD_INFO,
        "total_features": len(USER_INPUT_FEATURES),
        "location_types": LOCATION_TYPES
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict_price(input_data: PredictionInput):
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")

        model_features, location_multiplier = map_user_input_to_model_features(input_data.features)

        feature_array = np.array([
            model_features.get(feature, SMART_DEFAULTS.get(feature, 0))
            for feature in feature_names
        ])
        feature_array = feature_array.reshape(1, -1)

        if scaler is not None:
            feature_array = scaler.transform(feature_array)

        base_prediction = model.predict(feature_array)[0]
        prediction      = max(0, base_prediction * location_multiplier)

        formatted_price = f"${prediction:,.2f}"
        confidence      = "High" if prediction > 50000 else "Medium"

        location_type = input_data.features.get('location_type', 'suburban_standard')
        location_name = LOCATION_TYPES[location_type]['label']
        location_impact = f"Location ({location_name}): {location_multiplier}x"

        rec = compute_recommendations(prediction)

        return PredictionOutput(
            predicted_price=float(prediction),
            formatted_price=formatted_price,
            model_name=type(model).__name__,
            confidence=confidence,
            location_impact=location_impact,
            **rec
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@app.get("/model-info")
async def get_model_info():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {
        "model_type":     type(model).__name__,
        "user_fields":    USER_INPUT_FEATURES,
        "location_types": list(LOCATION_TYPES.keys())
    }


if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    print("\n" + "="*80)
    print("🏠 HOUSE PRICE PREDICTION v4.0 — WITH RECOMMENDATIONS")
    print("="*80)
    print(f"✅ Model: {type(model).__name__ if model else 'Not loaded'}")
    print(f"✅ User fields: {len(USER_INPUT_FEATURES)} high-impact features")
    print(f"✅ Location types: {len(LOCATION_TYPES)} universal categories")
    print(f"✅ Model features: {len(feature_names)} (auto-filled)")
    print(f"ℹ️  Kitchen Quality fixed at: Average (3) — hidden from UI")
    print(f"ℹ️  Stories fixed at: 2 — hidden from UI")
    print("="*80)
    print("⭐ Price Range, Market Insight & Suggestions enabled!")
    print("="*80)
    print("🌐 http://127.0.0.1:8000")
    print("="*80 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )