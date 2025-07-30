import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import DesmosGraph from '@/components/DesmosGraph';
import MathAnimation from '@/components/MathAnimation';
export default function MathVisualization() {
  const [functionInput, setFunctionInput] = useState('x^2');
  const [activeTab, setActiveTab] = useState('graph');
  const [animationParams, setAnimationParams] = useState({
    function: 'x**2',
    show_derivative: true,
    x_range: [-5, 5, 1],
    y_range: [0, 10, 1],
  });

  const handleFunctionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFunctionInput(e.target.value);
  };

  const handlePlotFunction = () => {
    // Cette fonction est gérée par le composant DesmosGraph
    console.log('Tracer la fonction:', functionInput);
  };

  const handleAnimationComplete = (url: string) => {
    console.log('Animation générée:', url);
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Visualisation Mathématique</h1>
      
      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-2 mb-6">
          <TabsTrigger value="graph">Graphique</TabsTrigger>
          <TabsTrigger value="animation">Animation</TabsTrigger>
        </TabsList>
        
        <TabsContent value="graph">
          <Card>
            <CardHeader>
              <CardTitle>Graphique de fonction</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <div className="flex space-x-2">
                  <Input 
                    type="text" 
                    value={functionInput}
                    onChange={handleFunctionChange}
                    placeholder="Entrez une fonction (ex: x^2, sin(x), etc.)"
                    className="flex-1"
                  />
                  <Button onClick={handlePlotFunction}>
                    Tracer
                  </Button>
                </div>
              </div>
              <div className="border rounded-lg overflow-hidden">
                <DesmosGraph 
                  expression={functionInput}
                  xRange={[-10, 10]}
                  yRange={[-10, 10]}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="animation">
          <Card>
            <CardHeader>
              <CardTitle>Animation Mathématique</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Fonction (en Python)
                    </label>
                    <Input 
                      value={animationParams.function}
                      onChange={(e) => setAnimationParams({
                        ...animationParams,
                        function: e.target.value
                      })}
                      placeholder="x**2"
                    />
                  </div>
                  <div className="flex items-end space-x-2">
                    <div className="flex-1">
                      <label className="block text-sm font-medium mb-1">
                        Plage X
                      </label>
                      <div className="flex space-x-2">
                        <Input 
                          type="number" 
                          value={animationParams.x_range[0]}
                          onChange={(e) => setAnimationParams({
                            ...animationParams,
                            x_range: [
                              parseFloat(e.target.value) || 0,
                              animationParams.x_range[1],
                              animationParams.x_range[2]
                            ]
                          })}
                          className="w-20"
                        />
                        <span className="flex items-center">à</span>
                        <Input 
                          type="number" 
                          value={animationParams.x_range[1]}
                          onChange={(e) => setAnimationParams({
                            ...animationParams,
                            x_range: [
                              animationParams.x_range[0],
                              parseFloat(e.target.value) || 0,
                              animationParams.x_range[2]
                            ]
                          })}
                          className="w-20"
                        />
                      </div>
                    </div>
                    <div className="flex-1">
                      <label className="block text-sm font-medium mb-1">
                        Plage Y
                      </label>
                      <div className="flex space-x-2">
                        <Input 
                          type="number" 
                          value={animationParams.y_range[0]}
                          onChange={(e) => setAnimationParams({
                            ...animationParams,
                            y_range: [
                              parseFloat(e.target.value) || 0,
                              animationParams.y_range[1],
                              animationParams.y_range[2]
                            ]
                          })}
                          className="w-20"
                        />
                        <span className="flex items-center">à</span>
                        <Input 
                          type="number" 
                          value={animationParams.y_range[1]}
                          onChange={(e) => setAnimationParams({
                            ...animationParams,
                            y_range: [
                              animationParams.y_range[0],
                              parseFloat(e.target.value) || 0,
                              animationParams.y_range[2]
                            ]
                          })}
                          className="w-20"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="showDerivative"
                    checked={animationParams.show_derivative}
                    onChange={(e) => setAnimationParams({
                      ...animationParams,
                      show_derivative: e.target.checked
                    })}
                    className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <label htmlFor="showDerivative" className="text-sm text-gray-700">
                    Afficher la dérivée
                  </label>
                </div>
                
                <MathAnimation 
                  animationType="function_plot"
                  parameters={animationParams}
                  onAnimationComplete={handleAnimationComplete}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
