import React, { useState, useEffect, useMemo } from "react";
import { CheckCircle, XCircle, Clock, RotateCcw } from "lucide-react";

// Données d'examen séparées du composant
// Supprimer examData local et utiliser le backend

const chapitres = ["Tous", "Chapitre 1", "Chapitre 2", "Chapitre 3"];
const tps = ["Tous", "TP1", "TP2", "TP3"];

// Validation améliorée avec différents niveaux de flexibilité
function isCorrect(studentAnswer: string, expectedAnswers: string[]): boolean {
  if (!studentAnswer || !studentAnswer.trim()) return false;
  const cleanAnswer = studentAnswer.trim().toLowerCase();
  return expectedAnswers.some(expected => {
    const cleanExpected = expected.trim().toLowerCase();
    // Correspondance exacte
    if (cleanAnswer === cleanExpected) return true;
    // Correspondance sans espaces/ponctuation
    const normalizeForComparison = (str: string) =>
      str.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
    if (normalizeForComparison(cleanAnswer) === normalizeForComparison(cleanExpected)) return true;
    // Vérification de mots-clés essentiels
    const answerWords = cleanAnswer.split(/\s+/);
    const expectedWords = cleanExpected.split(/\s+/);
    if (expectedWords.length <= 3) {
      return expectedWords.every(word =>
        answerWords.some(answerWord => answerWord.includes(word) || word.includes(answerWord))
      );
    }
    return false;
  });
}

type Exercise = {
  id: string;
  question: string;
  expectedAnswers: string[];
  feedback: string;
  points: number;
};

type ExerciseCardProps = {
  exercise: Exercise;
  isValidated: boolean;
  studentAnswer: string;
  onAnswerChange: (id: string, value: string) => void;
  onValidate: (exercise: Exercise) => void;
  feedback: string;
};

const ExerciseCard: React.FC<ExerciseCardProps> = ({ exercise, isValidated, studentAnswer, onAnswerChange, onValidate, feedback }) => {
  const getStatusIcon = () => {
    if (!isValidated) return <Clock className="w-5 h-5 text-gray-400" />;
    if (feedback.includes("Bonne réponse")) return <CheckCircle className="w-5 h-5 text-green-500" />;
    return <XCircle className="w-5 h-5 text-red-500" />;
  };

  const getStatusColor = () => {
    if (!isValidated) return "border-gray-300";
    if (feedback.includes("Bonne réponse")) return "border-green-300 bg-green-50";
    return "border-red-300 bg-red-50";
  };

  return (
    <div className={`p-6 border-2 rounded-lg shadow-sm ${getStatusColor()}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="font-mono text-sm whitespace-pre-line text-gray-800 mb-3">
            {exercise.question}
          </div>
          <div className="text-sm text-gray-600">
            Points: {exercise.points}
          </div>
        </div>
        <div className="ml-4 flex items-center">
          {getStatusIcon()}
        </div>
      </div>
      <div className="space-y-3">
        <textarea
          value={studentAnswer || ""}
          onChange={(e) => onAnswerChange(exercise.id, e.target.value)}
          disabled={isValidated}
          className={`w-full p-3 border rounded-lg resize-none h-24 ${
            isValidated 
              ? 'bg-gray-100 cursor-not-allowed' 
              : 'bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
          }`}
          placeholder="Votre réponse ici..."
        />
        <div className="flex justify-between items-center">
          <button
            onClick={() => onValidate(exercise)}
            disabled={isValidated || !studentAnswer?.trim()}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              isValidated 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : studentAnswer?.trim()
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {isValidated ? 'Validé' : 'Valider'}
          </button>
        </div>
        {feedback && (
          <div className={`p-3 rounded-lg ${
            feedback.includes("Bonne réponse") 
              ? 'bg-green-100 text-green-800 border border-green-300' 
              : 'bg-red-100 text-red-800 border border-red-300'
          }`}>
            {feedback}
          </div>
        )}
      </div>
    </div>
  );
};

const ModeExam: React.FC = () => {
  const [selectedChapitre, setSelectedChapitre] = useState<string>("Tous");
  const [selectedTP, setSelectedTP] = useState<string>("Tous");
  const [studentAnswers, setStudentAnswers] = useState<Record<string, string>>({});
  const [validatedAnswers, setValidatedAnswers] = useState<Set<string>>(new Set());
  const [feedbacks, setFeedbacks] = useState<Record<string, string>>({});
  const [sessionStarted, setSessionStarted] = useState(false);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch exercises from backend when filters change
  useEffect(() => {
    setLoading(true);
    let url = 'http://localhost:8000/exercises/filter';
    const params: string[] = [];
    if (selectedChapitre && selectedChapitre !== 'Tous') params.push(`chapter=${encodeURIComponent(selectedChapitre)}`);
    if (selectedTP && selectedTP !== 'Tous') params.push(`tp=${encodeURIComponent(selectedTP)}`);
    if (params.length > 0) url += '?' + params.join('&');
    fetch(url)
      .then(res => res.json())
      .then(data => setExercises(data))
      .catch(() => setExercises([]))
      .finally(() => setLoading(false));
  }, [selectedChapitre, selectedTP]);

  // Calcul des exercices filtrés avec useMemo pour optimisation
  const filteredExercises: Exercise[] = useMemo(() => exercises, [exercises]);

  // Calcul du score total
  const { currentScore, totalScore } = useMemo(() => {
    const total = filteredExercises.reduce((sum, ex) => sum + ex.points, 0);
    const current = filteredExercises.reduce((sum, ex) => {
      if (validatedAnswers.has(ex.id) && feedbacks[ex.id]?.includes("Bonne réponse")) {
        return sum + ex.points;
      }
      return sum;
    }, 0);
    return { currentScore: current, totalScore: total };
  }, [filteredExercises, validatedAnswers, feedbacks]);

  // Réinitialisation lors du changement de sélection
  useEffect(() => {
    if (sessionStarted) {
      setStudentAnswers({});
      setValidatedAnswers(new Set());
      setFeedbacks({});
    }
  }, [selectedChapitre, selectedTP, sessionStarted]);

  const handleAnswerChange = (exerciseId: string, answer: string) => {
    setStudentAnswers(prev => ({
      ...prev,
      [exerciseId]: answer
    }));
  };

  const handleValidate = (exercise: Exercise) => {
    if (validatedAnswers.has(exercise.id)) return;
    const isAnswerCorrect = isCorrect(studentAnswers[exercise.id], exercise.expectedAnswers);
    setValidatedAnswers(prev => new Set([...prev, exercise.id]));
    setFeedbacks(prev => ({
      ...prev,
      [exercise.id]: isAnswerCorrect 
        ? "Bonne réponse ! ✓" 
        : `Mauvaise réponse. ${exercise.feedback}`
    }));
  };

  const handleReset = () => {
    setStudentAnswers({});
    setValidatedAnswers(new Set());
    setFeedbacks({});
    setSessionStarted(false);
  };

  const startSession = () => {
    setSessionStarted(true);
    setStudentAnswers({});
    setValidatedAnswers(new Set());
    setFeedbacks({});
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Mode Examen</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chapitre
            </label>
            <select
              value={selectedChapitre}
              onChange={(e) => setSelectedChapitre(e.target.value)}
              disabled={sessionStarted}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            >
              {chapitres.map(ch => (
                <option key={ch} value={ch}>{ch}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              TP
            </label>
            <select
              value={selectedTP}
              onChange={(e) => setSelectedTP(e.target.value)}
              disabled={sessionStarted}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            >
              {tps.map(tp => (
                <option key={tp} value={tp}>{tp}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex justify-between items-center mb-6">
          <div className="text-lg font-semibold text-gray-700">
            {filteredExercises.length} exercice{filteredExercises.length > 1 ? 's' : ''} • Score: {currentScore}/{totalScore} points
          </div>
          <div className="flex gap-2">
            {!sessionStarted ? (
              <button
                onClick={startSession}
                disabled={filteredExercises.length === 0}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Commencer
              </button>
            ) : (
              <button
                onClick={handleReset}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center gap-2"
              >
                <RotateCcw className="w-4 h-4" />
                Réinitialiser
              </button>
            )}
          </div>
        </div>
      </div>
      {!sessionStarted && filteredExercises.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-800 mb-2">Prêt à commencer ?</h3>
          <p className="text-blue-700">
            Vous avez sélectionné {filteredExercises.length} exercice{filteredExercises.length > 1 ? 's' : ''} 
            pour un total de {totalScore} points. Cliquez sur "Commencer" pour démarrer votre session d'examen.
          </p>
        </div>
      )}
      {filteredExercises.length === 0 && (
        <div className="bg-gray-100 border border-gray-300 rounded-lg p-8 text-center">
          <p className="text-gray-600 text-lg">
            Aucun exercice disponible pour cette sélection.
          </p>
          <p className="text-gray-500 mt-2">
            Essayez de sélectionner un autre chapitre ou TP.
          </p>
        </div>
      )}
      {sessionStarted && filteredExercises.length > 0 && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-600">Chargement des exercices...</p>
            </div>
          ) : (
            filteredExercises.map((exercise) => (
              <ExerciseCard
                key={exercise.id}
                exercise={exercise}
                isValidated={validatedAnswers.has(exercise.id)}
                studentAnswer={studentAnswers[exercise.id]}
                onAnswerChange={handleAnswerChange}
                onValidate={handleValidate}
                feedback={feedbacks[exercise.id]}
              />
            ))
          )}
          {validatedAnswers.size === filteredExercises.length && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
              <h3 className="text-xl font-bold text-green-800 mb-2">
                Examen terminé !
              </h3>
              <p className="text-green-700">
                Score final: {currentScore}/{totalScore} points 
                ({totalScore > 0 ? Math.round((currentScore / totalScore) * 100) : 0}%)
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ModeExam;