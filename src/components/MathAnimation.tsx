import { useState, useRef, useEffect } from 'react';
import { Button, Card, Progress } from '@/components/ui';

interface MathAnimationProps {
  animationType: string;
  parameters: Record<string, any>;
  width?: number | string;
  height?: number | string;
  onAnimationComplete?: (url: string) => void;
}

export default function MathAnimation({
  animationType,
  parameters,
  width = '100%',
  height = '500px',
  onAnimationComplete,
}: MathAnimationProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [animationUrl, setAnimationUrl] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const generateAnimation = async () => {
    setIsLoading(true);
    setError(null);
    setProgress(0);

    try {
      // Simuler une progression
      const interval = setInterval(() => {
        setProgress((prev) => {
          const newProgress = prev + Math.random() * 10;
          return newProgress > 90 ? 90 : newProgress;
        });
      }, 300);

      // Appeler l'API pour générer l'animation
      const response = await fetch('http://localhost:8000/api/animation/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          animation_type: animationType,
          parameters,
        }),
      });

      clearInterval(interval);

      if (!response.ok) {
        throw new Error('Erreur lors de la génération de l\'animation');
      }

      const data = await response.json();
      setProgress(100);
      
      // Mettre à jour l'URL de l'animation
      const fullUrl = `http://localhost:8000${data.animation_url}`;
      setAnimationUrl(fullUrl);
      
      // Appeler le callback si fourni
      if (onAnimationComplete) {
        onAnimationComplete(fullUrl);
      }
      
    } catch (err) {
      console.error('Erreur:', err);
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setIsLoading(false);
    }
  };

  // Réinitialiser l'URL de l'animation lorsque les paramètres changent
  useEffect(() => {
    setAnimationUrl(null);
  }, [animationType, parameters]);

  return (
    <Card className="p-4">
      <div className="flex flex-col items-center space-y-4">
        {animationUrl ? (
          <video
            ref={videoRef}
            src={animationUrl}
            width={width}
            height={height}
            controls
            autoPlay
            loop
            className="rounded-lg shadow-md"
          />
        ) : isLoading ? (
          <div className="w-full space-y-2">
            <div className="text-center text-sm text-gray-600 mb-2">
              Génération de l'animation en cours...
            </div>
            <Progress value={progress} className="w-full" />
            <div className="text-xs text-right text-gray-500">{Math.round(progress)}%</div>
          </div>
        ) : error ? (
          <div className="text-red-500 text-center p-4">
            <p>Erreur: {error}</p>
            <Button 
              className="mt-2" 
              variant="outline" 
              onClick={generateAnimation}
            >
              Réessayer
            </Button>
          </div>
        ) : (
          <div className="text-center p-8 border-2 border-dashed rounded-lg w-full">
            <p className="text-gray-500 mb-4">Aucune animation générée</p>
            <Button onClick={generateAnimation}>
              Générer l'animation
            </Button>
          </div>
        )}
        
        {animationUrl && (
          <div className="flex space-x-2">
            <Button 
              variant="outline" 
              onClick={generateAnimation}
              disabled={isLoading}
            >
              Régénérer
            </Button>
            <Button asChild variant="outline">
              <a 
                href={animationUrl} 
                download={`animation-${new Date().toISOString().slice(0, 10)}.mp4`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Télécharger
              </a>
            </Button>
          </div>
        )}
      </div>
    </Card>
  );
}
