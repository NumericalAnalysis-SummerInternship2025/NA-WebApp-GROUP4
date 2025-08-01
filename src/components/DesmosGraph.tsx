import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    Desmos: any;
  }
}

interface DesmosGraphProps {
  expression?: string;
  expressions?: string[];
  xRange?: [number, number];
  yRange?: [number, number];
  onReady?: (calculator: any) => void;
}

export default function DesmosGraph({
  expression,
  expressions,
  xRange = [-10, 10],
  yRange = [-10, 10],
  onReady
}: DesmosGraphProps) {
  const calculatorRef = useRef<HTMLDivElement>(null);
  const calculatorInstance = useRef<any>(null);

  const initializeCalculator = () => {
    if (!calculatorRef.current || !window.Desmos) return;
    
    // Options de base pour la calculatrice
    calculatorInstance.current = window.Desmos.GraphingCalculator(calculatorRef.current, {
      keypad: true,
      expressions: true,
      settingsMenu: true,
      xAxisStep: 1,
      yAxisStep: 1,
      xAxisLabel: 'x',
      yAxisLabel: 'y',
      xAxisMinorSubdivisions: 1,
      yAxisMinorSubdivisions: 1,
      xAxisArrowMode: 'NONE',
      yAxisArrowMode: 'NONE',
      implicitFunctionMaxDepth: 3,
      pointsOfInterest: true,
      trace: false,
      border: true,
      expressionsCollapsed: false,
      expressionsTopbar: true,
      autosize: true,
      showGrid: true,
      showXAxis: true,
      showYAxis: true,
      xAxisNumbers: true,
      yAxisNumbers: true,
      polarMode: false,
      lockViewport: false,
      images: {},
      sliders: {}
    });
    
    // Définir la vue
    calculatorInstance.current.setMathBounds({
      left: xRange[0],
      right: xRange[1],
      bottom: yRange[0],
      top: yRange[1],
    });

    // Nouvelle logique : plusieurs courbes
    if (expressions && expressions.length > 0) {
      expressions.forEach((exp, i) => {
        calculatorInstance.current.setExpression({
          id: `graph${i+1}`,
          latex: exp,
          color: window.Desmos.Colors[i % window.Desmos.Colors.length] || window.Desmos.Colors.BLUE,
        });
      });
    } else if (expression) {
      calculatorInstance.current.setExpression({
        id: 'graph1',
        latex: expression,
        color: window.Desmos.Colors.BLUE,
      });
    }

    // Appeler le callback onReady si fourni
    if (onReady) {
      onReady(calculatorInstance.current);
    }
  };

  useEffect(() => {
    if (!calculatorRef.current) return;

    // Vérifier si le script est déjà chargé
    if (window.Desmos) {
      initializeCalculator();
      return;
    }

    // Charger le script Desmos
    const script = document.createElement('script');
    script.src = 'https://www.desmos.com/api/v1.7/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6';
    script.async = true;
    
    script.onload = () => {
      if (window.Desmos) {
        initializeCalculator();
      }
    };

    document.body.appendChild(script);

    // Nettoyer
    return () => {
      if (calculatorInstance.current) {
        calculatorInstance.current.destroy();
        calculatorInstance.current = null;
      }
    };
  }, [expression, expressions, xRange, yRange, onReady]);

  return (
    <div 
      ref={calculatorRef} 
      style={{ 
        width: '100%', 
        height: '500px',
        borderRadius: '8px',
        overflow: 'hidden',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }} 
    />
  );
}
