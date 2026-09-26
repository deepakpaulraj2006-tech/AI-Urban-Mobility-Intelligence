@echo off
python src\data_generation.py
python src\data_cleaning.py
python src\train_model.py
python verify_project.py
pause
