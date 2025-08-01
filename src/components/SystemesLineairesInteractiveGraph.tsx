import React, { useState } from "react";
import SystemesLineairesGraph from "./SystemesLineairesGraph";

// Helpers pour créer matrice/vecteur modifiables
function createMatrix(rows: number, cols: number, fill = 0): number[][] {
  return Array.from({ length: rows }, () => Array(cols).fill(fill));
}
function createVector(size: number, fill = 0): number[] {
  return Array(size).fill(fill);
}

const defaultA = [
  [4, 1],
  [1, 3],
];
const defaultB = [1, 2];
const defaultX0 = [0, 0];

// Appelle le backend pour obtenir les erreurs de convergence
async function fetchConvergence(A: number[][], b: number[], x0: number[]): Promise<{ jacobi: number[]; gaussSeidel: number[] }> {
  const response = await fetch("http://localhost:8000/api/linear_system/convergence", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ A, b, x0 })
  });
  if (!response.ok) throw new Error("Erreur backend");
  return await response.json();
}

const SystemesLineairesInteractiveGraph: React.FC = () => {
  const [A, setA] = useState<number[][]>(defaultA);
  const [b, setB] = useState<number[]>(defaultB);
  const [x0, setX0] = useState<number[]>(defaultX0);
  const [errors, setErrors] = useState<{ jacobi: number[]; gaussSeidel: number[] }>({ jacobi: [], gaussSeidel: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handlers pour modification matrice/vecteur
  const handleAChange = (i: number, j: number, value: string) => {
    const newA = A.map(row => [...row]);
    newA[i][j] = parseFloat(value) || 0;
    setA(newA);
  };
  const handleBChange = (i: number, value: string) => {
    const newB = [...b];
    newB[i] = parseFloat(value) || 0;
    setB(newB);
  };
  const handleX0Change = (i: number, value: string) => {
    const newX0 = [...x0];
    newX0[i] = parseFloat(value) || 0;
    setX0(newX0);
  };

  const handleCalculer = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchConvergence(A, b, x0);
      setErrors(result);
    } catch (e: any) {
      setError(e.message || "Erreur inconnue");
      setErrors({ jacobi: [], gaussSeidel: [] });
    } finally {
      setLoading(false);
    }
  };


  return (
    <div>
      <div className="flex gap-8 mb-4 flex-wrap">
        <div>
          <b>Matrice A :</b>
          <table className="border border-gray-300 mt-2">
            <tbody>
              {A.map((row, i) => (
                <tr key={i}>
                  {row.map((val, j) => (
                    <td key={j} className="border px-1 py-0.5">
                      <input
                        type="number"
                        value={val}
                        onChange={e => handleAChange(i, j, e.target.value)}
                        className="w-12 text-center"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div>
          <b>Vecteur b :</b>
          <table className="border border-gray-300 mt-2">
            <tbody>
              {b.map((val, i) => (
                <tr key={i}>
                  <td className="border px-1 py-0.5">
                    <input
                      type="number"
                      value={val}
                      onChange={e => handleBChange(i, e.target.value)}
                      className="w-12 text-center"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div>
          <b>Point initial :</b>
          <table className="border border-gray-300 mt-2">
            <tbody>
              {x0.map((val, i) => (
                <tr key={i}>
                  <td className="border px-1 py-0.5">
                    <input
                      type="number"
                      value={val}
                      onChange={e => handleX0Change(i, e.target.value)}
                      className="w-12 text-center"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex flex-col justify-end">
          <button
            onClick={handleCalculer}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mt-2"
          >
            CALCULER
          </button>
        </div>
      </div>
      {loading && <div className="text-blue-600 mb-2">Calcul en cours...</div>}
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <SystemesLineairesGraph jacobiErrors={errors.jacobi} gaussSeidelErrors={errors.gaussSeidel} />
    </div>
  );
};

export default SystemesLineairesInteractiveGraph;
