import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class IndiaHousePricePredictor:
    def __init__(self):
        self.model = None
        self.preprocessors = None
        self.models_dir = Path("models")
        self.load_model()
    
    def load_model(self):
        model_path = self.models_dir / 'india_house_price_model.pkl'
        preprocessor_path = self.models_dir / 'india_preprocessors.pkl'
        
        if model_path.exists():
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded: {type(self.model).__name__}")
        else:
            logger.warning(f" Model not found at {model_path}")
        
        if preprocessor_path.exists():
            self.preprocessors = joblib.load(preprocessor_path)
            logger.info(f" Preprocessors loaded")
    
    def predict(self, features):
        if self.model is None:
            return self.fallback_prediction(features)
        
        df = pd.DataFrame([features])
        
        if 'state' in df.columns and 'state' in self.preprocessors.get('label_encoders', {}):
            le = self.preprocessors['label_encoders']['state']
            df['state_encoded'] = le.transform(df['state'])
            df.drop('state', axis=1, inplace=True)
        
        
        if 'area_type' in df.columns:
            area_mapping = {'Rich': 2, 'Medium': 1, 'Poor': 0}
            df['area_type_encoded'] = df['area_type'].map(area_mapping)
            df.drop('area_type', axis=1, inplace=True)
        
    
        if 'age' in df.columns:
            df['is_new'] = (df['age'] < 5).astype(int)
            df['is_old'] = (df['age'] > 20).astype(int)
        
        df = df.select_dtypes(include=[np.number])
        
        expected_features = self.preprocessors.get('feature_names', [])
        for feature in expected_features:
            if feature not in df.columns:
                df[feature] = 0
        
    
        df = df[expected_features]
        

        if 'scaler' in self.preprocessors:
            X_scaled = self.preprocessors['scaler'].transform(df)
        else:
            X_scaled = df.values
        

        price = self.model.predict(X_scaled)[0]
        return float(price)
    
    def fallback_prediction(self, features):
        sqft = features.get('sqft', 1000)
        bhk = features.get('bhk', 2)
        area_type = features.get('area_type', 'Medium')
        state = features.get('state', 'Maharashtra')
        
    
        base_prices = {
            'Maharashtra': 15000,
            'Delhi': 14000,
            'Karnataka': 10000,
            'Tamil Nadu': 8000,
            'West Bengal': 7000,
            'Telangana': 9000,
            'Gujarat': 7500
        }
        
        price_per_sqft = base_prices.get(state, 8000)
        
        
        area_multiplier = {'Rich': 1.5, 'Medium': 1.0, 'Poor': 0.7}
        area_factor = area_multiplier.get(area_type, 1.0)
        
    
        bhk_multiplier = {1: 0.8, 2: 1.0, 3: 1.2, 4: 1.4, 5: 1.6}
        bhk_factor = bhk_multiplier.get(bhk, 1.0)
        
        price = sqft * price_per_sqft * area_factor * bhk_factor
        return float(price)

if __name__ == "__main__":
    predictor = IndiaHousePricePredictor()
    
    
    test_house = {
        'state': 'Maharashtra',
        'sqft': 1200,
        'bhk': 3,
        'area_type': 'Medium',
        'population': 15000,
        'age': 10
    }
    
    price = predictor.predict(test_house)
    print(f"\n Test House:")
    print(f"   State: {test_house['state']}")
    print(f"   Sqft: {test_house['sqft']}")
    print(f"   BHK: {test_house['bhk']}")
    print(f"   Area Type: {test_house['area_type']}")
    print(f"\n Predicted Price: ₹{price:,.2f}")