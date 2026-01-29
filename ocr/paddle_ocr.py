# ocr/paddle_ocr.py
import numpy as np
from paddleocr import PaddleOCR
from .backend import OCRBackend

class PaddleOCRRecognizer(OCRBackend):
    def __init__(
        self,
        lang="ch",
        use_angle_cls=True,
        use_gpu=False,
        show_log=False
    ):
        self.ocr = PaddleOCR(
            lang=lang,
            use_angle_cls=use_angle_cls,
            use_gpu=use_gpu,
            show_log=show_log
        )

    def recognize(self, image):
        result = self.ocr.ocr(image, cls=True)
        if not result or not result[0]:
            return []

        outputs = []
        for box, (text, conf) in result[0]:
            pts = np.array(box, dtype=np.int32)
            outputs.append({
                "text": text.strip(),
                "confidence": float(conf),
                "bbox": {
                    "x1": int(pts[:, 0].min()),
                    "y1": int(pts[:, 1].min()),
                    "x2": int(pts[:, 0].max()),
                    "y2": int(pts[:, 1].max()),
                }
            })
        return outputs
