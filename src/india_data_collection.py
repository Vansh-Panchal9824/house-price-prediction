import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndiaHouseDataCollector:
    def __init__(self):
        self.data = None
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_india_data(self, n_samples=3000):
        
        np.random.seed(42)
        
        
        states = {
            'Maharashtra': {'multiplier': 2.5, 'base_rate': 15000},
            'Delhi': {'multiplier': 2.3, 'base_rate': 14000},
            'Karnataka': {'multiplier': 2.0, 'base_rate': 10000},
            'Tamil Nadu': {'multiplier': 1.6, 'base_rate': 8000},
            'West Bengal': {'multiplier': 1.4, 'base_rate': 7000},
            'Telangana': {'multiplier': 1.8, 'base_rate': 9000},
            'Gujarat': {'multiplier': 1.5, 'base_rate': 7500},
            'Uttar Pradesh': {'multiplier': 1.2, 'base_rate': 6000},
            'Rajasthan': {'multiplier': 1.3, 'base_rate': 6500},
            'Kerala': {'multiplier': 1.4, 'base_rate': 8000},
            'Punjab': {'multiplier': 1.3, 'base_rate': 7000},
            'Haryana': {'multiplier': 1.5, 'base_rate': 9000}
        }
        
        
        area_types = {
            'Rich': 1.5,
            'Medium': 1.0,
            'Poor': 0.7
        }
        

        bhk_multiplier = {1: 0.7, 2: 0.9, 3: 1.0, 4: 1.2, 5: 1.4}
        
        data = []
        
        for _ in range(n_samples):
            
            state = np.random.choice(list(states.keys()))
            state_data = states[state]
            
            
            area_type = np.random.choice(list(area_types.keys()))
            area_multiplier = area_types[area_type]
            
            
            sqft = np.random.randint(300, 5000)
            
            
            bhk = np.random.randint(1, 6)
            bhk_factor = bhk_multiplier[bhk]
            
            
            population = np.random.randint(1000, 50000)
            
            
            age = np.random.randint(0, 41)
            
            
            if age < 5:
                age_multiplier = 1.2
            elif age < 10:
                age_multiplier = 1.1
            elif age < 20:
                age_multiplier = 1.0
            elif age < 30:
                age_multiplier = 0.9
            else:
                age_multiplier = 0.8
            
            
            price = (
                sqft * state_data['base_rate'] *
                state_data['multiplier'] *
                area_multiplier *
                bhk_factor *
                age_multiplier
            )
            
        
            population_factor = 1 + (population / 100000)
            price = price * population_factor
            
            
            price = price * np.random.uniform(0.9, 1.1)
            
            data.append({
                'country': 'India',
                'state': state,
                'sqft': sqft,
                'bhk': bhk,
                'area_type': area_type,
                'population': population,
                'age': age,
                'price': int(price)
            })
        
        self.data = pd.DataFrame(data)
        logger.info(f" Generated {n_samples} India house records")
        return self.data
    
    def save_data(self, filename='india_housing_data.csv'):
        if self.data is not None:
            filepath = self.data_dir / filename
            self.data.to_csv(filepath, index=False)
            logger.info(f" Data saved to {filepath}")
            return filepath
        return None

if __name__ == "__main__":
    collector = IndiaHouseDataCollector()
    df = collector.generate_india_data(2000)
    collector.save_data()
    print("\n Sample Data:")
    print(df.head())
    print("\n Data Statistics:")
    print(df.describe())