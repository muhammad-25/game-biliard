class ObjekGame:
    """Kelas dasar untuk semua objek pada meja (posisi + ukuran dasar)."""
    def __init__(self, x: float = 0.0, y: float = 0.0, jari_jari: float = 0.0):
        self.x: float = x
        self.y: float = y
        self.jari_jari: float = jari_jari

    def perbarui(self, dt: float) -> None:
        pass

    def gambar(self, layar) -> None:
        pass