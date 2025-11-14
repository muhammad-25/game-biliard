from .bola import Bola
from typing import List, Dict, Optional
class Tongkat:
    def __init__(self):
        self.sudut: float = 0.0
        self.kekuatan: float = 0.0
        self.terpasang_pada: Optional[Bola] = None

    def pasang(self, bola: Bola) -> None:
        pass

    def tarik_kanan(self, jarak: float) -> None:
        pass

    def lepaskan(self) -> None:
        pass
