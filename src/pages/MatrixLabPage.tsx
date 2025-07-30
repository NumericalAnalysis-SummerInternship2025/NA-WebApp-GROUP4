import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

function generateEmptyMatrix(rows: number, cols: number): number[][] {
  return Array.from({ length: rows }, () => Array(cols).fill(0));
}

export default function MatrixLabPage() {
  const [rows, setRows] = useState(2);
  const [cols, setCols] = useState(2);
  const [matrix, setMatrix] = useState<number[][]>(generateEmptyMatrix(2, 2));
  const [vectorB, setVectorB] = useState<number[]>(Array(2).fill(0));
  const [result, setResult] = useState<string>("");
  const [solveMethod, setSolveMethod] = useState("gauss");
  const [loading, setLoading] = useState(false);
  const [isVideoOpen, setIsVideoOpen] = useState(false);

  const handleMatrixChange = (i: number, j: number, value: string) => {
    const newMatrix = matrix.map((row, rowIdx) =>
      row.map((cell, colIdx) => (rowIdx === i && colIdx === j ? Number(value) : cell))
    );
    setMatrix(newMatrix);
  };

  const handleSizeChange = (newRows: number, newCols: number) => {
    setRows(newRows);
    setCols(newCols);
    setMatrix(generateEmptyMatrix(newRows, newCols));
    setVectorB(Array(newRows).fill(0));
    setResult("");
  };

  // --- Opérations (API backend à connecter) ---
  const handleOperation = async (op: string) => {
    setLoading(true);
    setResult("");
    try {
      const resp = await fetch(`http://localhost:8000/matrix/${op}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matrix }),
      });
      const data = await resp.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (e) {
      setResult("Erreur de connexion au backend.");
    }
    setLoading(false);
  };

  // --- Produit Ax ---
  const handleProductAx = async () => {
    setLoading(true);
    setResult("");
    try {
      const resp = await fetch(`http://localhost:8000/matrix/product`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matrix, vector: vectorB }),
      });
      const data = await resp.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (e) {
      setResult("Erreur de connexion au backend.");
    }
    setLoading(false);
  };

  // --- Résolution Ax=b ---
  const handleSolve = async () => {
    setLoading(true);
    setResult("");
    try {
        const resp = await fetch(`http://localhost:8000/system/solve`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ matrix, vector: vectorB, method: solveMethod }),
        });
        const data = await resp.json();
        setResult(JSON.stringify(data, null, 2));
    } catch (e) {
      setResult("Erreur de connexion au backend.");
    }
    setLoading(false);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Laboratoire de Matrices</h2>
      <div className="flex gap-4 mb-4 items-center">
        <span>Taille :</span>
        <select value={rows} onChange={e => handleSizeChange(Number(e.target.value), cols)}>
          {[2,3,4,5,6].map(n => <option key={n} value={n}>{n}</option>)}
        </select>
        <span>x</span>
        <select value={cols} onChange={e => handleSizeChange(rows, Number(e.target.value))}>
          {[2,3,4,5,6].map(n => <option key={n} value={n}>{n}</option>)}
        </select>
      </div>
      <table className="mb-4">
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) => (
                <td key={j}>
                  <input
                    type="number"
                    value={cell}
                    onChange={e => handleMatrixChange(i, j, e.target.value)}
                    className="w-16 border rounded px-1 py-1 text-center"
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex gap-2 mb-4 flex-wrap items-center">
        <Button onClick={() => handleOperation("determinant")} disabled={loading}>Déterminant</Button>
        <Dialog open={isVideoOpen} onOpenChange={setIsVideoOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" className="ml-2">
              Voir vidéo explicatif
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl">
            <DialogHeader>
              <DialogTitle>Explication du Déterminant</DialogTitle>
            </DialogHeader>
            <div className="w-full aspect-video">
              <video 
                src="http://localhost:8000/static/videos/manim_determinantettranspose/1080p60/Ma.mp4" 
                controls 
                autoPlay
                className="w-full h-full rounded-md"
              >
                Votre navigateur ne supporte pas la lecture de vidéos.
              </video>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <div className="mb-4 flex gap-2 items-center">
        <span>Vecteur b :</span>
        {vectorB.map((val, idx) => (
          <input
            key={idx}
            type="number"
            value={val}
            onChange={e => {
              const newB = [...vectorB];
              newB[idx] = Number(e.target.value);
              setVectorB(newB);
            }}
            className="w-16 border rounded px-1 py-1 text-center"
          />
        ))}
        <Button onClick={handleProductAx} disabled={loading}>Produit Ax</Button>
      </div>
      <div className="mb-4 flex gap-2 items-center">
        <span>Méthode :</span>
        <select value={solveMethod} onChange={e => setSolveMethod(e.target.value)} className="border rounded px-2 py-1">
          <option value="gauss">Gauss</option>
          <option value="lu">LU</option>
          <option value="jacobi">Jacobi</option>
          <option value="gauss-seidel">Gauss-Seidel</option>
        </select>
        <Button onClick={handleSolve} disabled={loading}>Résoudre Ax=b</Button>
      </div>
      {loading && <div className="text-blue-600">Calcul en cours...</div>}
      {result && (() => {
        let parsed: any;
        try {
          parsed = JSON.parse(result);
        } catch {
          return (
            <div className="mt-4 p-4 border rounded bg-white">
              <h4 className="font-semibold mb-2">Résultat</h4>
              <pre className="whitespace-pre-wrap text-sm">{result}</pre>
            </div>
          );
        }
        if (parsed.error || parsed.detail) {
          return (
            <div className="mt-4 p-4 border rounded bg-red-100 text-red-800">
              <b>Erreur :</b> {parsed.error || parsed.detail}
            </div>
          );
        }
          return (
            <div className="mt-4 p-4 border rounded bg-white">
            <h4 className="font-semibold mb-2">Résultat</h4>
            {parsed.solution && (
              <div className="mb-2">
                <b>Solution :</b> [{parsed.solution.map((v: number) => v.toFixed(6)).join(', ')}]
              </div>
            )}
            {parsed.L && parsed.U && (
                <div className="mb-2">
                <b>Matrice L :</b>
                <pre className="whitespace-pre-wrap text-xs">{JSON.stringify(parsed.L, null, 2)}</pre>
                <b>Matrice U :</b>
                <pre className="whitespace-pre-wrap text-xs">{JSON.stringify(parsed.U, null, 2)}</pre>
                </div>
              )}
            {parsed.convergence && (
              <div className="mb-2">
                <b>Convergence (erreur à chaque itération) :</b>
                <ul className="list-disc ml-6">
                  {parsed.convergence.map((err: number, i: number) => (
                    <li key={i}>Itération {i + 1} : {err.toExponential(2)}</li>
                  ))}
                </ul>
                </div>
              )}
              {parsed.steps && (
                <div className="mb-2">
                  <b>Étapes de résolution :</b>
                <ul className="list-decimal ml-6">
                  {parsed.steps.map((s: string, i: number) => <li key={i}>{s}</li>)}
                  </ul>
                </div>
              )}
            {!parsed.solution && !parsed.steps && (
            <pre className="whitespace-pre-wrap text-sm">{result}</pre>
            )}
          </div>
        );
      })()}

    </div>
  );
}
