"""
OCR Helper for Programming Assistant
Provides OCR functionality to extract text from screenshots
"""
import os
import pytesseract
from PIL import Image
import cv2
import numpy as np

class OCRHelper:
    """
    OCR Helper class to extract text from images using Tesseract OCR.
    """
    
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR Helper.
        
        Args:
            tesseract_path: Path to Tesseract executable (required on Windows)
        """
        # Store the tesseract path for reference in settings
        self.tesseract_path = tesseract_path
        
        # Set Tesseract path if provided
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Verify if Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
        except Exception as e:
            print(f"Error initializing Tesseract OCR: {str(e)}")
            print("Please ensure Tesseract OCR is installed and the path is correct.")
            self.tesseract_available = False
    
    def preprocess_image(self, image_path):
        """
        Preprocess the image to improve OCR accuracy.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image
        """
        # Read image with OpenCV
        img = cv2.imread(str(image_path))
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get black and white image
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        return thresh
    
    def extract_text_from_image(self, image_path, preprocess=True):
        """
        Extract text from an image file.
        
        Args:
            image_path: Path to the image file
            preprocess: Whether to preprocess the image for better OCR results
            
        Returns:
            Extracted text string
        """
        if not self.tesseract_available:
            return "Error: Tesseract OCR is not properly configured."
            
        try:
            if preprocess:
                # Preprocess image
                img = self.preprocess_image(image_path)
                
                # Use pytesseract on preprocessed image
                text = pytesseract.image_to_string(img)
            else:
                # Use pytesseract directly on the image
                text = pytesseract.image_to_string(Image.open(image_path))
            
            return text.strip()
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def extract_code_from_image(self, image_path):
        """
        Extract code from an image, with optimizations for programming languages.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted code string
        """
        if not self.tesseract_available:
            return "Error: Tesseract OCR is not properly configured."
            
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            
            # Use pytesseract with custom configuration for code
            # -l eng: Use English language
            # --psm 6: Assume a single uniform block of text
            # --oem 3: Use LSTM OCR Engine with Tesseract
            custom_config = r'--oem 3 --psm 6 -l eng'
            text = pytesseract.image_to_string(img, config=custom_config)
            
            return text.strip()
        except Exception as e:
            return f"Error extracting code: {str(e)}"
    
    def extract_code_with_language_detection(self, image_path):
        """
        Extract code and try to detect the programming language.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (extracted_code, detected_language)
        """
        if not self.tesseract_available:
            return "Error: Tesseract OCR is not properly configured.", "unknown"
            
        # Extract the text first
        code = self.extract_code_from_image(image_path)
        
        if "Error extracting" in code:
            return code, "unknown"
        
        # Simple language detection based on keywords
        language_indicators = {
            'python': ['def ', 'import ', 'class ', 'if __name__ == "__main__":', '#!/usr/bin/python'],
            'javascript': ['function ', 'const ', 'let ', 'var ', 'document.', 'window.'],
            'java': ['public class ', 'private ', 'protected ', 'import java.', '@Override'],
            'c++': ['#include <', 'std::', 'using namespace', 'int main('],
            'html': ['<!DOCTYPE', '<html>', '<div>', '<body>', '<head>'],
            'css': ['{', '}', 'margin:', 'padding:', 'color:'],
            'sql': ['SELECT ', 'FROM ', 'WHERE ', 'JOIN ', 'GROUP BY'],
        }
        
        # Count occurrences of language indicators
        language_scores = {lang: 0 for lang in language_indicators}
        
        for lang, indicators in language_indicators.items():
            for indicator in indicators:
                if indicator in code:
                    language_scores[lang] += 1
        
        # Get the language with the highest score
        detected_language = max(language_scores.items(), key=lambda x: x[1])
        
        # If no clear indicators were found
        if detected_language[1] == 0:
            return code, "unknown"
            
        return code, detected_language[0]