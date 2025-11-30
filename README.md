# 💰 Fashionista Price Optimization

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.104+-00a86b?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-ff4b4b?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-f7931e?logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**Find the profit-maximizing price for your products in seconds using ML** 🎯

[📊 Quick Start](#-quick-start) • [🚀 Deployment](#-deployment) • [📚 API Docs](#-api-endpoints) • [🐳 Docker](#-docker-deployment)

</div>

---

## ✨ Features at a Glance

| Feature | Description |
|---------|-------------|
| 🤖 **ML Model** | Ridge Regression demand forecaster (R²=0.9425) trained on real retail data |
| ⚡ **FastAPI Backend** | Lightweight REST API with automatic docs & validation |
| 🎨 **Streamlit UI** | Interactive dashboard for instant price optimization demos |
| 🛡️ **Production Ready** | Edge-case handling, error management, defensive checks |
| 🐳 **Containerized** | Docker & Docker Compose for one-command deployment |
| 🌐 **Shareable** | ngrok integration for instant client demos without hosting |
| 📦 **Complete Stack** | Training notebook + model coefficients + API + UI all included |

---

## 📋 What It Does

This tool **solves the pricing problem**: given product characteristics (COGS, competitor prices, customer metrics), it finds the price that **maximizes profit** using a pre-trained machine learning model.

**Example workflow:**
1. Enter product details (category, cost, competitor prices, customer metrics)
2. Click "Optimize Price"
3. Get instant recommendation: "Set price to **$275.50** for **$1,445.77 max profit**"

Perfect for retail pricing strategy, dynamic pricing, or pricing research demos!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Browser)                            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         ▼
    ┌────────────────────────────────────────┐
    │      Streamlit Dashboard (8501)         │
    │  • Interactive form for product inputs  │
    │  • Beautiful results cards & metrics    │
    │  • Real-time optimization visualization │
    └────────────┬─────────────────────────────┘
                 │ REST API calls (JSON)
                 ▼
    ┌────────────────────────────────────────┐
    │    FastAPI Server (8001)                │
    │  • /optimize_price POST endpoint        │
    │  • Feature engineering                  │
    │  • Ridge Regression prediction          │
    │  • Profit maximization algorithm        │
    └────────────┬─────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────────┐
    │    ML Model (Ridge Regression)          │
    │  • 38 features                          │
    │  • Embedded coefficients                │
    │  • Demand forecasting                   │
    └────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Local)

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### 1️⃣ Clone & Install

```bash
git clone https://github.com/HiNacho/fashionista-price-optimizer.git
cd fashionista-price-optimizer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Start the API

```bash
uvicorn api:app --host 127.0.0.1 --port 8001 --reload
```

Expected output:
```
Uvicorn running on http://127.0.0.1:8001
```

### 3️⃣ Start Streamlit (in a new terminal)

```bash
source .venv/bin/activate  # Activate venv again
streamlit run app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 4️⃣ Open Dashboard

Visit 🔗 **http://localhost:8501** and start optimizing prices!

---

## 📚 API Endpoints

### Base URL
```
http://127.0.0.1:8001
```

### Endpoints

#### GET `/`
Info about the API
```bash
curl http://127.0.0.1:8001/
```

**Response:**
```json
{
  "message": "Fashionista Price Optimization API",
  "description": "Ridge Regression Demand Model for price optimization",
  "r_squared": 0.9425,
  "endpoints": {
    "POST /optimize_price": "Calculate optimal price to maximize profit",
    "GET /optimize_price": "Get API documentation"
  }
}
```

#### POST `/optimize_price`
Calculate optimal price for maximum profit

**Request:**
```json
{
  "category": "bed_bath_table",
  "cogs": 45.0,
  "freight": 15.0,
  "comp1": 120.0,
  "comp2": 150.0,
  "comp3": 100.0,
  "score": 4.2,
  "customers": 50
}
```

**Response:**
```json
{
  "optimal_price": 275.5,
  "max_profit": 1445.77,
  "predicted_qty": 6.71
}
```

### Supported Categories

```
bed_bath_table
computers_accessories
consoles_games
cool_stuff
furniture_decor
garden_tools
health_beauty
perfumery
watches_gifts
```

### Python Example

```python
import requests

payload = {
    'category': 'bed_bath_table',
    'cogs': 45,
    'freight': 15,
    'comp1': 120,
    'comp2': 150,
    'comp3': 100,
    'score': 4.2,
    'customers': 50
}

response = requests.post(
    'http://127.0.0.1:8001/optimize_price',
    json=payload,
    timeout=10
)

print(f"Optimal Price: ${response.json()['optimal_price']}")
print(f"Max Profit: ${response.json()['max_profit']}")
print(f"Predicted Qty: {response.json()['predicted_qty']:.2f} units")
```

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
docker-compose up --build
```

This starts both services:
- **API:** http://localhost:8001
- **Streamlit:** http://localhost:8501

### Manual Docker Build

```bash
# Build image
docker build -t fashionista-api .

# Run API
docker run -p 8001:8001 fashionista-api

# Run Streamlit (different terminal)
docker run -p 8501:8501 \
  fashionista-api \
  streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

For detailed Docker info, see **[DOCKER.md](DOCKER.md)**.

---

## 🌐 Share with Clients (ngrok)

Want to demo without hosting? Use ngrok to expose locally:

### 1. Install ngrok

```bash
brew install --cask ngrok  # macOS
# or download from https://ngrok.com
```

### 2. Start Streamlit locally

```bash
streamlit run app.py
```

### 3. Expose with ngrok

```bash
ngrok http 8501
```

### 4. Share the public URL

Copy the `https://...ngrok.io` URL and send to your client. They can access the demo instantly!

⚠️ **Note:** ngrok free tier has limits. For production sharing, consider Streamlit Cloud, Heroku, or your own hosting.

---

## 📊 Model Details

### Training Pipeline

- **Algorithm:** Ridge Regression (alpha=20)
- **Features:** 38 (numeric + one-hot encoded categories)
- **Train Set:** Data before May 2018
- **Test Set:** Data from May 2018 onwards
- **R² Score:** 0.9425 (excellent fit!)

### Feature Engineering

The API automatically computes:
- Price ratios vs competitors
- Price differences vs competitors
- Customer-weighted demand signals
- Category embeddings

See **[price_opt.ipynb](price_opt.ipynb)** for the full training pipeline.

---

## 📁 Project Structure

```
fashionista-price-optimizer/
│
├── api.py                    # FastAPI server with optimization endpoint
├── app.py                    # Streamlit dashboard
├── price_opt.ipynb           # Jupyter notebook: model training pipeline
├── test_api.py               # Simple API test script
├── retail_price.csv          # Dataset for training
├── requirements.txt          # Python dependencies
│
├── Dockerfile                # Container image definition
├── docker-compose.yml        # Multi-service orchestration
├── .dockerignore              # Files to exclude from Docker image
│
├── README.md                 # This file
├── DOCKER.md                 # Docker deployment guide
├── GITHUB_DEPLOY.md          # GitHub setup instructions
│
└── .gitignore                # Git ignore rules
```

---

## 🛠️ Tech Stack

<div align="center">

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.104+ |
| **Frontend** | Streamlit | 1.50+ |
| **Runtime** | Python | 3.9 |
| **ML** | scikit-learn | 1.6+ |
| **Data** | pandas | 2.3+ |
| **Containerization** | Docker | Latest |
| **Server** | uvicorn | 0.38+ |

</div>

---

## 🧪 Testing

### Quick API Test

```bash
python test_api.py
```

### Test with curl

```bash
curl -X POST http://127.0.0.1:8001/optimize_price \
  -H "Content-Type: application/json" \
  -d '{
    "category": "bed_bath_table",
    "cogs": 45,
    "freight": 15,
    "comp1": 120,
    "comp2": 150,
    "comp3": 100,
    "score": 4.2,
    "customers": 50
  }'
```

### Edge Cases Tested

- ✅ Normal pricing (positive costs)
- ✅ Zero cost (COGS + freight = 0)
- ✅ Very low costs (< $1)
- ✅ High demand scenarios
- ✅ Low product scores
- ✅ Non-finite value handling (NaN/inf skipping)

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8001 in use** | `lsof -i :8001 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| **Port 8501 in use** | `lsof -i :8501 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| **Streamlit can't reach API** | Ensure API is running on 127.0.0.1:8001; check firewall |
| **Docker build fails** | Run `docker system prune` to clean up; rebuild with `--no-cache` |
| **Requirements install fails** | Try `pip install --upgrade pip setuptools` first |
| **"Repository not found" on git push** | Double-check username in git remote URL |

---

## 📈 Use Cases

✅ **E-commerce pricing:** Dynamically optimize product prices based on demand  
✅ **Retail strategy:** Test pricing scenarios before deploying  
✅ **Pricing research:** Demonstrate ML-based pricing to stakeholders  
✅ **Competitor analysis:** Benchmark against competitor prices  
✅ **Client demos:** Beautiful UI for pitching ML solutions  

---

## 🎓 Learning Resources

- **FastAPI:** [Official Docs](https://fastapi.tiangolo.com/)
- **Streamlit:** [Official Docs](https://docs.streamlit.io/)
- **scikit-learn:** [Ridge Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html)
- **Docker:** [Official Docs](https://docs.docker.com/)

---

## 🤝 Contributing

Found a bug? Have a feature idea? Pull requests welcome!

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## 📧 Contact & Support

- **GitHub Issues:** [Report a bug](https://github.com/HiNacho/fashionista-price-optimizer/issues)
- **Email:** hellotovictor@gmail.com
- **Portfolio:** Check out more projects on [GitHub](https://github.com/HiNacho)

---

<div align="center">

### 🌟 Made with ❤️ using Python, FastAPI & Streamlit

**If you found this useful, please give it a ⭐ Star!**

</div>
