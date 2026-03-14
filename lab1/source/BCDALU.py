from source.BaseALU import BaseALU
from constants import (
    BCD_MAX_DIGITS,
    BCD_DIGIT_BITS,
    BCD_CORRECTION_THRESHOLD,
    BCD_CORRECTION_VALUE,
    BCD_CARRY_THRESHOLD,
    BCD_MODULO,
    BCD_BASE,
)


class BCDALU(BaseALU):
    def int_to_bcd_8421(self, num: int) -> list[int]:
        arr: list[int] = self.get_empty_array()
        s_num = str(abs(num))
        if len(s_num) > BCD_MAX_DIGITS:
            raise ValueError(f"Число слишком большое для {self.bits}-бит BCD")

        idx: int = self.bits - BCD_DIGIT_BITS
        for digit in reversed(s_num):
            val = int(digit)
            for i in range(BCD_DIGIT_BITS - 1, -1, -1):
                arr[idx + i] = val % 2
                val //= 2
            idx -= BCD_DIGIT_BITS
        self.print_result(f"8421 BCD для {num}", arr, float(num))
        return arr

    def from_bcd_8421(self, arr: list[int]) -> int:
        res: int = 0
        multiplier: int = 1
        for i in range(self.bits - BCD_DIGIT_BITS, -1, -BCD_DIGIT_BITS):
            digit: int = arr[i] * 8 + arr[i + 1] * 4 + arr[i + 2] * 2 + arr[i + 3] * 1
            res += digit * multiplier
            multiplier *= BCD_BASE
        return res

    def add_bcd_8421(self, num1: int, num2: int) -> list[int]:
        bcd1: list[int] = self.int_to_bcd_8421(abs(num1))
        bcd2: list[int] = self.int_to_bcd_8421(abs(num2))
        res: list[int] = self.get_empty_array()
        carry: int = 0

        for i in range(self.bits - 1, -1, -BCD_DIGIT_BITS):
            val1: int = (
                bcd1[i] * 1 + bcd1[i - 1] * 2 + bcd1[i - 2] * 4 + bcd1[i - 3] * 8
            )
            val2: int = (
                bcd2[i] * 1 + bcd2[i - 1] * 2 + bcd2[i - 2] * 4 + bcd2[i - 3] * 8
            )

            s: int = val1 + val2 + carry
            if s > BCD_CORRECTION_THRESHOLD:
                s += BCD_CORRECTION_VALUE

            carry = 1 if s > BCD_CARRY_THRESHOLD else 0

            res_val: int = s % BCD_MODULO
            for j in range(BCD_DIGIT_BITS):
                res[i - j] = res_val % 2
                res_val //= 2

        dec_val: int = self.from_bcd_8421(res)
        self.print_result(f"Сложение BCD 8421: {num1} + {num2}", res, float(dec_val))
        return res
