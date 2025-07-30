import { useState } from "react";
import { useLocation } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { MathContainer } from "@/components/MathContainer";
import DesmosGraph from "@/components/DesmosGraph";
import { Button } from "@/components/ui/button";
import { Code, BarChart3, LayoutGrid, Info } from "lucide-react";
import { useSidebar } from "@/components/ui/sidebar";
import MatrixLabPage from "./MatrixLabPage";
import SystemesLineairesInteractiveGraph from "../components/SystemesLineairesInteractiveGraph";
import EquationsNonLineairesInteractiveGraph from "../components/EquationsNonLineairesInteractiveGraph";
import LinearSystemSolver from "@/pages/modules/LinearSystemSolver";
import { GuideTooltip } from "@/components/ui/GuideTooltip";

const MathTools = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialTab = params.get("tab") || "python";
  const [activeTab, setActiveTab] = useState(initialTab);
  const { open } = useSidebar();

  const tabs = [
    { id: "linearsystems", label: "Systèmes Linéaires 2x2", icon: LayoutGrid },
    { id: "desmos", label: "Desmos", icon: BarChart3 },
    { id: "systemes", label: "Systèmes Linéaires", icon: BarChart3 },
    { id: "equations", label: "Équations Non-linéaires", icon: BarChart3 },
    { id: "matrixlab", label: "Laboratoire de Matrices", icon: Code },
  ];

  return (
    <Layout className="bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className={`${open ? 'px-4' : 'px-12'} py-8 w-full`}>
        <div className="mb-8">
          <div className="flex items-center gap-2">
            <h1 className="text-3xl font-bold text-gray-900">
              Interactive Mathematical Tools
            </h1>
            <GuideTooltip 
              title="Guide des Outils Mathématiques"
              content={
                <>
                  <p className="mb-2">Cette page regroupe différents outils interactifs pour explorer les concepts mathématiques :</p>
                  <ul className="list-disc pl-5 space-y-1">
                    <li><strong>Systèmes Linéaires 2x2</strong> : Résolution graphique et numérique</li>
                    <li><strong>Desmos</strong> : Calculatrice graphique avancée</li>
                    <li><strong>Laboratoire de Matrices</strong> : Visualisation et manipulation de matrices</li>
                  </ul>
                  <p className="mt-2 text-sm text-gray-600">Passez la souris sur les icônes <Info className="inline h-3 w-3" /> pour plus d'informations sur chaque outil.</p>
                </>
              }
            />
          </div>
          <p className="text-gray-600 mt-2">
            Explorez les concepts mathématiques de manière interactive avec nos outils de visualisation
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 mb-8">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              variant={activeTab === tab.id ? "default" : "outline"}
              className="flex items-center gap-2"
            >
              <tab.icon size={16} />
              {tab.label}
            </Button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="grid gap-6">
          {activeTab === "linearsystems" && (
            <MathContainer 
              title={
                <div className="flex items-center gap-2">
                  <span>Résolution de systèmes d'équations linéaires 2x2</span>
                  <GuideTooltip 
                    title="Guide : Systèmes Linéaires 2x2"
                    content={
                      <>
                        <p className="mb-2">Cet outil vous permet de résoudre des systèmes de 2 équations à 2 inconnues :</p>
                        <p className="font-mono bg-gray-100 p-2 rounded mb-2">
                          a₁x + b₁y = c₁<br />
                          a₂x + b₂y = c₂
                        </p>
                        <ul className="list-disc pl-5 space-y-1">
                          <li>Entrez les coefficients dans les champs correspondants</li>
                          <li>Visualisez la solution graphiquement</li>
                          <li>Obtenez la solution exacte</li>
                        </ul>
                      </>
                    }
                  />
                </div>
              }
            >
              <LinearSystemSolver />
            </MathContainer>
          )}
          {activeTab === "desmos" && (
            <MathContainer 
              title={
                <div className="flex items-center gap-2">
                  <span>Calculatrice Graphique Desmos</span>
                  <GuideTooltip 
                    title="Guide : Calculatrice Desmos"
                    content={
                      <>
                        <p className="mb-2">Cette calculatrice graphique avancée vous permet de :</p>
                        <ul className="list-disc pl-5 space-y-1">
                          <li>Tracer des fonctions mathématiques</li>
                          <li>Créer des tables de valeurs</li>
                          <li>Visualiser des équations algébriques</li>
                          <li>Ajouter des curseurs pour des paramètres variables</li>
                          <li>Explorer les transformations de fonctions</li>
                        </ul>
                        <p className="mt-2 text-sm text-gray-600">Essayez d'entrer des équations comme y=sin(x) ou x² + y² = 1</p>
                      </>
                    }
                  />
                </div>
              }
            >
              <DesmosGraph expression={"y=x^2"} />
            </MathContainer>
          )}

          {activeTab === "systemes" && (
            <MathContainer 
              title={
                <div className="flex items-center gap-2">
                  <span>Systèmes Linéaires : Convergence Jacobi vs Gauss-Seidel</span>
                  <GuideTooltip 
                    title="Guide : Méthodes Itératives"
                    content={
                      <>
                        <p className="mb-2">Comparez la convergence des méthodes itératives pour résoudre des systèmes linéaires :</p>
                        <ul className="list-disc pl-5 space-y-1">
                          <li><span className="text-red-600 font-medium">Méthode de Jacobi</span> : Met à jour toutes les composantes de la solution en parallèle</li>
                          <li><span className="text-blue-700 font-medium">Méthode de Gauss-Seidel</span> : Utilise immédiatement les nouvelles valeurs dans le calcul</li>
                        </ul>
                        <p className="mt-2">Entrez votre système linéaire et observez quelle méthode converge le plus rapidement !</p>
                      </>
                    }
                  />
                </div>
              }
            >
              <SystemesLineairesInteractiveGraph />
              <div className="mt-4 text-sm text-gray-600">
                <b>Exemple :</b> Système 4x₁ + x₂ = 1, x₁ + 3x₂ = 2 <br/>
                <span className="text-red-600">Jacobi</span> converge en 10 itérations, <span className="text-blue-700">Gauss-Seidel</span> en 7.
              </div>
            </MathContainer>
          )}

          {activeTab === "equations" && (
            <MathContainer 
              title={
                <div className="flex items-center gap-2">
                  <span>Équations Non-linéaires : Convergence des méthodes</span>
                  <GuideTooltip 
                    title="Guide : Résolution d'Équations Non-linéaires"
                    content={
                      <>
                        <p className="mb-2">Comparez différentes méthodes numériques pour résoudre f(x) = 0 :</p>
                        <ul className="list-disc pl-5 space-y-1">
                          <li><span className="text-green-700 font-medium">Dichotomie</span> : Méthode de bissection qui divise l'intervalle</li>
                          <li><span className="text-orange-700 font-medium">Newton-Raphson</span> : Utilise la dérivée pour une convergence quadratique</li>
                          <li><span className="text-purple-700 font-medium">Point Fixe</span> : Résout g(x) = x</li>
                        </ul>
                        <p className="mt-2">Visualisez comment chaque méthode converge vers la solution !</p>
                      </>
                    }
                  />
                </div>
              }
            >
              <EquationsNonLineairesInteractiveGraph />
              <div className="mt-4 text-sm text-gray-600">
                <b>Exemple :</b> f(x) = x² - 2, point initial x₀=1<br/>
                <span className="text-green-700">Dichotomie</span> : largeur de l'intervalle<br/>
                <span className="text-orange-700">Newton</span> : erreur |xₖ₊₁ - xₖ|<br/>
                <span className="text-purple-700">Point Fixe</span> : distance à la solution
              </div>
            </MathContainer>
          )}

        

          {activeTab === "matrixlab" && (
            <MathContainer 
              title={
                <div className="flex items-center gap-2">
                  <span>Laboratoire de Matrices</span>
                  <GuideTooltip 
                    title="Guide : Laboratoire de Matrices"
                    content={
                      <>
                        <p className="mb-2">Explorez les opérations matricielles de manière interactive :</p>
                        <ul className="list-disc pl-5 space-y-1">
                          <li>Créez et modifiez des matrices</li>
                          <li>Effectuez des opérations de base (addition, multiplication, transposée)</li>
                          <li>Calculez le déterminant et l'inverse</li>
                          <li>Visualisez les transformations géométriques</li>
                        </ul>
                        <p className="mt-2">Idéal pour comprendre l'algèbre linéaire de manière visuelle !</p>
                      </>
                    }
                  />
                </div>
              }
            >
              {/* @ts-ignore */}
              <MatrixLabPage />
            </MathContainer>
          )}


        </div>
      </div>
    </Layout>
  );
};

export default MathTools;
