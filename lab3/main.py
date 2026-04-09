from source.Lab3Synthesizer import Lab3Synthesizer

if __name__ == "__main__":
    synth = Lab3Synthesizer()

    print("--- 1. ОДС-3 (Выходные функции в СДНФ) ---")
    ods3 = synth.synthesize_ods3()
    for k, v in ods3.items():
        print(f"{k} = {v}")

    print("\n--- 2. Сумматор Gray BCD (Смещение n=1) ---")
    gray_adder = synth.synthesize_gray_bcd_adder()
    for k, v in gray_adder.items():
        print(f"{k} = {v}")

    print("\n--- 3. Вычитающий счетчик на Т-триггерах ---")
    counter = synth.synthesize_down_counter()
    for k, v in counter.items():
        print(f"{k} = {v}")
