import numpy as np

def lu_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    steps = []

    for i in range(n):
        # Upper Triangular
        for k in range(i, n):
            sum_val = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_val
        steps.append(f"Step {i+1}: Calculated row {i+1} of U.")

        # Lower Triangular
        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                sum_val = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (A[k][i] - sum_val) / U[i][i]
        steps.append(f"Step {i+1}: Calculated column {i+1} of L.")

    return L.tolist(), U.tolist(), steps

def gaussian_elimination(A, b):
    n = len(A)
    M = np.array(A, dtype=float)
    b_vec = np.array(b, dtype=float).reshape(n, 1)
    aug_matrix = np.hstack([M, b_vec])
    steps = [f"Initial augmented matrix:\n{aug_matrix}"]

    for i in range(n):
        pivot = aug_matrix[i][i]
        if pivot == 0:
            raise ValueError("Pivot is zero, cannot proceed.")
        
        for j in range(i + 1, n):
            ratio = aug_matrix[j][i] / pivot
            aug_matrix[j] = aug_matrix[j] - ratio * aug_matrix[i]
            steps.append(f"R{j+1} -> R{j+1} - {ratio:.2f} * R{i+1}\n{aug_matrix}")

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (aug_matrix[i][-1] - np.dot(aug_matrix[i][i+1:n], x[i+1:n])) / aug_matrix[i][i]
        steps.append(f"Calculated x[{i+1}] = {x[i]:.2f}")

    return x.tolist(), steps

def lu_solve(A, b):
    # Décomposition LU
    L, U, steps = lu_decomposition(A)
    n = len(A)
    b = np.array(b)
    # Résolution LY = b (descente)
    Y = np.zeros(n)
    steps_res = []
    for i in range(n):
        Y[i] = b[i] - np.dot(L[i, :i], Y[:i])
        steps_res.append(f"Y[{i+1}] = {Y[i]}")
    # Résolution UX = Y (remontée)
    X = np.zeros(n)
    for i in range(n-1, -1, -1):
        X[i] = (Y[i] - np.dot(U[i, i+1:], X[i+1:])) / U[i, i]
        steps_res.append(f"X[{i+1}] = {X[i]}")
    return L.tolist(), U.tolist(), steps + steps_res, X.tolist()