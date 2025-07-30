export const quizDataByModule = {
  "Chapitre 1: Résolution numérique de systèmes d'équations linéaires": [
    {
      lesson: "Rappel sur les Normes Vectorielles et Matricielles",
      questions: [
        {
          type: "mcq",
          question: "Quelles sont les propriétés essentielles d'une norme vectorielle ?",
          options: [
            "Continuité, dérivabilité, symétrie",
            "Linéarité, orthogonalité, commutativité",
            "Positivité définie, homogénéité, inégalité triangulaire",
            "Additivité, inversibilité, associativité",
          ],
          correct: 2,
        },
        {
          type: "mcq",
          question: "Quelle est la formule correcte de la norme vectorielle 1 (‖X‖₁) ?",
          options: [
            "√(x₁² + x₂² + ... + xₙ²)",
            "max(|x₁|, |x₂|, ..., |xₙ|)",
            "|x₁ + x₂ + ... + xₙ|",
            "|x₁| + |x₂| + ... + |xₙ|",
          ],
          correct: 3,
        },
        {
          type: "bool",
          question: "Toute norme vectorielle définit une norme matricielle subordonnée.",
          correct: true,
        },
        {
          type: "bool",
          question: "La norme matricielle ‖AB‖ est toujours égale à ‖A‖ × ‖B‖.",
          correct: false,
        },
        {
          type: "text",
          question: "Soit X = (3, -4). Calculez la norme euclidienne ‖X‖₂.",
          correct: "5",
        },
        {
          type: "mcq",
          question: "Quelle norme est aussi appelée norme infinie (‖X‖∞) ?",
          options: [
            "La somme des valeurs absolues",
            "La racine carrée de la somme des carrés",
            "Le maximum des valeurs absolues des composantes",
            "Aucune de ces réponses",
          ],
          correct: 2,
        },
        {
          type: "bool",
          question: "Toutes les normes vectorielles sont équivalentes dans ℝⁿ.",
          correct: true,
        },
      ],
      remedialQuestions: [
        {
          type: "text",
          question: "Un algorithme qui converge lentement est-il toujours inutile ? (oui/non)",
          correct: "non",
        },
        {
          type: "mcq",
          question: "Quelle est la principale cause d'erreur dans les calculs numériques ?",
          options: ["Erreurs de modèle", "Erreurs d'arrondi", "Erreurs de troncature", "Toutes les réponses"],
          correct: 3,
        },
      ],
    },
    {
      lesson: "Résolution par Pivot de Gauss  Résolution  Décomposition LU",
      questions: [
        {
          type: "bool",
          question: "La méthode du pivot de Gauss permet de transformer un système linéaire en un système triangulaire supérieur.",
          correct: true,
        },
        {
          type: "mcq",
          question: "Quel est le principal objectif du pivot partiel dans l’algorithme de Gauss ?",
          options: [
            "Minimiser les erreurs de troncature",
            "Réduire le temps de calcul",
            "Éviter la division par zéro ou les petits pivots",
            "Améliorer la symétrie du système",
          ],
          correct: 2,
        },
        {
          type: "text",
          question: "Quelle est la forme générale d'une matrice triangulaire supérieure 3x3 ?",
          correct: "a11 a12 a13 / 0 a22 a23 / 0 0 a33",
        },
        {
          type: "bool",
          question: "La décomposition LU d'une matrice A existe toujours, quelle que soit A.",
          correct: false,
        },
      ],
    },
    {
      lesson: "Méthodes de Jacobi  / Gauss-Seidel",
      questions: [
        {
          type: "bool",
          question: "La méthode de Jacobi utilise toujours les valeurs de l’itération précédente pour calculer la nouvelle solution.",
          correct: true,
        },
        {
          type: "mcq",
          question: "Quelle est la condition de convergence pour la méthode de Jacobi ?",
          options: [
            "A est symétrique",
            "A est inversible",
            "La matrice A est à diagonale strictement dominante",
            "A a un déterminant positif",
          ],
          correct: 2,
        },
        {
          type: "mcq",
          question: "Quelle différence distingue Gauss-Seidel de Jacobi ?",
          options: [
            "Gauss-Seidel est plus lent",
            "Jacobi utilise des valeurs mises à jour immédiatement",
            "Gauss-Seidel utilise les nouvelles valeurs dès qu'elles sont disponibles",
            "Aucune différence significative",
          ],
          correct: 2,
        },
        {
          type: "text",
          question: "Donnez une situation réelle où l’on préfère une méthode itérative à une méthode directe.",
          correct: "grande matrice creuse / faible mémoire / résolution approximative",
        },
      ],
    },
  ],
  "Chapitre 2: Un Autre Chapitre": [
    {
      lesson: "Quiz pour le chapitre 2",
      questions: [
        {
          type: "text",
          question: "Ceci est une question pour le chapitre 2.",
          correct: "réponse"
        }
      ]
    }
  ]
};
