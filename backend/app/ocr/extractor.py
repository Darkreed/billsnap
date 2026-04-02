from abc import ABC, abstractmethod

import numpy as np
from PIL import Image
import pytesseract


class OCRExtractor(ABC):

    @abstractmethod
    def extract_text(self, image: Image.Image) -> str:
        ...


class TesseractExtractor(OCRExtractor):

    def extract_text(self, image: Image.Image) -> str:
        extracted_text = pytesseract.image_to_string(image, lang="eng+jpn")
        return extracted_text


class PaddleOCRExtractor(OCRExtractor):

    def __init__(self):
        from paddleocr import PaddleOCR
        # lang="japan" enables Japanese + English recognition
        self._ocr = PaddleOCR(use_doc_orientation_classify=False, use_angle_cls=False, lang="japan")

    def extract_text(self, image: Image.Image) -> str:
        img_array = np.array(image)
        result = self._ocr.predict(img_array)
        if not result:
            return ""
        return "\n".join(result[0].get("rec_texts", []))

        
