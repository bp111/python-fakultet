# Przewidywanie odejścia klientów

## Streszczenie 
Ten projekt podejmuje problem przewidzenia czy klient pewnego serwisu opuści serwis czy nie (churn) używając różnych algorytmów klasyfikacji. Porównuje 5 różych modeli uczenia maszynowego (Regresja logistyczna, KNN, SVM, Random Forest, Sieć Neuronowa), dokonuje optymalizacji doboru hiperparametrów. Wykonuje również obróbkę wstępna danych (dane: Telco Customer Churn, https://www.kaggle.com/datasets/blastchar/telco-customer-churn).

W folderze "report" znajduje się dodatkowo tekst wyłaniający najlepiej sprawujący się w tym przypadku model.

## Set-up
1. Sklonuj repozytorium.
2. Utwórz wirtualne środowisko: `python -m venv .venv`
3. Aktywuj środowisko:
   - Windows: `Set-ExecutionPolicy Unrestricted -Scope Process`, potem `.venv/Scripts/Activate.ps1`
4. Zainstaluj zależności: `pip install -r requirements.txt`
5. Uruchom projekt: `python main.py`

## Zakres korzystania z pomocy samouczków i AI:
- AI: pomoc w debugowaniu

## Bibliografia:
- samouczki, dokumentacja:
    - https://docs.python.org/3/, 3.05.2026
    - https://www.kaggle.com/learn, 6.05.2026    
    - https://scikit-learn.org/, 6.05.2026    
- AI:
    - Google Gemini 3.1 Pro, 6.05.2026