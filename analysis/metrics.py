import pandas as pd

def dividend_yield(dividend_per_share: float, price: float) -> float:
    """Calcula o Dividend Yield (DY) de um FII."""
    if price == 0:
        return 0
    return (dividend_per_share / price) * 100

def p_vp(price: float, book_value_per_share: float) -> float:
    """Calcula o Preço sobre Valor Patrimonial (P/VP)."""
    if book_value_per_share == 0:
        return float('inf')
    return price / book_value_per_share

def ffo_yield(ffo_per_share: float, price: float) -> float:
    """Calcula o FFO Yield (Fluxo de Caixa Operacional / Preço)."""
    if price == 0:
        return 0
    return (ffo_per_share / price) * 100

def volatility(prices: pd.Series) -> float:
    """Calcula a volatilidade anualizada dos preços."""
    return prices.pct_change().std() * (252 ** 0.5)

# Exemplo de uso
if __name__ == "__main__":
    print("Dividend Yield:", dividend_yield(1.2, 100))
    print("P/VP:", p_vp(100, 80))
    print("FFO Yield:", ffo_yield(5, 100))
