# 🏠 AI House Price Predictor - Full Stack Web Application

A modern, professional full-stack web application for predicting house prices using machine learning. Built with FastAPI backend and vanilla JavaScript frontend.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-teal.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

## 🌟 Features

- ✨ **Modern UI/UX** - Responsive design with smooth animations
- 🚀 **Real-time Predictions** - Instant price predictions using pre-trained ML model
- 📊 **Dynamic Form Generation** - Automatically generates input fields from model features
- 🎨 **Beautiful Gradient Design** - Professional gradient backgrounds and card layouts
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast Performance** - Predictions in under 1 second
- 🔒 **Error Handling** - Comprehensive error handling and validation
- 🎯 **RESTful API** - Clean API endpoints with FastAPI

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.8 or higher** installed
- **Trained ML model** saved as `best_model.pkl`
- **Feature names** file (either `feature_names.pkl` or `feature_names.txt`)
- **Optional**: `scaler.pkl` for feature scaling

## 📁 Project Structure

```
house_price_app/
│
├── main.py                 # FastAPI backend application
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── saved_models/          # Directory for trained models
│   ├── best_model.pkl     # Your trained model
│   ├── scaler.pkl         # Feature scaler (optional)
│   └── feature_names.pkl  # Feature names
│
├── templates/             # HTML templates
│   └── index.html         # Main frontend page
│
└── static/                # Static files
    ├── style.css          # Stylesheet
    └── script.js          # JavaScript functionality
```

## 🚀 Installation & Setup

### Step 1: Clone/Download the Project

```bash
# If you have this as a repository
git clone <repository-url>
cd house_price_app

# Or simply navigate to the project directory
cd house_price_app
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Add Your Trained Model

Place your trained model files in the project:

```
house_price_app/
├── saved_models/
│   ├── best_model.pkl       # ✅ Required
│   ├── scaler.pkl           # ⚠️ Recommended
│   └── feature_names.pkl    # ✅ Required
```

**Alternative locations** (if files are in root):
```
house_price_app/
├── best_model.pkl
├── scaler.pkl
└── feature_names.txt or feature_names.pkl
```

The application will automatically detect files in either location.

## 🎮 Running the Application

### Method 1: Using Uvicorn (Recommended)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Direct Python Execution

```bash
python main.py
```

### Method 3: Production Mode (No Auto-reload)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 Accessing the Application

Once the server is running, you can access:

- **Web Application**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 📡 API Endpoints

### 1. Get Features
```http
GET /features
```
Returns list of all features and their metadata.

**Response:**
```json
{
  "features": ["OverallQual", "GrLivArea", ...],
  "feature_info": {...},
  "total_features": 70
}
```

### 2. Make Prediction
```http
POST /predict
```

**Request Body:**
```json
{
  "features": {
    "OverallQual": 7,
    "GrLivArea": 1500,
    "TotalBsmtSF": 1000,
    ...
  }
}
```

**Response:**
```json
{
  "predicted_price": 250000.50,
  "formatted_price": "$250,000.50",
  "model_name": "GradientBoostingRegressor",
  "confidence": "High"
}
```

### 3. Model Info
```http
GET /model-info
```
Returns information about the loaded model.

### 4. Health Check
```http
GET /health
```
Check if the application is running and model is loaded.

## 💻 Usage Guide

### Web Interface

1. **Open the Application**
   - Navigate to http://127.0.0.1:8000 in your browser

2. **Fill in Features**
   - The form dynamically generates input fields based on your model's features
   - Each field has default values and validation

3. **Predict Price**
   - Click "Predict Price" button
   - Wait for the prediction (typically < 1 second)

4. **View Results**
   - See the predicted price with formatting
   - View model confidence and details

5. **Make Another Prediction**
   - Click "Predict Another Price" to reset the form

### Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Submit form
- **Escape**: Reset form (when result is visible)

## 🎨 Customization

### Change Color Scheme

Edit `static/style.css`:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change to your preferred gradient */
}
```

### Modify Feature Metadata

Edit `main.py` in the `create_feature_info()` function to customize how features are displayed.

### Add Custom Validation

Edit `static/script.js` in the `validateInput()` function.

## 🔧 Troubleshooting

### Issue: "Model file not found"

**Solution:**
- Ensure `best_model.pkl` exists in either `saved_models/` or root directory
- Check file name spelling (case-sensitive)

### Issue: "Features file not found"

**Solution:**
- Ensure you have either `feature_names.pkl` or `feature_names.txt`
- Place it in `saved_models/` directory

### Issue: Port already in use

**Solution:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Issue: CORS errors

**Solution:**
- The app has CORS enabled by default
- If issues persist, check browser console for specific errors

### Issue: Prediction errors

**Solution:**
- Ensure all features match the training data
- Check that scaler.pkl is present if used during training
- Verify input data types (all should be numeric)

## 📊 Model Requirements

Your trained model must:

1. Be saved using `joblib.dump(model, 'best_model.pkl')`
2. Have a `predict()` method that accepts numpy arrays
3. Have corresponding feature names saved
4. Optionally have a scaler if features were scaled during training

## 🚀 Deployment

### Deploy to Production

For production deployment, consider:

1. **Use Gunicorn with Uvicorn workers:**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **Set up environment variables:**
```bash
export MODEL_PATH="/path/to/your/model.pkl"
```

3. **Use a reverse proxy (Nginx/Apache)**

4. **Enable HTTPS with SSL certificate**

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t house-price-predictor .
docker run -p 8000:8000 house-price-predictor
```

## 📈 Performance Optimization

- **Enable caching** for model predictions
- **Use async/await** for I/O operations
- **Implement request batching** for multiple predictions
- **Add database** for storing prediction history
- **Use CDN** for static files in production

## 🛡️ Security Considerations

- ✅ Input validation implemented
- ✅ CORS configured
- ⚠️ Add rate limiting for production
- ⚠️ Implement authentication if needed
- ⚠️ Sanitize user inputs
- ⚠️ Use HTTPS in production

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Open an issue on GitHub

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Store prediction history
- [ ] Add data visualization charts
- [ ] Implement model comparison
- [ ] Add export to PDF functionality
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Real-time model updates

---

**Built with ❤️ using FastAPI and Modern Web Technologies**

**Version:** 1.0.0  
**Last Updated:** 2024
