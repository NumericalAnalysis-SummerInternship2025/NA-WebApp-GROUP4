from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
import numpy as np
from services import gaussian_elimination, lu_decomposition, lu_solve

router = APIRouter()

# --- Systèmes linéaires ---
class LinearSystemRequest(BaseModel):
    A: List[List[float]]
    b: List[float]
    x0: List[float]

@router.post("/api/linear_system/convergence")
def linear_system_convergence(data: LinearSystemRequest):
    import numpy as np
    A = np.array(data.A, dtype=float)
    b = np.array(data.b, dtype=float)
    x0 = np.array(data.x0, dtype=float)
    n = len(b)
    max_iter = 50
    tol = 1e-8
    errors_jacobi = []
    errors_gs = []
    # Jacobi
    x_jac = x0.copy()
    for _ in range(max_iter):
        x_new = x_jac.copy()
        for i in range(n):
            s = sum(A[i, j] * x_jac[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        err = np.linalg.norm(x_new - x_jac, 2)
        errors_jacobi.append(float(err))
        if err < tol:
            break
        x_jac = x_new
    # Gauss-Seidel
    x_gs = x0.copy()
    for _ in range(max_iter):
        x_new = x_gs.copy()
        for i in range(n):
            s1 = sum(A[i, j] * x_new[j] for j in range(i))
            s2 = sum(A[i, j] * x_gs[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        err = np.linalg.norm(x_new - x_gs, 2)
        errors_gs.append(float(err))
        if err < tol:
            break
        x_gs = x_new
    return {"jacobi": errors_jacobi, "gaussSeidel": errors_gs}

# --- Équations non-linéaires ---
class NonLinearRequest(BaseModel):
    fx: str
    x0: float
    gx: Optional[str] = None

from fastapi import HTTPException

@router.post("/api/nonlinear_equation/convergence")
def nonlinear_convergence(data: NonLinearRequest):
    import numpy as np
    import math
    from asteval import Interpreter
    
    aeval = Interpreter()
    aeval.symtable['np'] = np
    aeval.symtable['math'] = math

    fx_str = data.fx.replace('^', '**').strip()
    x0 = float(data.x0)
    max_iter = 30
    tol = 1e-10

    def safe_eval(expr, x_val):
        aeval.symtable['x'] = x_val
        try:
            return aeval.eval(expr)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur d'évaluation: {e}")

    # Newton
    def df(expr, x, h=1e-6):
        return (safe_eval(expr, x + h) - safe_eval(expr, x - h)) / (2 * h)

    x_newton = x0
    errors_newton = []
    for _ in range(max_iter):
        fval = safe_eval(fx_str, x_newton)
        dfdx = df(fx_str, x_newton)
        if abs(dfdx) < 1e-12:
            break
        x_next = x_newton - fval / dfdx
        err = abs(x_next - x_newton)
        errors_newton.append(float(err))
        if err < tol:
            break
        x_newton = x_next

    # Point fixe
    errors_pf = []
    x_pf = x0
    gx_str = data.gx.strip() if data.gx else f"x - ({fx_str})"
    
    for _ in range(max_iter):
        g = safe_eval(gx_str, x_pf)
        if abs(g) > 1e6:
            raise HTTPException(status_code=400, detail="La méthode du point fixe diverge.")
        err = abs(g - x_pf)
        errors_pf.append(float(err))
        if err < tol:
            break
        x_pf = g

    # Dichotomie
    errors_dicho = []
    a, b = x0 - 1, x0 + 1
    fa, fb = safe_eval(fx_str, a), safe_eval(fx_str, b)

    if fa * fb > 0:
        raise HTTPException(status_code=400, detail="Pas de changement de signe trouvé pour la méthode de dichotomie dans l'intervalle [x0-1, x0+1].")

    for _ in range(max_iter):
        m = (a + b) / 2
        fm = safe_eval(fx_str, m)
        errors_dicho.append(abs(b - a))
        if abs(fm) < tol or abs(b - a) < tol:
            break
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return {
        "dichotomie": errors_dicho,
        "newton": errors_newton,
        "pointFixe": errors_pf
    }

class MatrixRequest(BaseModel):
    matrix: List[List[float]]
    vector: Optional[List[float]] = None
    method: Optional[Literal["gauss", "lu", "jacobi", "gauss-seidel"]] = None

@router.post("/matrix/determinant")
def determinant(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        det = float(np.linalg.det(mat))
        return {"result": det}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/matrix/inverse")
def inverse(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        inv = np.linalg.inv(mat)
        return {"result": inv.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/matrix/transpose")
def transpose(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        t = mat.T
        return {"result": t.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/matrix/norm")
def norm(req: MatrixRequest, type: str = "fro"):
    try:
        mat = np.array(req.matrix)
        if type == "1":
            n = float(np.linalg.norm(mat, 1))
        elif type == "2":
            n = float(np.linalg.norm(mat, 2))
        elif type == "inf":
            n = float(np.linalg.norm(mat, np.inf))
        else:
            n = float(np.linalg.norm(mat, "fro"))
        return {"result": n}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/matrix/product")
def product(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        if req.vector is None:
            raise ValueError("Le vecteur n'est pas fourni.")
        vec = np.array(req.vector)
        prod = mat.dot(vec)
        return {"result": prod.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/system/solve")
def solve(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        b = np.array(req.vector) if req.vector is not None else None
        method = req.method
        if method == "gauss":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            solution, steps = gaussian_elimination(mat, b)
            return {"method": method, "steps": steps, "solution": solution}
        elif method == "lu":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            L, U, steps, solution = lu_solve(mat, b)
            return {"method": method, "steps": steps, "L": L, "U": U, "solution": solution}
        elif method == "jacobi":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            n = len(mat)
            x = np.zeros(n)
            steps = [f"Initial guess: {x.tolist()}"]
            convergence = []
            max_iter = 50
            tol = 1e-8
            for it in range(max_iter):
                x_new = np.zeros(n)
                for i in range(n):
                    s = sum(mat[i][j] * x[j] for j in range(n) if j != i)
                    x_new[i] = (b[i] - s) / mat[i][i]
                err = np.linalg.norm(x_new - x, 2)
                steps.append(f"Iter {it+1}: {x_new.tolist()} (err={err})")
                convergence.append(float(err))
                if err < tol:
                    break
                x = x_new
            return {"method": method, "steps": steps, "solution": x.tolist(), "convergence": convergence}
        elif method == "gauss-seidel":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            n = len(mat)
            x = np.zeros(n)
            steps = [f"Initial guess: {x.tolist()}"]
            convergence = []
            max_iter = 50
            tol = 1e-8
            for it in range(max_iter):
                x_new = x.copy()
                for i in range(n):
                    s1 = sum(mat[i][j] * x_new[j] for j in range(i))
                    s2 = sum(mat[i][j] * x[j] for j in range(i+1, n))
                    x_new[i] = (b[i] - s1 - s2) / mat[i][i]
                err = np.linalg.norm(x_new - x, 2)
                steps.append(f"Iter {it+1}: {x_new.tolist()} (err={err})")
                convergence.append(float(err))
                if err < tol:
                    break
                x = x_new
            return {"method": method, "steps": steps, "solution": x.tolist(), "convergence": convergence}
        else:
            raise HTTPException(status_code=400, detail="Méthode non supportée.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
