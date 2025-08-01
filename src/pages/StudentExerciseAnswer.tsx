import React, { useState, useMemo } from "react";
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

interface StudentExerciseAnswerProps {
  question: string;
  solution: string;
}

const renderWithLatex = (content: string) => {
  if (!content) return null;
  
  // D'abord, gérer les formules en mode bloc (entre $$...$$)
  const blockMathParts = content.split(/(\$\$[^$]+\$\$)/g);
  
  return blockMathParts.map((part, blockIndex) => {
    // Si c'est une formule en mode bloc (commence et finit par $$)
    if (part.startsWith('$$') && part.endsWith('$$')) {
      const formula = part.slice(2, -2).trim();
      return <BlockMath key={`block-${blockIndex}`} math={formula} />;
    }
    
    // Sinon, chercher les formules en ligne dans le texte
    const lineParts = part.split(/([^\\]?\$[^$\s]+\$)/g);
    
    return (
      <span key={`text-${blockIndex}`}>
        {lineParts.map((fragment, lineIndex) => {
          // Si c'est une formule en ligne (commence par $ et finit par $)
          if (fragment.match(/[^\\]?\$[^$\s]+\$/)) {
            // Gérer le cas où il y a un caractère avant le $
            if (fragment[0] !== '$') {
              const before = fragment[0];
              const formula = fragment.slice(1);
              return (
                <React.Fragment key={`frag-${lineIndex}`}>
                  {before}<InlineMath math={formula.slice(1, -1)} />
                </React.Fragment>
              );
            }
            return <InlineMath key={`inline-${lineIndex}`} math={fragment.slice(1, -1)} />;
          }
          // Sinon, retourner le texte tel quel
          return fragment;
        })}
      </span>
    );
  });
};

export default function StudentExerciseAnswer({ question, solution }: StudentExerciseAnswerProps) {
  const [studentAnswer, setStudentAnswer] = useState("");
  const [showSolution, setShowSolution] = useState(false);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    // Just clear the textarea for now
    setStudentAnswer("");
  };

  // Rendu de la question avec support LaTeX
  const renderedQuestion = useMemo(() => renderWithLatex(question), [question]);
  
  // Rendu de la solution avec support LaTeX (si disponible)
  const renderedSolution = useMemo(() => 
    solution ? renderWithLatex(solution) : null
  , [solution]);

  return (
    <div className="p-6 border rounded-lg bg-white shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Énoncé :</h3>
        <div className="prose max-w-none">
          {renderedQuestion}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mb-6">
        <label htmlFor="answer" className="block text-sm font-medium text-gray-700 mb-2">
          Votre réponse :
        </label>
        <textarea
          id="answer"
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          rows={4}
          value={studentAnswer}
          onChange={e => setStudentAnswer(e.target.value)}
          placeholder="Écrivez votre réponse ici..."
        />
        <div className="mt-4 flex justify-end">
          <button
            type="submit"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={!studentAnswer.trim()}
          >
            Soumettre
          </button>
        </div>
      </form>

      {solution && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <button
            onClick={() => setShowSolution(!showSolution)}
            className="text-sm font-medium text-blue-600 hover:text-blue-800 focus:outline-none"
          >
            {showSolution ? 'Masquer la solution' : 'Afficher la solution'}
          </button>
          
          {showSolution && (
            <div className="mt-3 p-4 bg-blue-50 rounded-md">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Solution :</h4>
              <div className="prose max-w-none">
                {renderedSolution}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}