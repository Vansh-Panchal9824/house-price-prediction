import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class IndiaHousePriceModel:
    def __init__(self):
        self.models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=1.0)
        }
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
    
    def train_models(self, X_train, y_train):
        print("\n" + "="*60)
        print("🇮🇳 TRAINING INDIA HOUSE PRICE MODELS")
        print("="*60)
        
        for name, model in self.models.items():
            try:
                print(f"\n Training {name}...")
                model.fit(X_train, y_train)
                
                train_score = model.score(X_train, y_train)
                self.results[name] = {'model': model, 'train_score': train_score}
                print(f" {name} trained (R² = {train_score:.4f})")
                
            except Exception as e:
                print(f" Error training {name}: {e}")
    
    def evaluate_models(self, X_test, y_test):
        print("\n" + "="*60)
        print("EVALUATING MODELS")
        print("="*60)
        
        for name, result in self.results.items():
            model = result['model']
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.results[name].update({
                'test_mse': mse,
                'test_mae': mae,
                'test_r2': r2
            })
            
            print(f"\n {name}:")
            print(f"   MAE: ₹{mae:,.2f}")
            print(f"   RMSE: ₹{np.sqrt(mse):,.2f}")
            print(f"   R² Score: {r2:.4f}")
    
    def select_best_model(self):
        best_r2 = -np.inf
        for name, result in self.results.items():
            if result['test_r2'] > best_r2:
                best_r2 = result['test_r2']
                self.best_model = result['model']
                self.best_model_name = name
        
        print("\n" + "="*60)
        print(" BEST MODEL SELECTED")
        print("="*60)
        print(f"Model: {self.best_model_name}")
        print(f"R² Score: {best_r2:.4f}")
        
        return self.best_model
    
    def save_model(self, filename='india_house_price_model.pkl'):
        if self.best_model:
            filepath = self.models_dir / filename
            joblib.dump(self.best_model, filepath)
            print(f"\n✅ Model saved to {filepath}")
            return filepath
        return None

if __name__ == "__main__":
    from india_preprocessing import IndiaDataPreprocessor

    preprocessor = IndiaDataPreprocessor()
    df = preprocessor.load_data("data/raw/india_housing_data.csv")
    df = preprocessor.encode_categorical(df)
    df = preprocessor.create_features(df)
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
    preprocessor.save_preprocessors()
    
    
    trainer = IndiaHousePriceModel()
    trainer.train_models(X_train, y_train)
    trainer.evaluate_models(X_test, y_test)
    trainer.select_best_model()
    trainer.save_model()
    
    print("\n✅ Training completed successfully!")