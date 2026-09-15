# 🧩 Automatyczny Solver Puzzli

Program do automatycznego rozwiązywania puzzli na podstawie zdjęcia. Wykorzystuje zaawansowane techniki przetwarzania obrazu i analizę grafów do wykrycia i ułożenia kawałków puzzli.

## 🎯 Możliwości

- ✅ Automatyczna detekcja kawałków puzzli na zdjęciu
- ✅ Analiza cech i kształtów kawałków
- ✅ Inteligentne dopasowywanie pasujących części
- ✅ Wizualizacja procesu rozwiązywania
- ✅ Tworzenie finalnego obrazu z ułożonym puzzlem

## 🛠️ Wymagania

- Python 3.7+
- OpenCV
- NumPy
- SciPy
- scikit-image
- scikit-learn
- Pillow
- Matplotlib
- NetworkX

## 📦 Instalacja

1. **Klonowanie repozytorium:**
```bash
git clone https://github.com/vinter85ztg-oss/puzzle-game.git
cd puzzle-game
```

2. **Instalacja zależności:**
```bash
pip install -r requirements.txt
```

## 🚀 Użycie

### Podstawowe użycie:

```bash
python main.py <ścieżka_do_zdjęcia>
```

### Przykłady:

```bash
# Rozwiązanie puzzli z pliku local
python main.py puzzle.jpg

# Rozwiązanie puzzli z podkatalogu
python main.py ./photos/my_puzzle.png

# Rozwiązanie i wyświetlenie wyniku
python main.py puzzle.jpg --show
```

## 📂 Struktura projektu

```
puzzle-game/
├── main.py                 # Główny script
├── puzzle_detector.py      # Moduł detekcji kawałków
├── puzzle_solver.py        # Moduł rozwiązywania
├── requirements.txt        # Zależności
├── README.md              # Dokumentacja
└── results/               # Katalog z wynikami
    ├── 1_pieces_detected.jpg   # Wykryte kawałki
    ├── 2_matches.jpg           # Wizualizacja dopasowań
    └── 3_solution.jpg          # Finalne rozwiązanie
```

## 🔍 Jak to działa?

### 1. **Przetwarzanie wstępne**
- Konwersja na skalę szarości
- Rozmazanie Gaussa
- Adaptacyjne thresholding
- Morfologiczne operacje (dylatacja, erozja)

### 2. **Detekcja kawałków**
- Znalezienie konturów na przetworzonym obrazie
- Filtrowanie po rozmiarze (minimalna i maksymalna powierzchnia)
- Ekstrakcja ROI (Region of Interest) dla każdego kawałka

### 3. **Analiza cech**
- Histogram kolorów (8x8x8 kanały HSV)
- Statystyki (średnia, odchylenie standardowe)
- Cechy geometryczne (kształt, rozmiar)

### 4. **Dopasowywanie kawałków**
- Obliczanie odległości między centrami kawałków
- Porównanie cech przy pomocy Cosine Similarity
- Budowanie grafu połączeń

### 5. **Ułożenie puzzli**
- Sortowanie kawałków po pozycji
- Obliczenie siatki (liczba wierszy i kolumn)
- Rozmieszczenie na kanwie
- Zmiana rozmiaru do jednolitych wymiarów

## 📊 Wyniki

Program generuje 3 obrazy w katalogu `results/`:

1. **pieces_detected.jpg** - Wizualizacja wykrytych kawałków (zielone prostokąty, niebieskie obszary)
2. **matches.jpg** - Wizualizacja dopasowań (linie łączące pasujące kawałki, kolor wskazuje pewność)
3. **solution.jpg** - **Finalne rozwiązanie** - całość ułożone puzzle

## ⚙️ Parametry i dostrojenia

Możesz dostosować zachowanie programu edytując poniższe wartości w kodzie:

```python
# W puzzle_detector.py

# Rozmiar jądra dla morfologicznych operacji
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Minimalna i maksymalna powierzchnia kawałka
min_area = (self.width * self.height) // 10000
max_area = (self.width * self.height) // 10

# Maksymalna odległość dla dopasowywania
max_distance_threshold = 100

# Histogram - liczba binów
hist = cv2.calcHist(..., [8, 8, 8], ...)
```

## 💡 Porady dla najlepszych wyników

1. **Oświetlenie**: Zapewni dobre, równomierne oświetlenie
2. **Kontrast**: Tło powinno mieć inny kolor niż kawałki puzzli
3. **Rozdzielczość**: Użyj wysokiej rozdzielczości (min. 1920x1440)
4. **Kąt**: Zrób zdjęcie prostopadle do puzzli
5. **Czystość**: Upewnij się, że kawałki nie zachodią na siebie
6. **Rozmiar pliku**: Optymalne wymiary 2000-4000 pikseli

## 🐛 Troubleshooting

### "Nie znaleziono kawałków puzzli!"
- Sprawdź kontrast między puzzlem a tłem
- Zmniejsz lub zwiększ wartości `min_area` i `max_area`
- Upewnij się, że zdjęcie ma dobrej jakości

### Słabe dopasowanie kawałków
- Dostosuj `max_distance_threshold`
- Zmień parametry histogramu w `extract_features()`
- Poprawiaj oświetlenie na zdjęciu

### Nierówne rozmieszczenie
- Kawałki puzzli mogą mieć różne rozmiary - to normalne
- Program automatycznie je normalizuje

## 📝 Licencja

MIT License - zobacz LICENSE.md

## 👨‍💻 Autor

Created with ❤️ for puzzle lovers

## 🤝 Wkład

Zapraszamy do zgłaszania issues i pull requestów!

---

**Powodzenia przy rozwiązywaniu puzzli! 🧩✨**
