import React, { useState } from "react";
import EquationsNonLineairesGraph from "./EquationsNonLineairesGraph";

// Appelle le backend pour obtenir les erreurs de convergence
async function fetchConvergence(fx: string, x0: number, gx: string): Promise<{ dichotomie: number[]; newton: number[]; pointFixe: number[] }> {
  const response = await fetch("http://localhost:8000/api/nonlinear_equation/convergence", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fx, x0, gx })
  });
  if (!response.ok) {
    const errText = await response.text();
    throw new Error("Erreur backend : " + errText);
  }
  return await response.json();
}

const EquationsNonLineairesInteractiveGraph: React.FC = () => {
  const [fx, setFx] = useState<string>("x^2 - 2");
  const [gx, setGx] = useState<string>("");
  const [x0, setX0] = useState<number>(1.5);
  const [errors, setErrors] = useState<{ dichotomie: number[]; newton: number[]; pointFixe: number[] }>({ dichotomie: [], newton: [], pointFixe: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCalculer = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchConvergence(fx, x0, gx);
      setErrors(result);
    } catch (e: any) {
      setError(e.message || "Erreur inconnue");
      setErrors({ dichotomie: [], newton: [], pointFixe: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex gap-8 mb-4 flex-wrap items-end">
        <div>
          <label className="block font-bold mb-1">Fonction f(x):</label>
          <input
            type="text"
            value={fx}
            onChange={e => setFx(e.target.value)}
            className="border px-2 py-1 rounded w-40"
          />
        </div>
        <div>
          <label className="block font-bold mb-1">Point initial:</label>
          <input
            type="number"
            value={x0}
            onChange={e => setX0(parseFloat(e.target.value) || 0)}
            className="border px-2 py-1 rounded w-24"
          />
        </div>
        <div>
          <label className="block font-bold mb-1">Fonction g(x) (point fixe):</label>
          <input
            type="text"
            value={gx}
            onChange={e => setGx(e.target.value)}
            className="border px-2 py-1 rounded w-40"
            placeholder="ex: sqrt(2) ou 2/x"
          />
        </div>
        <div>
          <button
            onClick={handleCalculer}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            CALCULER
          </button>
        </div>
      </div>
      {loading && <div className="text-blue-600 mb-2">Calcul en cours...</div>}
      {error && (
        <div className="text-red-600 mb-2">
          {/* Analyse intelligente des erreurs pour guider l'étudiant */}
          {(() => {
            if (error.includes('Pas de changement de signe')) {
              return (
                <>
                  <b>Astuce :</b> Pour utiliser la méthode de dichotomie, il faut que la fonction f(x) prenne des valeurs de signes opposés aux deux extrémités de l’intervalle testé. Si ce n’est pas le cas, essaie un autre point initial ou un autre intervalle.
                </>
              );
            }
            if (error.match(/point initial.*non valide|division par zéro|hors domaine|domain/i)) {
              return (
                <>
                  <b>Erreur :</b> Le point initial choisi n’est pas valide pour cette fonction. Vérifie que la valeur saisie est autorisée (pas de division par zéro, racine carrée d’un nombre négatif, etc.).
                </>
              );
            }
            if (error.match(/fonction g\(x\).*non valide|g\(x\).*erreur|point fixe.*non valide/i)) {
              return (
                <>
                  <b>Erreur :</b> La fonction g(x) saisie n’est pas valide ou provoque une erreur de calcul. Vérifie la syntaxe et assure-toi que g(x) est bien définie pour le point initial choisi.
                </>
              );
            }
            if (error.match(/n’a pas convergé|non convergence|convergence.*pas atteinte/i)) {
              return (
                <>
                  <b>Astuce :</b> La méthode n’a pas convergé vers une solution après le nombre maximal d’itérations. Essaie un autre point initial ou une autre méthode.
                </>
              );
            }
            if (error.match(/erreur de syntaxe|syntax|unexpected|invalid/i)) {
              return (
                <>
                  <b>Erreur :</b> Il y a une erreur de syntaxe dans la fonction saisie. Vérifie l’écriture de ta fonction (ex : x^2 au lieu de x**2, parenthèses manquantes, etc.).
                </>
              );
            }
            if (error.match(/hors domaine|not defined|math domain/i)) {
              return (
                <>
                  <b>Erreur :</b> La fonction n’est pas définie pour certaines valeurs de l’intervalle choisi. Vérifie que toutes les valeurs testées sont dans le domaine de définition de la fonction.
                </>
              );
            }
            // Message générique si non reconnu
            return error;
          })()}
        </div>
      )}
      <EquationsNonLineairesGraph
        dichotomie={errors.dichotomie}
        newton={errors.newton}
        pointFixe={errors.pointFixe}
      />
    </div>
  );
};

export default EquationsNonLineairesInteractiveGraph;
