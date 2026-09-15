import cv2
import numpy as np
from puzzle_detector import PuzzleDetector
import networkx as nx
from collections import defaultdict

class PuzzleSolver:
    def __init__(self, image_path):
        """
        Inicjalizacja solwera puzzli
        
        Args:
            image_path: ścieżka do zdjęcia z puzzlami
        """
        self.detector = PuzzleDetector(image_path)
        self.image = self.detector.original_image.copy()
        self.graph = nx.Graph()
        self.solution = None
        
    def build_graph(self, matches):
        """
        Budowanie grafu połączeń między kawałkami
        
        Args:
            matches: lista dopasowanych kawałków
        """
        # Dodanie węzłów
        for i, piece in enumerate(self.detector.pieces):
            self.graph.add_node(i, piece=piece)
        
        # Dodanie krawędzi
        for match in matches:
            self.graph.add_edge(
                match['piece_i'],
                match['piece_j'],
                weight=match['similarity'],
                distance=match['distance']
            )
        
        print(f"Graf: {len(self.graph.nodes)} węzłów, {len(self.graph.edges)} krawędzi")
    
    def find_corners(self):
        """
        Znalezienie kawałków narożników
        """
        corners = []
        
        for i, piece in enumerate(self.detector.pieces):
            contour = piece['contour']
            
            # Przybliżenie konturu do wielokąta
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Narożniki mają zwykle 3-4 wierzchołki
            if 3 <= len(approx) <= 4:
                # Analiza kąta
                corners.append({
                    'piece_id': i,
                    'vertices': len(approx),
                    'piece': piece
                })
        
        print(f"Znaleziono {len(corners)} potencjalnych narożników")
        return corners
    
    def arrange_pieces(self):
        """
        Ułożenie kawałków w całość na podstawie grafu
        """
        if len(self.detector.pieces) == 0:
            return None
        
        # Sortowanie kawałków po współrzędnym X
        sorted_pieces = sorted(
            enumerate(self.detector.pieces),
            key=lambda x: x[1]['center'][0]
        )
        
        # Tworzenie siatki
        rows = int(np.sqrt(len(self.detector.pieces)))
        cols = int(np.ceil(len(self.detector.pieces) / rows))
        
        print(f"Szacunkowe wymiary puzzli: {cols}x{rows}")
        
        # Obliczenie średniej wielkości kawałka
        avg_width = np.mean([p['bbox'][2] for p in self.detector.pieces])
        avg_height = np.mean([p['bbox'][3] for p in self.detector.pieces])
        
        return {
            'rows': rows,
            'cols': cols,
            'avg_width': avg_width,
            'avg_height': avg_height,
            'pieces': self.detector.pieces
        }
    
    def create_solution_image(self, arrangement):
        """
        Tworzenie obrazu z ułożonymi kawałkami
        
        Args:
            arrangement: informacje o ułożeniu
            
        Returns:
            obraz z ułożonym puzzlem
        """
        rows = arrangement['rows']
        cols = arrangement['cols']
        avg_width = int(arrangement['avg_width'])
        avg_height = int(arrangement['avg_height'])
        
        # Tworzenie pustego obrazu
        canvas = np.ones(
            (rows * avg_height + 20, cols * avg_width + 20, 3),
            dtype=np.uint8
        ) * 255
        
        # Sortowanie kawałków
        pieces = sorted(
            enumerate(arrangement['pieces']),
            key=lambda x: (x[1]['center'][1] // avg_height, x[1]['center'][0] // avg_width)
        )
        
        # Umieszczanie kawałków
        for idx, (orig_idx, piece) in enumerate(pieces):
            row = idx // cols
            col = idx % cols
            
            y = row * avg_height + 10
            x = col * avg_width + 10
            
            piece_img = piece['image']
            
            # Zmiana rozmiaru kawałka
            resized = cv2.resize(piece_img, (avg_width, avg_height))
            
            # Umieszczenie na kanwie
            canvas[y:y+avg_height, x:x+avg_width] = resized
        
        return canvas
    
    def solve(self, output_dir='results'):
        """
        Główna funkcja rozwiązywania puzzli
        
        Args:
            output_dir: katalog na wyniki
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n=== ROZWIĄZYWANIE PUZZLI ===\n")
        
        # Detekcja kawałków
        print("1. Detekcja kawałków...")
        self.detector.detect_pieces()
        
        # Wizualizacja wykrytych kawałków
        print("2. Wizualizacja wykrytych kawałków...")
        self.detector.visualize_pieces(f'{output_dir}/1_pieces_detected.jpg')
        
        # Dopasowywanie kawałków
        print("3. Dopasowywanie kawałków...")
        matches = self.detector.match_pieces()
        
        # Wizualizacja dopasowań
        print("4. Wizualizacja dopasowań...")
        self.detector.visualize_matches(matches, f'{output_dir}/2_matches.jpg')
        
        # Budowanie grafu
        print("5. Budowanie grafu połączeń...")
        self.build_graph(matches)
        
        # Znalezienie narożników
        print("6. Szukanie narożników...")
        corners = self.find_corners()
        
        # Ułożenie kawałków
        print("7. Ułożenie kawałków...")
        arrangement = self.arrange_pieces()
        
        # Tworzenie rozwiązania
        print("8. Tworzenie obrazu rozwiązania...")
        solution = self.create_solution_image(arrangement)
        
        # Zapis wyników
        output_path = f'{output_dir}/3_solution.jpg'
        cv2.imwrite(output_path, solution)
        print(f"\n✓ Rozwiązanie zapisane: {output_path}")
        
        self.solution = solution
        return solution
    
    def print_statistics(self):
        """
        Wydruk statystyk
        """
        print("\n=== STATYSTYKI ===")
        print(f"Liczba kawałków: {len(self.detector.pieces)}")
        print(f"Liczba krawędzi grafu: {len(self.graph.edges)}")
        print(f"Wymiary obrazu: {self.image.shape[1]}x{self.image.shape[0]}")
