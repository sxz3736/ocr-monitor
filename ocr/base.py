# ocr/base.py
from .paddle_ocr import PaddleOCRRecognizer

class OCRManager:
    _instance = None   # 单例实例
    _backend_name = None

    def __new__(cls, *args, **kwargs):
        """
        保证 OCR 只初始化一次
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        backend="paddle",
        **kwargs
    ):
        """
        backend: str
            "paddle" / "tesseract" / "easyocr" ...
        kwargs:
            传递给具体 OCR backend 的初始化参数
        """

        # 防止重复初始化
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.backend_name = backend.lower()
        self.backend = self._create_backend(self.backend_name, **kwargs)

        self._initialized = True

    def _create_backend(self, backend_name, **kwargs):
        if backend_name == "paddle":
            return PaddleOCRRecognizer(**kwargs)

        raise ValueError(f"Unsupported OCR backend: {backend_name}")

    def recognize(self, image):
        """
        对外统一 OCR 接口
        """
        return self.backend.recognize(image)
