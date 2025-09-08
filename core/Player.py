class Player:
    def __init__(self, color: str, nombre: str | None = None):
        color_norm = (color or "").strip().lower()
        if color_norm not in ("blanco", "negro"):
            raise ValueError("color debe ser 'blanco' o 'negro'")
        self._color = color_norm
        self._nombre = nombre

    def obtener_color(self) -> str:
        return self._color

    def es_blanco(self) -> bool:
        return self._color == "blanco"

    def es_negro(self) -> bool:
        return self._color == "negro"

    def nombre(self) -> str | None:
        return self._nombre