import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class IndiaDataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
    
    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        logger.info(f" Loaded data: {df.shape}")
        return df
    
    def encode_categorical(self, df):
        if 'state' in df.columns:
            le = LabelEncoder()
            df['state_encoded'] = le.fit_transform(df['state'])
            self.label_encoders['state'] = le
            df.drop('state', axis=1, inplace=True)
        
    
        if 'area_type' in df.columns:
            area_mapping = {'Rich': 2, 'Medium': 1, 'Poor': 0}
            df['area_type_encoded'] = df['area_type'].map(area_mapping)
            df.drop('area_type', axis=1, inplace=True)
        
        if 'country' in df.columns:
            df.drop('country', axis=1, inplace=True)
        
        return df
    
    def create_features(self, df):
        if 'price' in df.columns and 'sqft' in df.columns:
            df['price_per_sqft'] = df['price'] / df['sqft']
        
    
        if 'age' in df.columns:
            df['is_new'] = (df['age'] < 5).astype(int)
            df['is_old'] = (df['age'] > 20).astype(int)
        
        return df
    
    def prepare_data(self, df, target_col='price', test_size=0.2):
    
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        
        
        X = X.select_dtypes(include=[np.number])
        
        self.feature_names = X.columns.tolist()
        

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
    
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        logger.info(f" Training set: {len(X_train)} samples")
        logger.info(f" Test set: {len(X_test)} samples")
        logger.info(f" Features: {self.feature_names}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def save_preprocessors(self, filename='india_preprocessors.pkl'):
        
        preprocessors = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        filepath = self.models_dir / filename
        joblib.dump(preprocessors, filepath)
        logger.info(f" Preprocessors saved to {filepath}")
        return filepath

if __name__ == "__main__":
    preprocessor = IndiaDataPreprocessor()
    df = preprocessor.load_data("data/raw/india_housing_data.csv")
    df = preprocessor.encode_categorical(df)
    df = preprocessor.create_features(df)
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
    preprocessor.save_preprocessors()
    print(" Preprocessing completed!")