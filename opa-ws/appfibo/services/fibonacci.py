def calculate_fibonacci(n):
    try:
        n = int(n)
        if n <= 0:
            return "O número deve ser maior que 0."
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n):
                a, b = b, a + b
            return b
    except ValueError:
        return "Entrada inválida. Por favor, insira um número inteiro."