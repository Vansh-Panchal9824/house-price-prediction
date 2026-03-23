import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.india_data_collection import IndiaHouseDataCollector
from src.india_preprocessing import IndiaDataPreprocessor
from src.india_model_training import IndiaHousePriceModel

print("\n" + "="*60)
print("🇮🇳 INDIA HOUSE PRICE MODEL TRAINING")
print("="*60)

print("\n Step 1: Generating India house data...")
collector = IndiaHouseDataCollector()
df = collector.generate_india_data(3000)
filepath = collector.save_data()
print(f"Generated {len(df)} records")
print(f" Saved to {filepath}")

print("\n Step 2: Preprocessing data...")
preprocessor = IndiaDataPreprocessor()
df = preprocessor.load_data(filepath)
df = preprocessor.encode_categorical(df)
df = preprocessor.create_features(df)
X_train, X_test, y_train, y_test = preprocessor.prepare_data(df)
preprocessor.save_preprocessors()
print(f" Training samples: {len(X_train)}")
print(f" Test samples: {len(X_test)}")
print(f" Features: {preprocessor.feature_names}")

print("\n Step 3: Training models...")
trainer = IndiaHousePriceModel()
trainer.train_models(X_train, y_train)


print("\n Step 4: Evaluating models...")
trainer.evaluate_models(X_test, y_test)

print("\n Step 5: Selecting best model...")
trainer.select_best_model()


print("\n Step 6: Saving model...")
trainer.save_model()

print("\n" + "="*60)
print(" TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)
print("\n Next step: Run python app_india.py")