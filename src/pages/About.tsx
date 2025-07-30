
import { Users, Target, BookOpen, Lightbulb } from "lucide-react"; /*react libararyyy*/
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const About = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            À propos de Num
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Une plateforme dédiée à l'apprentissage interactif de l'analyse numérique
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <Card className="bg-white border border-gray-200">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Target className="h-8 w-8 text-blue-600" />
                <CardTitle className="text-xl">Notre Mission</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Rendre l'analyse numérique accessible et compréhensible grâce à des 
                visualisations interactives et des explications claires. Nous croyons 
                que les mathématiques deviennent plus faciles à comprendre quand on 
                peut les voir en action.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Lightbulb className="h-8 w-8 text-yellow-600" />
                <CardTitle className="text-xl">Notre Vision</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Créer un environnement d'apprentissage où les étudiants peuvent 
                expérimenter, visualiser et maîtriser les concepts fondamentaux 
                de l'analyse numérique à leur propre rythme.
              </p>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 mb-12">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <Users className="h-8 w-8 text-blue-600" />
              <CardTitle className="text-2xl">L'Équipe</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Équipe de Développement Num
                </h3>
                <p className="text-gray-600 mb-4">
                  Passionnés par l'éducation mathématique et les technologies web
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <BookOpen className="h-8 w-8 text-blue-600" />
                  </div>
                  <h4 className="font-medium text-gray-900">Expertise Pédagogique</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Conception de modules d'apprentissage adaptés
                  </p>
                </div>
                
                <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Target className="h-8 w-8 text-green-600" />
                  </div>
                  <h4 className="font-medium text-gray-900">Développement Web</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Interfaces interactives et visualisations
                  </p>
                </div>
                
                <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Lightbulb className="h-8 w-8 text-purple-600" />
                  </div>
                  <h4 className="font-medium text-gray-900">Innovation</h4>
                  <p className="text-sm text-gray-600 mt-1">
                    Nouvelles approches d'apprentissage
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white border border-gray-200">
          <CardHeader>
            <CardTitle className="text-2xl text-center">Pourquoi NumiViz ?</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  🎯 Apprentissage Visuel
                </h3>
                <p className="text-gray-600">
                  Les concepts abstraits deviennent concrets grâce à nos visualisations 
                  interactives qui permettent de voir les algorithmes en action.
                </p>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  🔬 Expérimentation
                </h3>
                <p className="text-gray-600">
                  Modifiez les paramètres, testez différentes valeurs et observez 
                  immédiatement l'impact sur les résultats.
                </p>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  📚 Progression Structurée
                </h3>
                <p className="text-gray-600">
                  Modules organisés du plus simple au plus complexe, avec des 
                  explications étape par étape.
                </p>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  🌐 Accessible Partout
                </h3>
                <p className="text-gray-600">
                  Plateforme web accessible depuis n'importe quel appareil, 
                  sans installation requise.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default About;
