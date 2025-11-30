import requests
import json

# Test data with default values from dataset
test_data = {
    "category": "bed_bath_table",
    "cogs": 45.0,
    "freight": 15.0,
    "comp1": 120.0,
    "comp2": 150.0,
    "comp3": 100.0,
    "score": 4.2,
    "customers": 50
}

# API endpoint
api_url = "http://127.0.0.1:8000/optimize_price"

try:
    # Send POST request
    response = requests.post(api_url, json=test_data)
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        
        # Print results in a clean, readable format
        print("\n" + "="*50)
        print("FASHIONISTA PRICE OPTIMIZATION RESULTS")
        print("="*50)
        print(f"Optimal Price:    ${result['optimal_price']:.2f}")
        print(f"Max Profit:       ${result['max_profit']:.2f}")
        print(f"Predicted Qty:    {result['predicted_qty']:.2f} units")
        print("="*50 + "\n")
        
    else:
        print(f"Error: API returned status code {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API.")
    print("Make sure the API server is running on http://127.0.0.1:8000")
except Exception as e:
    print(f"Error: {str(e)}")
