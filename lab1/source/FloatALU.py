from source.BaseALU import BaseALU
from constants import (
    FLOAT_EXP_LEN,
    FLOAT_MANT_LEN,
    FLOAT_EXP_BIAS,
    FLOAT_MANT_IMPLICIT_LEN,
)


class FloatALU(BaseALU):
    def _add_arrays(self, a: list[int], b: list[int]) -> list[int]:
        length: int = len(a)
        res: list[int] = [0] * length
        carry: int = 0
        for i in range(length - 1, -1, -1):
            s: int = a[i] + b[i] + carry
            res[i] = s % 2
            carry = s // 2
        return res

    def _sub_arrays(self, a: list[int], b: list[int]) -> list[int]:
        length: int = len(a)
        b_comp: list[int] = [0] * length
        carry: int = 1
        for i in range(length - 1, -1, -1):
            s: int = (1 if b[i] == 0 else 0) + carry
            b_comp[i] = s % 2
            carry = s // 2

        res: list[int] = [0] * length
        carry = 0
        for i in range(length - 1, -1, -1):
            s: int = a[i] + b_comp[i] + carry
            res[i] = s % 2
            carry = s // 2
        return res

    def _is_greater_or_equal(self, a: list[int], b: list[int]) -> bool:
        for i in range(len(a)):
            if a[i] > b[i]:
                return True
            if a[i] < b[i]:
                return False
        return True

    def float_to_ieee754(self, f_num: float) -> list[int]:
        arr: list[int] = self.get_empty_array()
        if f_num == 0.0:
            self.print_result(f"IEEE-754 ({self.bits}-bit)", arr, f_num)
            return arr

        if f_num < 0:
            arr[0] = 1
            f_num = -f_num

        int_part: int = int(f_num)
        frac_part: float = f_num - int_part

        int_bits: list[int] = []
        while int_part > 0:
            int_bits.append(int_part % 2)
            int_part //= 2
        int_bits.reverse()

        frac_bits: list[int] = []
        while frac_part > 0 and len(frac_bits) < self.bits:
            frac_part *= 2
            bit = int(frac_part)
            frac_bits.append(bit)
            frac_part -= bit

        if int_bits:
            exponent: int = len(int_bits) - 1
            mantissa: list[int] = int_bits[1:] + frac_bits
        else:
            first_1: int = frac_bits.index(1) if 1 in frac_bits else 0
            exponent = -(first_1 + 1)
            mantissa = frac_bits[first_1 + 1 :]

        exp_biased: int = exponent + FLOAT_EXP_BIAS
        exp_bits: list[int] = []
        for _ in range(FLOAT_EXP_LEN):
            exp_bits.append(exp_biased % 2)
            exp_biased //= 2
        exp_bits.reverse()
        arr[1 : 1 + FLOAT_EXP_LEN] = exp_bits

        for i in range(min(FLOAT_MANT_LEN, len(mantissa))):
            arr[1 + FLOAT_EXP_LEN + i] = mantissa[i]

        display_val = -f_num if arr[0] == 1 else f_num
        self.print_result(f"IEEE-754 для {display_val}", arr)
        return arr

    def from_ieee754(self, arr: list[int]) -> float:
        sign: int = -1 if arr[0] == 1 else 1

        exp_biased: int = 0
        for i in range(1, 1 + FLOAT_EXP_LEN):
            power: int = FLOAT_EXP_LEN - i
            exp_biased += arr[i] * (2**power)

        if exp_biased == 0:
            return 0.0

        exponent: int = exp_biased - FLOAT_EXP_BIAS

        mantissa_val: float = 1.0
        for i in range(1 + FLOAT_EXP_LEN, self.bits):
            power = i - FLOAT_EXP_LEN
            mantissa_val += arr[i] * (2**-power)

        result: float = sign * mantissa_val * (2**exponent)
        return result

    def add_ieee754(self, arr1: list[int], arr2: list[int]) -> list[int]:
        sign1: int = arr1[0]
        sign2: int = arr2[0]

        exp1_val: int = sum(
            arr1[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )
        exp2_val: int = sum(
            arr2[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )

        mant1: list[int] = [1] + arr1[1 + FLOAT_EXP_LEN : self.bits]
        mant2: list[int] = [1] + arr2[1 + FLOAT_EXP_LEN : self.bits]

        if exp1_val > exp2_val:
            diff: int = exp1_val - exp2_val
            mant2 = ([0] * diff + mant2)[:FLOAT_MANT_IMPLICIT_LEN]
            exp_res: int = exp1_val
        elif exp2_val > exp1_val:
            diff = exp2_val - exp1_val
            mant1 = ([0] * diff + mant1)[:FLOAT_MANT_IMPLICIT_LEN]
            exp_res: int = exp2_val
        else:
            exp_res = exp1_val

        m1_val: int = sum(
            val * (2 ** (FLOAT_MANT_LEN - i)) for i, val in enumerate(mant1)
        )
        m2_val: int = sum(
            val * (2 ** (FLOAT_MANT_LEN - i)) for i, val in enumerate(mant2)
        )

        if sign1 == sign2:
            m_res_val: int = m1_val + m2_val
            res_sign: int = sign1
        else:
            if m1_val >= m2_val:
                m_res_val = m1_val - m2_val
                res_sign = sign1
            else:
                m_res_val = m2_val - m1_val
                res_sign = sign2

        res_arr: list[int] = self.get_empty_array()
        if m_res_val == 0:
            self.print_result("Сложение IEEE-754", res_arr, 0.0)
            return res_arr

        res_bin: list[int] = []
        temp: int = m_res_val
        while temp > 0:
            res_bin.append(temp % 2)
            temp //= 2
        res_bin.reverse()

        shift: int = len(res_bin) - FLOAT_MANT_IMPLICIT_LEN
        exp_res += shift

        if shift > 0:
            final_mant: list[int] = res_bin[1 : 1 + FLOAT_MANT_LEN]
        elif shift < 0:
            final_mant = (res_bin[1:] + [0] * (-shift))[:FLOAT_MANT_LEN]
        else:
            final_mant = res_bin[1 : 1 + FLOAT_MANT_LEN]

        res_arr[0] = res_sign

        for i in range(FLOAT_EXP_LEN):
            res_arr[FLOAT_EXP_LEN - i] = exp_res % 2
            exp_res //= 2

        for i in range(min(FLOAT_MANT_LEN, len(final_mant))):
            res_arr[1 + FLOAT_EXP_LEN + i] = final_mant[i]

        dec_val: float = self.from_ieee754(res_arr)
        self.print_result("Сложение IEEE-754", res_arr, dec_val)
        return res_arr

    def sub_ieee754(self, arr1: list[int], arr2: list[int]) -> list[int]:
        arr2_neg: list[int] = arr2[:]
        arr2_neg[0] = 1 if arr2[0] == 0 else 0

        print("\n[Вычитание преобразуется в сложение с отрицательным числом]")
        res_arr: list[int] = self.add_ieee754(arr1, arr2_neg)

        dec_val: float = self.from_ieee754(res_arr)
        self.print_result("Итог вычитания IEEE-754", res_arr, dec_val)
        return res_arr

    def mul_ieee754_pure(self, arr1: list[int], arr2: list[int]) -> list[int]:
        res_arr: list[int] = self.get_empty_array()
        res_arr[0] = arr1[0] ^ arr2[0]

        exp1: int = sum(
            arr1[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )
        exp2: int = sum(
            arr2[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )

        if exp1 == 0 or exp2 == 0:
            self.print_result("Умножение IEEE-754", res_arr, 0.0)
            return res_arr

        exp_res: int = exp1 + exp2 - FLOAT_EXP_BIAS

        m1: list[int] = [1] + arr1[1 + FLOAT_EXP_LEN : self.bits]
        m2: list[int] = [1] + arr2[1 + FLOAT_EXP_LEN : self.bits]

        res_m: list[int] = [0] * (FLOAT_MANT_IMPLICIT_LEN * 2)

        for i in range(FLOAT_MANT_LEN, -1, -1):
            if m2[i] == 1:
                shift: int = FLOAT_MANT_LEN - i
                shifted_m1: list[int] = (
                    [0] * (FLOAT_MANT_IMPLICIT_LEN - shift) + m1 + [0] * shift
                )
                res_m = self._add_arrays(res_m, shifted_m1)

        if res_m[0] == 1:
            exp_res += 1
            final_mant: list[int] = res_m[1 : 1 + FLOAT_MANT_LEN]
        else:
            final_mant = res_m[2 : 2 + FLOAT_MANT_LEN]

        for i in range(FLOAT_EXP_LEN, 0, -1):
            res_arr[i] = exp_res % 2
            exp_res //= 2

        for i in range(FLOAT_MANT_LEN):
            res_arr[1 + FLOAT_EXP_LEN + i] = final_mant[i]

        dec_val: float = self.from_ieee754(res_arr)
        self.print_result("Умножение IEEE-754", res_arr, dec_val)
        return res_arr

    def div_ieee754_pure(self, arr1: list[int], arr2: list[int]) -> list[int]:
        res_arr: list[int] = self.get_empty_array()
        res_arr[0] = arr1[0] ^ arr2[0]

        exp1: int = sum(
            arr1[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )
        exp2: int = sum(
            arr2[i] * (2 ** (FLOAT_EXP_LEN - i)) for i in range(1, 1 + FLOAT_EXP_LEN)
        )

        if exp2 == 0:
            raise ZeroDivisionError("Деление на ноль в IEEE-754")
        if exp1 == 0:
            self.print_result("Деление IEEE-754", res_arr, 0.0)
            return res_arr

        exp_res: int = exp1 - exp2 + FLOAT_EXP_BIAS

        m1: list[int] = [1] + arr1[1 + FLOAT_EXP_LEN : self.bits]
        m2: list[int] = [1] + arr2[1 + FLOAT_EXP_LEN : self.bits]

        rem: list[int] = [0] + m1 + [0] * FLOAT_MANT_IMPLICIT_LEN
        divisor: list[int] = [0] + m2 + [0] * FLOAT_MANT_IMPLICIT_LEN
        quotient: list[int] = []

        for _ in range(FLOAT_MANT_IMPLICIT_LEN + 1):
            if self._is_greater_or_equal(rem, divisor):
                rem = self._sub_arrays(rem, divisor)
                quotient.append(1)
            else:
                quotient.append(0)
            rem = rem[1:] + [0]

        if quotient[0] == 1:
            final_mant: list[int] = quotient[1 : 1 + FLOAT_MANT_LEN]
        else:
            final_mant = quotient[2 : 2 + FLOAT_MANT_LEN]
            exp_res -= 1

        for i in range(FLOAT_EXP_LEN, 0, -1):
            res_arr[i] = exp_res % 2
            exp_res //= 2

        for i in range(FLOAT_MANT_LEN):
            res_arr[1 + FLOAT_EXP_LEN + i] = final_mant[i]

        dec_val: float = self.from_ieee754(res_arr)
        self.print_result("Деление IEEE-754", res_arr, dec_val)
        return res_arr
