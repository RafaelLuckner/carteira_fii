import numpy as np
import pandas as pd
from scipy.optimize import minimize

def portfolio_metrics(weights, returns, cov_matrix):
    """Calcula retorno esperado e risco da carteira."""
    expected_return = np.sum(returns * weights)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return expected_return, risk

def optimize_portfolio(returns: pd.DataFrame):
    """Otimiza a carteira usando variância mínima (Markowitz)."""
    num_assets = len(returns.columns)
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    def objective(weights):
        """Função objetivo: minimizar o risco."""
        return portfolio_metrics(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})  # Somatório dos pesos = 1
    bounds = tuple((0, 1) for _ in range(num_assets))  # Sem posições vendidas
    initial_guess = np.ones(num_assets) / num_assets

    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)
    return result.x  # Retorna os pesos ótimos

# Exemplo de uso
if __name__ == "__main__":
    np.random.seed(42)
    data = pd.DataFrame(np.random.randn(100, 4), columns=['FII1', 'FII2', 'FII3', 'FII4'])
    optimal_weights = optimize_portfolio(data)
    print("Pesos ótimos da carteira:", optimal_weights)
