# 🏠 AI House Price Recommendation System

A full-stack Machine Learning web application that predicts house prices and provides intelligent price recommendations using advanced ML models.

---

## 🚀 Features

* 🔮 Predict house price based on input features
* 📊 Show recommended price range
* 💡 Provide market insights (Low / Medium / High)
* 📌 Smart suggestions for buyers
* ⚡ Real-time prediction using FastAPI
* 🎨 Modern responsive UI (HTML, CSS, JS)

---

## 🧠 Machine Learning

* Model Used: **GradientBoostingRegressor**
* Dataset: **Ames Housing Dataset**
* Features: 15+ important housing features
* Evaluation Metrics:

  * MAE, MSE, RMSE
  * R² Score

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Frontend:** HTML, CSS, JavaScript
* **ML Libraries:** scikit-learn, pandas, numpy
* **Deployment:** Render

---

## 📂 Project Structure

```
project/
│
├── main.py
├── best_model.pkl
├── feature_names.txt
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
```

---

## ⚙️ Installation & Run Locally

### 1. Clone the repository

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the application

```
uvicorn main:app --reload
```

### 4. Open in browser

```
http://127.0.0.1:8000
```

---

## 🌐 Deployment

This project is deployed using **Render**.

Steps:

* Push code to GitHub
* Connect repo to Render
* Add build and start commands
* Deploy

---

## 📊 How It Works

1. User enters house details
2. Backend loads trained ML model
3. Model predicts house price
4. System generates:

   * Estimated price
   * Recommended price range
   * Market insight
   * Suggestions

---

## 🎯 Use Cases

* Property price estimation
* Real estate decision support
* ML-based recommendation systems
* Educational ML projects

---

## 📌 Future Improvements

* Add more features (location-based pricing)
* Improve model accuracy with tuning
* Add user login system
* Deploy mobile app version

---

## 👨‍💻 Author

**Nikhil Sajan**

---

## ⭐ Acknowledgment

* Ames Housing Dataset
* Scikit-learn Documentation
* FastAPI Framework

---

## 📜 License

This project is for educational purposes.
