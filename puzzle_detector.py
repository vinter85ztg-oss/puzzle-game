import cv2
import numpy as np
from scipy import ndimage
from sklearn import preprocessing
import imutils

class PuzzleDetector:
    def __init__(self, image_path):
        """
        Inicjalizacja detektora puzzli
        
        Args:
            image_path: ścieżka do zdjęcia z rozrzuconymi puzzlami
        """
        self.image = cv2.imread(image_path)
        self.original_image = self.image.copy()
        self.height, self.width = self.image.shape[:2]
        self.pieces = []
        self.contours = []
        
    def preprocess_image(self):
        """
        Przetwarzanie wstępne zdjęcia
        """
        # Konwersja na skalę szarości
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Rozmazanie Gaussa
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptacyjne thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Dylatacja i erozja
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
        
        return processed
    
    def detect_pieces(self):
        """
        Detekcja poszczególnych kawałków puzzli
        """
        processed = self.preprocess_image()
        
        # Znalezienie konturów
        contours, _ = cv2.findContours(
            processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filtrowanie konturów po rozmiarze
        min_area = (self.width * self.height) // 10000
        max_area = (self.width * self.height) // 10
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                self.contours.append(contour)
                
                # Otrzymanie obszaru zainteresowania (ROI)
                x, y, w, h = cv2.boundingRect(contour)
                piece = self.original_image[y:y+h, x:x+w].copy()
                
                self.pieces.append({
                    'image': piece,
                    'contour': contour,
                    'bbox': (x, y, w, h),
                    'center': (x + w//2, y + h//2),
                    'area': area
                })
        
        print(f"Wykryto {len(self.pieces)} kawałków puzzli")
        return self.pieces
    
    def extract_features(self, piece_image):
        """
        Ekstrakcja cech z kawałka puzzli
        
        Args:
            piece_image: obraz kawałka
            
        Returns:
            wektor cech
        """
        # Konwersja na skalę szarości
        gray = cv2.cvtColor(piece_image, cv2.COLOR_BGR2GRAY)
        
        # Histogram koloru
        hist = cv2.calcHist([piece_image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        # Statystyki obrazu
        mean_val = np.mean(gray)
        std_val = np.std(gray)
        
        features = np.concatenate([hist, [mean_val, std_val]])
        return features
    
    def match_pieces(self, max_distance_threshold=100):
        """
        Dopasowywanie kawałków puzzli na podstawie sąsiedztwa
        
        Args:
            max_distance_threshold: maksymalna odległość między kawałkami
            
        Returns:
            lista par dopasowanych kawałków
        """
        matches = []
        
        for i in range(len(self.pieces)):
            for j in range(i + 1, len(self.pieces)):
                piece_i = self.pieces[i]
                piece_j = self.pieces[j]
                
                # Obliczenie odległości między środkami
                center_i = np.array(piece_i['center'])
                center_j = np.array(piece_j['center'])
                distance = np.linalg.norm(center_i - center_j)
                
                if distance < max_distance_threshold:
                    # Porównanie cech
                    feat_i = self.extract_features(piece_i['image'])
                    feat_j = self.extract_features(piece_j['image'])
                    
                    # Cosine similarity
                    similarity = np.dot(feat_i, feat_j) / (
                        np.linalg.norm(feat_i) * np.linalg.norm(feat_j) + 1e-5
                    )
                    
                    matches.append({
                        'piece_i': i,
                        'piece_j': j,
                        'distance': distance,
                        'similarity': similarity,
                        'score': similarity
                    })
        
        # Sortowanie po wynikowi
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches
    
    def solve_puzzle(self):
        """
        Główna funkcja rozwiązywania puzzli
        """
        print("Rozpoczęcie rozwiązywania puzzli...")
        
        # Detekcja kawałków
        self.detect_pieces()
        
        if len(self.pieces) == 0:
            print("Nie znaleziono kawałków puzzli!")
            return None
        
        # Dopasowywanie kawałków
        matches = self.match_pieces()
        
        print(f"Znaleziono {len(matches)} potencjalnych połączeń")
        
        return matches
    
    def visualize_pieces(self, output_path='pieces_detected.jpg'):
        """
        Wizualizacja wykrytych kawałków
        """
        result = self.original_image.copy()
        
        for piece in self.pieces:
            contour = piece['contour']
            cv2.drawContours(result, [contour], 0, (0, 255, 0), 2)
            
            # Narysowanie bounding box
            x, y, w, h = piece['bbox']
            cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 1)
        
        cv2.imwrite(output_path, result)
        print(f"Zapisano wizualizację: {output_path}")
        return result
    
    def visualize_matches(self, matches, output_path='matches_visualization.jpg'):
        """
        Wizualizacja dopasowanych kawałków
        """
        result = self.original_image.copy()
        
        # Narysowanie linii między dopasowanymi kawałkami
        for match in matches[:20]:  # Top 20 matches
            i = match['piece_i']
            j = match['piece_j']
            
            center_i = self.pieces[i]['center']
            center_j = self.pieces[j]['center']
            
            # Kolor zależy od wyniku dopasowania
            color_intensity = min(255, int(match['similarity'] * 255))
            color = (0, color_intensity, 255 - color_intensity)
            
            cv2.line(result, center_i, center_j, color, 2)
            cv2.circle(result, center_i, 5, (0, 255, 0), -1)
            cv2.circle(result, center_j, 5, (0, 255, 0), -1)
        
        cv2.imwrite(output_path, result)
        print(f"Zapisano wizualizację dopasowań: {output_path}")
        return result
