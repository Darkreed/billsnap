from abc import ABC, abstractmethod

from PIL import Image
import pytesseract


class OCRExtractor(ABC):
    
    @abstractmethod
    def extract_text(self, image: Image.Image) -> str:
        ...


class TesseractExtractor(OCRExtractor):

    def extract_text(self, image: Image.Image) -> str:
        bill_str = pytesseract.image_to_string(image, lang="eng+jpn")
        return bill_str
        
