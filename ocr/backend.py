# ocr/backend.py
from abc import ABC, abstractmethod

class OCRBackend(ABC):
    @abstractmethod
    def recognize(self, image):
        """
        输入:
            image: BGR numpy array

        输出:
            [
                {
                    "text": str,
                    "confidence": float,
                    "bbox": {
                        "x1": int, "y1": int,
                        "x2": int, "y2": int
                    }
                },
                ...
            ]
        """
        pass
