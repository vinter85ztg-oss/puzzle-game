#!/usr/bin/env python3
"""
Program do automatycznego rozwiązywania puzzli ze zdjęcia
"""

import cv2
import sys
import os
from puzzle_solver import PuzzleSolver

def main():
    """
    Główna funkcja programu
    """
    # Sprawdzenie argumentów
    if len(sys.argv) < 2:
        print("Użycie: python main.py <ścieżka_do_zdjęcia>")
        print("\nPrzykład:")
        print("  python main.py puzzle.jpg")
        print("  python main.py ./photos/my_puzzle.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Sprawdzenie czy plik istnieje
    if not os.path.exists(image_path):
        print(f"Błąd: Plik '{image_path}' nie istnieje!")
        sys.exit(1)
    
    # Sprawdzenie czy to obraz
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
        print(f"Błąd: Plik musi być obrazem ({', '.join(valid_extensions)})")
        sys.exit(1)
    
    print("╔════════════════════════════════════════╗")
    print("║   SOLVER PUZZLI - WERSJA AUTOMATYCZNA  ║")
    print("╚════════════════════════════════════════╝\n")
    
    try:
        # Inicjalizacja solvera
        print(f"Wczytywanie obrazu: {image_path}")
        solver = PuzzleSolver(image_path)
        
        # Rozwiązanie puzzli
        solution = solver.solve(output_dir='results')
        
        # Wydruk statystyk
        solver.print_statistics()
        
        # Wyświetlenie wyników
        print("\n✓ Puzzle zostało pomyślnie rozwiązane!")
        print("  Wyniki znajdują się w katalogu 'results/'")
        
        # Opcja wyświetlenia rezultatu
        if len(sys.argv) > 2 and sys.argv[2] == '--show':
            print("\nWyświetlanie wyników...")
            cv2.namedWindow('Rozwiązanie', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Rozwiązanie', 1200, 800)
            cv2.imshow('Rozwiązanie', solution)
            print("Naciśnij dowolny klawisz, aby zamknąć okno...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"\n✗ Błąd: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
