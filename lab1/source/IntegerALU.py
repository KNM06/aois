from source.BaseALU import BaseALU
from constants import INT_FRAC_LEN, INT_INT_LEN


class IntegerALU(BaseALU):
    def _add_binary_arrays(self, a: list[int], b: list[int]) -> list[int]:
        res: list[int] = self.get_empty_array()
        carry: int = 0
        for i in range(self.bits - 1, -1, -1):
            s: int = a[i] + b[i] + carry
            res[i] = s % 2
            carry = s // 2
        return res

    def to_direct_code(self, num: int) -> list[int]:
        arr: list[int] = self.get_empty_array()
        if num < 0:
            arr[0] = 1
            num = -num

        idx: int = self.bits - 1
        while num > 0 and idx > 0:
            arr[idx] = num % 2
            num //= 2
            idx -= 1
        return arr

    def to_inverse_code(self, num: int) -> list[int]:
        arr: list[int] = self.to_direct_code(num)
        if arr[0] == 1:
            for i in range(1, self.bits):
                arr[i] = 1 if arr[i] == 0 else 0
        return arr

    def to_additional_code(self, num: int) -> list[int]:
        arr: list[int] = self.to_inverse_code(num)
        if arr[0] == 1:
            arr = self._add_binary_arrays(arr, self.to_direct_code(1))
        return arr

    def from_additional_code(self, arr: list[int]) -> int:
        if arr[0] == 1:
            arr_minus_1: list[int] = self._add_binary_arrays(
                arr, self.to_additional_code(-1)
            )
            val: int = 0
            for i in range(1, self.bits):
                bit: int = 1 if arr_minus_1[i] == 0 else 0
                val += bit * (2 ** (self.bits - 1 - i))
            return -val
        else:
            val = 0
            for i in range(1, self.bits):
                val += arr[i] * (2 ** (self.bits - 1 - i))
            return val

    def add_additional(self, num1: int, num2: int) -> list[int]:
        a: list[int] = self.to_additional_code(num1)
        b: list[int] = self.to_additional_code(num2)
        res: list[int] = self._add_binary_arrays(a, b)
        dec_res: int = self.from_additional_code(res)
        self.print_result(f"Сложение {num1} + {num2}", res, float(dec_res))
        return res

    def sub_additional(self, num1: int, num2: int) -> list[int]:
        a: list[int] = self.to_additional_code(num1)
        b_neg: list[int] = self.to_additional_code(-num2)
        res: list[int] = self._add_binary_arrays(a, b_neg)
        dec_res: int = self.from_additional_code(res)
        self.print_result(f"Вычитание {num1} - {num2}", res, float(dec_res))
        return res

    def mul_direct(self, num1: int, num2: int) -> list[int]:
        sign1: int = 1 if num1 < 0 else 0
        sign2: int = 1 if num2 < 0 else 0
        res_sign: int = sign1 ^ sign2

        a: list[int] = self.to_direct_code(abs(num1))
        b: list[int] = self.to_direct_code(abs(num2))
        res: list[int] = self.get_empty_array()

        for i in range(self.bits - 1, 0, -1):
            if b[i] == 1:
                shift: int = (self.bits - 1) - i
                shifted_a: list[int] = a[shift:] + [0] * shift if shift > 0 else a
                res = self._add_binary_arrays(res, shifted_a[-self.bits :])

        res[0] = res_sign
        dec_val: int = sum(
            res[i] * (2 ** (self.bits - 1 - i)) for i in range(1, self.bits)
        )
        dec_val = -dec_val if res_sign else dec_val
        self.print_result(f"Умножение {num1} * {num2}", res, float(dec_val))
        return res

    def _compare_abs(self, arr_a: list[int], arr_b: list[int]) -> bool:
        for k in range(1, self.bits):
            if arr_a[k] > arr_b[k]:
                return True
            if arr_a[k] < arr_b[k]:
                return False
        return True

    def _sub_abs(self, arr_a: list[int], arr_b: list[int]) -> list[int]:
        out = self.get_empty_array()
        borrow = 0
        for k in range(self.bits - 1, 0, -1):
            bit_diff = arr_a[k] - arr_b[k] - borrow
            if bit_diff < 0:
                bit_diff += 2
                borrow = 1
            else:
                borrow = 0
            out[k] = bit_diff
        return out

    def decode_div(self, arr: list[int]) -> float:
        sign = -1 if arr[0] == 1 else 1
        int_val = sum(
            arr[k] * (2 ** (INT_INT_LEN - k)) for k in range(1, INT_INT_LEN + 1)
        )
        frac_val = sum(
            arr[k] * (2 ** -(k - INT_INT_LEN))
            for k in range(INT_INT_LEN + 1, self.bits)
        )
        return sign * (int_val + frac_val)

    def div_direct(self, num1: int, num2: int) -> list[int]:
        if num2 == 0:
            raise ZeroDivisionError("Деление на ноль")

        sign_dividend: int = 1 if num1 < 0 else 0
        sign_divisor: int = 1 if num2 < 0 else 0
        final_sign: int = sign_dividend ^ sign_divisor

        dividend_arr: list[int] = self.to_direct_code(abs(num1))
        divisor_arr: list[int] = self.to_direct_code(abs(num2))

        total_steps: int = (self.bits - 1) + INT_FRAC_LEN

        accumulator: list[int] = self.get_empty_array()
        quotient_bits: list[int] = []

        for step in range(total_steps):
            accumulator = accumulator[1:] + [0]

            if step < (self.bits - 1):
                accumulator[-1] = dividend_arr[step + 1]
            else:
                accumulator[-1] = 0

            if self._compare_abs(accumulator, divisor_arr):
                accumulator = self._sub_abs(accumulator, divisor_arr)
                quotient_bits.append(1)
            else:
                quotient_bits.append(0)

        out_array: list[int] = self.get_empty_array()
        out_array[0] = final_sign

        out_array[1 : INT_INT_LEN + 1] = quotient_bits[
            INT_FRAC_LEN : INT_FRAC_LEN + INT_INT_LEN
        ]

        out_array[INT_INT_LEN + 1 : self.bits] = quotient_bits[
            INT_FRAC_LEN + INT_INT_LEN :
        ]

        dec_val: float = self.decode_div(out_array)

        self.print_result(
            f"Деление {num1} / {num2} (Точность 5 знаков)",
            out_array,
            float(f"{dec_val:.5f}"),
        )
        return out_array
