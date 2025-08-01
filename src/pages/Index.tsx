import { Calculator, BarChart3, BookOpen, Zap, Play, Info, LogIn } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useAuth } from '@/contexts/AuthContext';

const Index = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  const features = [
    {
      icon: Calculator,
      title: "Méthodes Numériques",
      description: "Implémentations interactives de résolution de racines, d'intégration et d'équations différentielles"
    },
    {
      icon: BarChart3,
      title: "Visualisation de Données",
      description: "Tracé en temps réel et graphiques de fonctions mathématiques et de résultats numériques"
    },
    {
      icon: BookOpen,
      title: "Modules Éducatifs",
      description: "Tutoriels étape par étape couvrant l'algèbre linéaire, le calcul et les statistiques"
    },
    {
      icon: Zap,
      title: "Apprentissage Interactif",
      description: "Exploration pratique des concepts mathématiques avec un retour visuel immédiat"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Auth Button Top Right */}
      <div className="fixed top-6 right-8 z-50">
        {isAuthenticated ? (
          <Button
            variant="outline"
            className="flex items-center gap-2 border-blue-600 text-blue-700 hover:bg-blue-600 hover:text-white shadow"
            onClick={logout}
          >
            Déconnexion
          </Button>
        ) : (
          <Button
            variant="outline"
            className="flex items-center gap-2 border-blue-600 text-blue-700 hover:bg-blue-600 hover:text-white shadow"
            onClick={() => navigate('/auth')}
          >
            <LogIn className="w-4 h-4" />
            Connexion / Inscription
          </Button>
        )}
      </div>
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Analyse Numérique Interactive
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Explorez les concepts clés de l'analyse numérique à travers des animations et des outils interactifs. 
            Parfait pour les étudiants et enseignants en sciences.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-blue-600 hover:bg-blue-700 flex items-center gap-2"
              onClick={() => navigate('/modules')}
            >
              <Play size={20} />
              Commencer l'exploration
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="flex items-center gap-2"
              onClick={() => navigate('/tools')}
            >
              <Calculator size={20} />
              Outils Interactifs
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="flex items-center gap-2"
              onClick={() => navigate('/about')}
            >
              <Info size={20} />
              À propos
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Fonctionnalités Principales
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Découvrez une approche moderne et interactive pour apprendre l'analyse numérique
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="bg-white/70 backdrop-blur-sm hover:bg-white/90 transition-all duration-300">
              <CardHeader className="text-center">
                <feature.icon className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Modules Preview */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">
            Modules Disponibles
          </h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Explorez nos modules interactifs pour maîtriser les concepts d'analyse numérique
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div>
              <h4 className="text-xl font-semibold mb-4">Apprentissage Visuel</h4>
              <p className="text-gray-600 mb-4">
                Visualisations interactives des méthodes numériques avec ajustement des paramètres en temps réel.
              </p>
              <Button 
                className="bg-blue-600 hover:bg-blue-700"
                onClick={() => navigate('/modules')}
              >
                <BookOpen className="mr-2" size={16} />
                Voir tous les modules
              </Button>
            </div>
            <div className="bg-gray-50 rounded-lg p-6 min-h-[200px] flex items-center justify-center">
              <div className="text-center text-gray-500">
                <BarChart3 className="h-16 w-16 mx-auto mb-2" />
                <p>Zone Interactive</p>
                <p className="text-sm">Cliquez sur "Voir tous les modules" pour explorer</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Calculator className="h-6 w-6" />
                <span className="text-lg font-semibold">NumiViz</span>
              </div>
              <p className="text-gray-400">
                Plateforme interactive pour l'éducation et la visualisation de l'analyse numérique.
              </p>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Modules</h5>
              <ul className="space-y-2 text-gray-400">
                <li>Méthodes de résolution</li>
                <li>Intégration numérique</li>
                <li>Outils d'algèbre linéaire</li>
                <li>Analyse statistique</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Ressources</h5>
              <ul className="space-y-2 text-gray-400">
                <li>Documentation</li>
                <li>Tutoriels</li>
                <li>Exemples</li>
                <li>Référence API</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Plateforme NumiViz. Conçue pour l'excellence éducative.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
