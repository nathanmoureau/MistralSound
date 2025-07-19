def calib(noise_only_level, signal_only_level):
    if noise_only_level == signal_only_level:
        print("Noisy level = Signal level, dividing by 0.")
        return Null
    a = 1/(signal_only_level - noise_only_level)
    b = noise_only_level/(signal_only_level - noise_only_level)
    print(f"noise_a={a}, noise_b={b}")
    return a,b
