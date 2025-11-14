from typing import List, Dict, Optional
class PengelolaSkor:
    def __init__(self):
        self.skor: Dict[int, int] = {}  # key = id pemain, value = poin

    def tambah_skor(self, pemain_id: int, poin: int) -> None:
        pass

    def reset(self) -> None:
        pass

    def giliran_berikut(self) -> int:
        """Kembalikan id pemain berikutnya (atau logika pergantian giliran)."""
        pass