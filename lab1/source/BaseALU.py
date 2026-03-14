from constants import BITS


class BaseALU:
    def __init__(self) -> None:
        self.bits: int = BITS

    def get_empty_array(self) -> list[int]:
        return [0] * self.bits

    def print_result(
        self, label: str, bin_array: list[int], dec_value: float | None = None
    ) -> None:
        bin_str: str = "".join(map(str, bin_array))
        dec_str: str = f" (Десятичный: {dec_value})" if dec_value is not None else ""
        print(f"{label}: {bin_str}{dec_str}")
