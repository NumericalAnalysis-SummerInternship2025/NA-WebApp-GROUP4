import React, { useState } from "react";
import { Button } from "@/components/ui/button";

// Génère une matrice aléatoire de taille n x m
function generateRandomMatrix(rows: number, cols: number): number[][] {
  return Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => Math.floor(Math.random() * 21) - 10)
  );
}

const MIN_SIZE = 2;
const MAX_SIZE = 6;

export default function MatrixLab() {
  const [rows, setRows] = useState(2);
  const [cols, setCols] = useState(2);
  const [matrix, setMatrix] = useState<number[][]>(generateRandomMatrix(2, 2));
  const [result, setResult] = useState<string>("");
  const [vectorX, setVectorX] = useState<string>("");
  const [vectorB, setVectorB] = useState<string>("");
  const [solveMethod, setSolveMethod] = useState<string>("gauss");

  // Met à jour une cellule
  const handleCellChange = (i: number, j: number, value: string) => {
    const newMatrix = matrix.map((row, rowIdx) =>
      row.map((cell, colIdx) => (rowIdx === i && colIdx === j ? Number(value) : cell))
    );
    setMatrix(newMatrix);
  };

  // Change la taille de la matrice et réinitialise
  const handleSizeChange = (newRows: number, newCols: number) => {
    setRows(newRows);
    setCols(newCols);
    setMatrix(generateRandomMatrix(newRows, newCols));
  };

  // Génère une nouvelle matrice aléatoire
  const handleRandom = () => {
    setMatrix(generateRandomMatrix(rows, cols));
  };

  // Gestion des opérations matricielles
  const handleOperation = async (type: string) => {
    if (type === 'determinant') {
      setResult('Calcul en cours...');
      try {
        // Vérifier que la matrice est carrée
        if (rows !== cols) {
          setResult('Erreur : La matrice doit être carrée pour calculer le déterminant');
          return;
        }

        const response = await fetch('http://127.0.0.1:8000/matrix/determinant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ matrix })
        });

        if (!response.ok) {
          const err = await response.text();
          setResult('Erreur : ' + err);
          return;
        }

        const data = await response.json();
        setResult(`Déterminant = ${data.result}`);
      } catch (e) {
        setResult('Erreur lors du calcul : ' + e);
      }
      return;
    }
    
    // Autres opérations...
    setResult(`Opération non implémentée : ${type}`);
  };

  // Résolution de système linéaire
  const handleSolve = async () => {
    // Convertir le vecteur b en tableau de nombres
    const b = vectorB.split(',').map(x => Number(x.trim()));
    if (b.length !== matrix.length) {
      setResult("Erreur : la taille de b ne correspond pas au nombre de lignes de la matrice.");
      return;
    }

    setResult("Calcul en cours...");

    let method = solveMethod;
    // Adapter le nom pour l'API si besoin
    if (method === "gauss-seidel") method = "gauss-seidel";
    if (method === "jacobi") method = "jacobi";
    if (method === "gauss") method = "gauss";
    if (method === "lu") method = "lu";

    try {
      const response = await fetch("http://127.0.0.1:8000/system/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matrix, vector: b, method }),
      });
      
      if (!response.ok) {
        const err = await response.text();
        setResult("Erreur backend : " + err);
        return;
      }
      
      const data = await response.json();
      let display = "";
      if (data.solution) {
        display += `Solution : ${JSON.stringify(data.solution)}\n`;
      }
      if (data.L && data.U) {
        display += `L : ${JSON.stringify(data.L)}\nU : ${JSON.stringify(data.U)}\n`;
      }
      if (data.steps) {
        display += `\nÉtapes :\n${data.steps.join("\n")}`;
      }
      setResult(display);
    } catch (e) {
      setResult("Erreur réseau : " + e);
    }
  };



  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Laboratoire de Matrices Dynamiques</h2>
      <div className="flex gap-4 items-center">
        <label>Taille :</label>
        <select value={rows} onChange={e => handleSizeChange(Number(e.target.value), cols)}>
          {[...Array(MAX_SIZE - MIN_SIZE + 1)].map((_, i) => (
            <option key={i + MIN_SIZE} value={i + MIN_SIZE}>{i + MIN_SIZE}</option>
          ))}
        </select>
        <span> × </span>
        <select value={cols} onChange={e => handleSizeChange(rows, Number(e.target.value))}>
          {[...Array(MAX_SIZE - MIN_SIZE + 1)].map((_, i) => (
            <option key={i + MIN_SIZE} value={i + MIN_SIZE}>{i + MIN_SIZE}</option>
          ))}
        </select>
        <Button onClick={handleRandom} variant="secondary">Générer Aléatoirement</Button>
      </div>
      <div className="overflow-x-auto">
        <table className="border border-gray-400">
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td key={j} className="border border-gray-300 p-1">
                    <input
                      type="number"
                      value={cell}
                      onChange={e => handleCellChange(i, j, e.target.value)}
                      className="w-16 text-center border rounded"
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Opérations matricielles */}
      <div className="space-y-2">
        <div className="flex flex-wrap gap-2">
          <Button onClick={() => handleOperation('determinant')}>Déterminant</Button>
        </div>
        <div className="flex gap-2 items-center mt-2">
          <span>Produit Ax&nbsp;:</span>
          <input
            type="text"
            placeholder="Ex: 1,2,3"
            value={vectorX}
            onChange={e => setVectorX(e.target.value)}
            className="w-32 border rounded px-2 py-1"
          />
          <Button onClick={() => handleOperation('product-ax')}>Calculer Ax</Button>
        </div>
      </div>

      {/* Résolution de Ax = b */}
      <div className="mt-6 p-4 border rounded bg-gray-50">
        <h3 className="font-semibold mb-2">Résoudre Ax = b</h3>
        <div className="flex gap-2 items-center mb-2">
          <span>b =</span>
          <input
            type="text"
            placeholder="Ex: 4,5,6"
            value={vectorB}
            onChange={e => setVectorB(e.target.value)}
            className="w-32 border rounded px-2 py-1"
          />
          <span>Méthode :</span>
          <select value={solveMethod} onChange={e => setSolveMethod(e.target.value)} className="border rounded px-2 py-1">
            <option value="gauss">Gauss</option>
            <option value="lu">LU</option>
            <option value="jacobi">Jacobi</option>
            <option value="gauss-seidel">Gauss-Seidel</option>
          </select>
          <Button onClick={handleSolve}>Résoudre</Button>
        </div>
        {/* Affichage des étapes, matrices, approximations, graphique de convergence à venir */}
      </div>

      {/* Affichage du résultat d'opération */}
      {result && (
        <div className="mt-4 p-4 border rounded bg-white">
          <h4 className="font-semibold mb-2">Résultat</h4>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
      )}
    </div>
  );
}



