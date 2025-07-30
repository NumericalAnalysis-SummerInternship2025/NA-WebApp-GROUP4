from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import List, Optional, Literal
from services import gaussian_elimination, lu_decomposition

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatrixRequest(BaseModel):
    matrix: List[List[float]]
    vector: Optional[List[float]] = None
    method: Optional[Literal["gauss", "lu", "jacobi", "gauss-seidel"]] = None

@app.post("/matrix/determinant")
def determinant(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        det = float(np.linalg.det(mat))
        return {"result": det}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/matrix/inverse")
def inverse(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        inv = np.linalg.inv(mat)
        return {"result": inv.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/matrix/transpose")
def transpose(req: MatrixRequest):
    try:
        mat = np.array(req.matrix)
        t = mat.T
        return {"result": t.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/matrix/norm")
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

@app.post("/matrix/product")
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

# Résolution de Ax = b (Gauss, LU, Jacobi, Gauss-Seidel)
@app.post("/system/solve")
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
            L, U, steps = lu_decomposition(mat)
            return {"method": method, "steps": steps, "L": L, "U": U}
        elif method == "jacobi":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            # Jacobi iterative method
            n = len(mat)
            x = np.zeros(n)
            steps = [f"Initial guess: {x.tolist()}"]
            max_iter = 50
            tol = 1e-8
            for it in range(max_iter):
                x_new = np.zeros(n)
                for i in range(n):
                    s = sum(mat[i][j] * x[j] for j in range(n) if j != i)
                    x_new[i] = (b[i] - s) / mat[i][i]
                err = np.linalg.norm(x_new - x, 2)
                steps.append(f"Iter {it+1}: {x_new.tolist()} (err={err})")
                if err < tol:
                    break
                x = x_new
            return {"method": method, "steps": steps, "solution": x.tolist()}
        elif method == "gauss-seidel":
            if b is None:
                raise HTTPException(status_code=400, detail="Le vecteur b est requis.")
            # Gauss-Seidel iterative method
            n = len(mat)
            x = np.zeros(n)
            steps = [f"Initial guess: {x.tolist()}"]
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
                if err < tol:
                    break
                x = x_new
            return {"method": method, "steps": steps, "solution": x.tolist()}
        else:
            raise HTTPException(status_code=400, detail="Méthode non supportée.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
