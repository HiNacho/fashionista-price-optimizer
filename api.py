from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import math

# Model Coefficients (extracted from trained Ridge model in the notebook)
MODEL_COEFFICIENTS = {
    'intercept': 14.853360488798305,
    'unit_price': -0.28587598812465354,
    'product_score': 0.5438133598425678,
    'customers': 7.723945321787855,
    'comp_1': -1.288367484270411,
    'comp_2': 0.49889132632829736,
    'comp_3': 0.5629239228716054,
    'price_ratio_1': -0.3809751653771346,
    'price_diff_1': 0.7088265708288127,
    'price_ratio_2': -0.5421674135298935,
    'price_diff_2': -0.7577806489555758,
    'price_ratio_3': -0.18554514689308288,
    'price_diff_3': -0.8602668746696169,
    # Category dummies (note: bed_bath_table was the dropped baseline)
    'cat_bed_bath_table': 0.0,
    'cat_computers_accessories': 0.1993419622795043,
    'cat_consoles_games': 0.3669261150230482,
    'cat_cool_stuff': -2.0803094819519266,
    'cat_furniture_decor': 1.5619133127902447,
    'cat_garden_tools': -2.4678555653046086,
    'cat_health_beauty': -1.3583504702650084,
    'cat_perfumery': -0.2515015610223594,
    'cat_watches_gifts': -2.906045082275523,
}

# Scaler Parameters (means and stds extracted from the training scaler)
SCALER_PARAMS = {
    'unit_price': {'mean': 99.44523713731162, 'std': 62.97369568592211},
    'product_score': {'mean': 4.080448065173115, 'std': 0.22488875469238448},
    'customers': {'mean': 80.27494908350306, 'std': 63.53323747857187},
    'comp_1': {'mean': 82.0746224177393, 'std': 45.07783534917797},
    'comp_2': {'mean': 94.22953593456212, 'std': 47.74317009020924},
    'comp_3': {'mean': 87.62979113309574, 'std': 50.83361087506544},
    'price_ratio_1': {'mean': 1.5230047207087019, 'std': 1.760434580900736},
    'price_diff_1': {'mean': 17.370614719572302, 'std': 56.53590242567708},
    'price_ratio_2': {'mean': 1.1384233344948709, 'std': 0.6379685588869871},
    'price_diff_2': {'mean': 5.215701202749489, 'std': 55.18921733767781},
    'price_ratio_3': {'mean': 1.2823692803405475, 'std': 0.879648952164473},
    'price_diff_3': {'mean': 11.815446004215886, 'std': 54.19030361420513},
}

app = FastAPI(title="Fashionista Price Optimization API")


class PriceOptimizationInput(BaseModel):
    """Input model for price optimization request"""
    category: str
    cogs: float
    freight: float
    comp1: float
    comp2: float
    comp3: float
    score: float
    customers: float


def normalize_feature(value: float, feature_name: str) -> float:
    """Normalize a feature using the scaler parameters"""
    params = SCALER_PARAMS[feature_name]
    return (value - params['mean']) / params['std']


def predict_demand(price: float, input_values: PriceOptimizationInput) -> float:
    """
    Predict demand (quantity) using the Ridge Regression model.
    
    This function:
    1. Performs feature engineering (ratios and differences)
    2. Normalizes features using scaler parameters
    3. Calculates the prediction using model coefficients
    4. Clamps the result at a minimum of 0.1
    """
    # Feature engineering: Calculate ratios and differences
    price_ratio_1 = price / input_values.comp1 if input_values.comp1 > 0 else 1.0
    price_diff_1 = price - input_values.comp1
    
    price_ratio_2 = price / input_values.comp2 if input_values.comp2 > 0 else 1.0
    price_diff_2 = price - input_values.comp2
    
    price_ratio_3 = price / input_values.comp3 if input_values.comp3 > 0 else 1.0
    price_diff_3 = price - input_values.comp3
    
    # Normalize features
    normalized_price = normalize_feature(price, 'unit_price')
    normalized_score = normalize_feature(input_values.score, 'product_score')
    normalized_customers = normalize_feature(input_values.customers, 'customers')
    normalized_comp1 = normalize_feature(input_values.comp1, 'comp_1')
    normalized_comp2 = normalize_feature(input_values.comp2, 'comp_2')
    normalized_comp3 = normalize_feature(input_values.comp3, 'comp_3')
    normalized_price_ratio_1 = normalize_feature(price_ratio_1, 'price_ratio_1')
    normalized_price_diff_1 = normalize_feature(price_diff_1, 'price_diff_1')
    normalized_price_ratio_2 = normalize_feature(price_ratio_2, 'price_ratio_2')
    normalized_price_diff_2 = normalize_feature(price_diff_2, 'price_diff_2')
    normalized_price_ratio_3 = normalize_feature(price_ratio_3, 'price_ratio_3')
    normalized_price_diff_3 = normalize_feature(price_diff_3, 'price_diff_3')
    
    # Calculate category one-hot encoding
    cat_bed_bath_table = 1.0 if (
        input_values.category.lower() == 'bed_bath_table'
    ) else 0.0
    cat_computers_accessories = 1.0 if (
        input_values.category.lower() == 'computers_accessories'
    ) else 0.0
    cat_consoles_games = 1.0 if (
        input_values.category.lower() == 'consoles_games'
    ) else 0.0
    cat_cool_stuff = 1.0 if (
        input_values.category.lower() == 'cool_stuff'
    ) else 0.0
    cat_furniture_decor = 1.0 if (
        input_values.category.lower() == 'furniture_decor'
    ) else 0.0
    cat_garden_tools = 1.0 if (
        input_values.category.lower() == 'garden_tools'
    ) else 0.0
    cat_health_beauty = 1.0 if (
        input_values.category.lower() == 'health_beauty'
    ) else 0.0
    cat_perfumery = 1.0 if (
        input_values.category.lower() == 'perfumery'
    ) else 0.0
    cat_watches_gifts = 1.0 if (
        input_values.category.lower() == 'watches_gifts'
    ) else 0.0
    
    # Model prediction using Ridge Regression coefficients
    prediction = (
        MODEL_COEFFICIENTS['intercept'] +
        MODEL_COEFFICIENTS['unit_price'] * normalized_price +
        MODEL_COEFFICIENTS['product_score'] * normalized_score +
        MODEL_COEFFICIENTS['customers'] * normalized_customers +
        MODEL_COEFFICIENTS['comp_1'] * normalized_comp1 +
        MODEL_COEFFICIENTS['comp_2'] * normalized_comp2 +
        MODEL_COEFFICIENTS['comp_3'] * normalized_comp3 +
        MODEL_COEFFICIENTS['price_ratio_1'] * normalized_price_ratio_1 +
        MODEL_COEFFICIENTS['price_diff_1'] * normalized_price_diff_1 +
        MODEL_COEFFICIENTS['price_ratio_2'] * normalized_price_ratio_2 +
        MODEL_COEFFICIENTS['price_diff_2'] * normalized_price_diff_2 +
        MODEL_COEFFICIENTS['price_ratio_3'] * normalized_price_ratio_3 +
        MODEL_COEFFICIENTS['price_diff_3'] * normalized_price_diff_3 +
        MODEL_COEFFICIENTS['cat_bed_bath_table'] * (
            cat_bed_bath_table
        ) +
        MODEL_COEFFICIENTS['cat_computers_accessories'] * (
            cat_computers_accessories
        ) +
        MODEL_COEFFICIENTS['cat_consoles_games'] * (
            cat_consoles_games
        ) +
        MODEL_COEFFICIENTS['cat_cool_stuff'] * cat_cool_stuff +
        MODEL_COEFFICIENTS['cat_furniture_decor'] * (
            cat_furniture_decor
        ) +
        MODEL_COEFFICIENTS['cat_garden_tools'] * cat_garden_tools +
        MODEL_COEFFICIENTS['cat_health_beauty'] * cat_health_beauty +
        MODEL_COEFFICIENTS['cat_perfumery'] * cat_perfumery +
        MODEL_COEFFICIENTS['cat_watches_gifts'] * cat_watches_gifts
    )
    
    # Clamp at minimum of 0.1
    qty = max(0.1, prediction)
    
    return qty


@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Fashionista Price Optimization API",
        "description": "Ridge Regression Demand Model for price optimization",
        "r_squared": 0.9425,
        "endpoints": {
            "POST /optimize_price": "Calculate optimal price to maximize profit",
            "GET /optimize_price": "Get API documentation",
            "GET /": "This endpoint"
        }
    }


@app.get("/optimize_price")
async def optimize_price_info():
    """Get information about the optimize_price endpoint"""
    return {
        "endpoint": "/optimize_price",
        "method": "POST",
        "description": "Optimize product price to maximize profit",
        "required_parameters": {
            "category": "Product category (apparel, accessories, footwear)",
            "cogs": "Cost of goods sold (float)",
            "freight": "Freight cost (float)",
            "comp1": "Competitor 1 price (float)",
            "comp2": "Competitor 2 price (float)",
            "comp3": "Competitor 3 price (float)",
            "score": "Product score/rating (float)",
            "customers": "Number of customers (integer)"
        },
        "example": {
            "category": "apparel",
            "cogs": 45.0,
            "freight": 15.0,
            "comp1": 120.0,
            "comp2": 150.0,
            "comp3": 100.0,
            "score": 4.2,
            "customers": 50
        }
    }


@app.post("/optimize_price")
async def optimize_price(input_data: PriceOptimizationInput):
    """
    Optimize price to maximize profit.
    
    Iterates through a price range and calculates profit for each price point.
    Returns the optimal price that maximizes profit.
    """
    # Calculate price range
    min_price = input_data.cogs + input_data.freight + 10
    max_price = max(input_data.comp1, input_data.comp2, input_data.comp3) * 2
    step = 0.50
    
    optimal_price = min_price
    max_profit = -float('inf')
    optimal_qty = 0.0
    
    # Optimization loop
    price = min_price
    while price <= max_price:
        # Predict demand for this price
        try:
            qty = predict_demand(price, input_data)
        except Exception:
            # skip this price if prediction fails
            price += step
            continue

        # Calculate profit
        profit = (price * qty) - (input_data.cogs * qty) - (input_data.freight * qty)

        # Skip if values are not finite (avoid JSON serialization errors)
        if not (math.isfinite(qty) and math.isfinite(profit)):
            price += step
            continue

        # Update optimal values if this is better
        if profit > max_profit:
            max_profit = profit
            optimal_price = price
            optimal_qty = qty

        price += step
    
    # Ensure returned values are finite and JSON serializable
    if not math.isfinite(max_profit):
        return {"error": "Unable to compute optimal price (no valid price points)."}

    return {
        "optimal_price": float(round(optimal_price, 2)),
        "max_profit": float(round(max_profit, 2)),
        "predicted_qty": float(round(optimal_qty, 2))
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
