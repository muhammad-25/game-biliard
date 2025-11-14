from .objek_game import ObjekGame
class Bola(ObjekGame):
    def __init__(
        self,
        nomor: int = 0,
        warna: str = "putih",
        x: float = 0.0,
        y: float = 0.0,
        jari_jari: float = 0.0,
        massa: float = 1.0
    ):
        super().__init__(x=x, y=y, jari_jari=jari_jari)
        self.nomor: int = nomor
        self.warna: str = warna
        self.kecepatanX: float = 0.0
        self.kecepatanY: float = 0.0
        self.massa: float = massa
        self.terjebak_di_lubang: bool = False

    def terapkan_impuls(self, ix: float, iy: float) -> None:
        pass

    def perbarui(self, dt: float) -> None:
        pass