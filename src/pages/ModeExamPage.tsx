import ModeExam from "./ModeExam";

export default function ModeExamPage() {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen py-8 px-4 flex flex-col items-center">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">Mode Examen</h1>
        <p className="text-gray-600 mb-6 text-center">
          Entraînez-vous sur des exercices interactifs par chapitre, avec feedback immédiat et suivi de vos progrès.
        </p>
        <ModeExam />
      </div>
    </div>
  );
}
