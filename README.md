# 👗 Fashionista Price Optimizer

A machine learning-powered price optimization system for fashion and retail products. Uses Ridge Regression to analyze demand patterns and recommend optimal pricing strategies based on product characteristics, competitor prices, and market conditions.

## 🎯 Features

- **AI-Powered Price Optimization**: Ridge Regression model (R² = 0.9425) predicts optimal prices
- **Demand Analysis**: Estimates unit demand based on pricing and product metrics
- **Competitive Intelligence**: Analyzes competitor prices to position products strategically
- **Profit Maximization**: Recommends prices that maximize profit margins
- **Interactive UI**: Streamlit-based web interface for easy price analysis
- **REST API**: FastAPI backend for programmatic access

## 📊 Model Performance

- **R² Score**: 0.9425 - High accuracy in demand prediction
- **Features Analyzed**:
  - Unit price (negative correlation)
  - Product rating/score
  - Customer count
  - Competitor prices (average, min, max)
  - Product category
  - Cost of goods sold (COGS)
  - Freight costs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HiNacho/fashionista-price-optimizer.git
cd fashionista-price-optimizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: Streamlit Web Interface**
```bash
streamlit run app.py
```
Access at: http://localhost:8501

**Option 2: FastAPI Backend**
```bash
python api.py
```
API runs at: http://localhost:8000

**Option 3: Combined (Web + API)**
```bash
# Terminal 1: Start API
python api.py

# Terminal 2: Start Streamlit
streamlit run app.py
```

## 📈 Usage

1. **Open the Streamlit app** at http://localhost:8501
2. **Enter product details**:
   - Select product category
   - Input COGS and freight costs
   - Enter competitor prices
   - Set product rating and customer count
3. **Click "Optimize Price Now"**
4. **View recommendations**:
   - Optimal price point
   - Maximum profit potential
   - Predicted demand quantity
   - Additional market insights

## 🗂️ Project Structure

```
.
├── app.py                 # Streamlit web interface
├── api.py                 # FastAPI backend server
├── price_opt.ipynb        # Jupyter notebook with model development
├── retail_price.csv       # Training dataset
├── requirements.txt       # Python dependencies
├── test_api.py           # API testing script
└── README.md             # This file
```

## 🔧 API Endpoints

### GET /
Returns model information and R² score.

### POST /optimize_price
**Request Body:**
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
  "optimal_price": 128.45,
  "max_profit": 3445.67,
  "predicted_qty": 26.8,
  "r_squared": 0.9425
}
```

## 📦 Dependencies

- **streamlit**: Web UI framework
- **fastapi**: REST API framework
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning
- **numpy**: Numerical computing
- **requests**: HTTP client
- **uvicorn**: ASGI server

See `requirements.txt` for complete list and versions.

## 🧪 Testing

Run the test script to verify API functionality:
```bash
python test_api.py
```

## 📝 Notes

- The model is trained on retail fashion product data
- Supports 9 product categories
- Prices are optimized for profit maximization
- All monetary values in USD
- Demand predictions include confidence intervals

## 🚢 Deployment

### Streamlit Cloud
Push to GitHub and deploy via [Streamlit Cloud](https://streamlit.io/cloud)

### Docker
Create a Dockerfile and deploy to your preferred container platform.

## 📄 License

This project is available under the MIT License.

## 👤 Author

**HiNacho** - Price Optimization Development

---

**Last Updated**: November 30, 2025
