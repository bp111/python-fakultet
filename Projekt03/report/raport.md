## Wybór najlepszego modelu

Za najlepszy model można uznać regresję logistyczną.

#### Uzasadnienie wyboru:
* **Odporność na przeuczenie**: Modele takie jak Random Forest oraz Neural Network wykazały na krzywych uczenia się ewidentne przeuczenie – wynik na zbiorze treningowym był bardzo wysoki - ponad 0.85 - podczas gdy wynik walidacyjny utrzymywał się na znacznie niższym poziomie. Regresja logistyczna zaprezentowała najbardziej stabilną i zbieżną krzywą uczenia się.
* **Najwyższa skuteczność dla klasy mniejszościowej**: Problem przewidzenia odejść charakteryzuje się niezbalansowanym zbiorem danych - dużo więcej klientów zostaje niż odchodzi. Z tego powodu główną metryką nie była ogólna dokładność, ale F1-Score oraz Recall dla klasy 1. Regresja Logistyczna osiągnęła najwyższy wynik F1-Score - 0.59 - oraz poprawnie zidentyfikowała największą liczbę odchodzących klientów w macierzy błędów - 208 true positives.