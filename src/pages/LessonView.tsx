import React, { useState, useEffect, ReactNode, useRef, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Edit, FileText, Video, Image, File, Brain, Download, ExternalLink, Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import StudentExerciseAnswer from "./StudentExerciseAnswer";
import DesmosGraph from "@/components/DesmosGraph";
import { ContentBlock } from '../types/ContentBlock';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

interface Lesson {
  id: number;
  titre: string;
  description: string;
  duree: string;
  niveau: string;
  visibilite: string;
  prerequis: string;
  progression: boolean;
  contenu: string;
}

const LessonView = () => {
  const { lessonId, moduleId } = useParams<{ lessonId: string; moduleId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [videoProgress, setVideoProgress] = useState<number>(0);
  const [hasManimVideo, setHasManimVideo] = useState<boolean>(false);
  
  // Vérifie si le contenu de la leçon contient une vidéo Manim
  useEffect(() => {
    if (lesson?.contenu) {
      try {
        const blocks = JSON.parse(lesson.contenu);
        const hasManim = blocks.some((block: any) => block.type === 'video_manim');
        setHasManimVideo(hasManim);
      } catch (e) {
        console.error('Erreur lors de l\'analyse du contenu de la leçon:', e);
      }
    }
  }, [lesson]);

  // Video progress tracking component
  const VideoPlayer = ({ src, userId, lessonId, moduleId, onProgressUpdate }: { 
    src: string, 
    userId: string | number | undefined, 
    lessonId: string, 
    moduleId: string | undefined,
    onProgressUpdate?: (progress: number) => void 
  }) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const lastTrackedProgress = useRef<number>(0);
    const progressTimeout = useRef<NodeJS.Timeout | null>(null);
    
    // Track video progress with debounce
    const trackProgress = useCallback(async (progressPercentage: number) => {
      if (!userId || !lessonId || !moduleId) return;
      
      // Only update if progress has increased significantly (at least 1%)
      if (Math.abs(progressPercentage - lastTrackedProgress.current) < 1) {
        return;
      }
      
      // Update last tracked progress
      lastTrackedProgress.current = progressPercentage;
      
      try {
        const response = await fetch('http://localhost:8000/progress/video', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: userId,
            lesson_id: lessonId,
            progress_percentage: Math.min(100, Math.round(progressPercentage * 10) / 10) // Round to 1 decimal place
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to update video progress');
        }
        
        console.log(`Progress updated to ${progressPercentage.toFixed(1)}%`);
      
      // Mettre à jour l'état de progression localement
      if (onProgressUpdate) {
        onProgressUpdate(progressPercentage);
      }
      
      // Mettre à jour l'état global de progression
      setVideoProgress(progressPercentage);
      } catch (error) {
        console.error('Error tracking video progress:', error);
      }
    }, [userId, lessonId, moduleId]);
    
    // Handle time update to track progress with debounce
    const handleTimeUpdate = useCallback(() => {
      if (!videoRef.current || !videoRef.current.duration) return;
      
      const progress = (videoRef.current.currentTime / videoRef.current.duration) * 100;
      
      // Clear any pending updates
      if (progressTimeout.current) {
        clearTimeout(progressTimeout.current);
      }
      
      // Track immediately if at key points (every 10% or at the end)
      if (progress % 10 < 0.5 || progress >= 99) {
        trackProgress(progress);
      } else {
        // Otherwise, debounce the update to avoid too many API calls
        progressTimeout.current = setTimeout(() => {
          trackProgress(progress);
        }, 2000); // 2 second debounce
      }
    }, [trackProgress]);
    
    // Handle video end
    const handleEnded = useCallback(() => {
      console.log('Video ended, marking as 100% complete');
      trackProgress(100);
      
      // Force a refresh of the module progress
      if (moduleId && userId) {
        fetch(`http://localhost:8000/progress/module/${userId}/${moduleId}`)
          .then(res => res.json())
          .then(data => console.log('Module progress after video end:', data))
          .catch(console.error);
      }
    }, [trackProgress, moduleId, userId]);
    
    // Clean up timeout on unmount
    useEffect(() => {
      return () => {
        if (progressTimeout.current) {
          clearTimeout(progressTimeout.current);
        }
      };
    }, []);
    
    return (
      <video
        ref={videoRef}
        src={src}
        controls
        className="w-full h-full"
        onTimeUpdate={handleTimeUpdate}
        onEnded={handleEnded}
      />
    );
  };
  
  const [contentBlocks, setContentBlocks] = useState<ContentBlock[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showSolution, setShowSolution] = useState<{ [blockId: string]: boolean }>({});

  useEffect(() => {
    if (!lessonId || lessonId === 'new') {
      setError('Leçon introuvable');
      setLoading(false);
      return;
    }

    setLoading(true);
    fetch(`http://localhost:8000/lessons/${lessonId}`)
      .then(res => {
        if (!res.ok) throw new Error('Leçon introuvable');
        return res.json();
      })
      .then(data => {
        setLesson(data);
        try {
          if (data.contenu) {
            const blocks = JSON.parse(data.contenu);
            if (Array.isArray(blocks)) {
              setContentBlocks(blocks);
            }
          }
        } catch (err) {
          console.error('Erreur lors du parsing des blocs de contenu:', err);
          setContentBlocks([]);
        }
      })
      .catch(err => {
        console.error('Erreur lors du chargement de la leçon:', err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [lessonId]);

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

  // Vérifie si l'utilisateur peut accéder à la leçon suivante
  const canAccessNextLesson = useCallback(() => {
    if (user?.role === 'professeur') return true;
    if (!hasManimVideo) return true;
    return videoProgress >= 90; // Considéré comme terminé à 90% ou plus
  }, [hasManimVideo, videoProgress, user?.role]);

  // Gère la navigation vers la page suivante
  const handleNextLesson = useCallback(() => {
    if (!canAccessNextLesson()) {
      alert('Vous devez terminer de regarder la vidéo avant de pouvoir passer à la leçon suivante.');
      return;
    }
    // Logique pour passer à la leçon suivante
    // À implémenter : récupérer l'ID de la prochaine leçon
    // navigate(`/lesson/${nextLessonId}/${moduleId}`);
  }, [canAccessNextLesson]);

  const renderContentBlock = (block: ContentBlock) => {
    const content = block.content || {};

    const BlockWrapper = ({ children, icon, title }: { children: ReactNode, icon: ReactNode, title: string }) => (
      <div className="mb-12">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-gray-100 p-2 rounded-lg">{icon}</div>
          <h3 className="text-xl font-semibold text-gray-700">{title}</h3>
        </div>
        <div className="ml-12 pl-4 border-l-2 border-gray-200">{children}</div>
      </div>
    );

    switch (block.type) {
      case 'video':
      case 'video_manim':
        return (
          <div key={block.id} className="mb-16">
            <div className="aspect-video w-full bg-black rounded-xl overflow-hidden shadow-2xl mb-4">
              <VideoPlayer
                src={content.url}
                userId={user?.id}
                lessonId={lesson?.id?.toString()}
                moduleId={moduleId}
                onProgressUpdate={(progress) => setVideoProgress(progress)}
              />
            </div>
            <h2 className="text-3xl font-bold text-gray-900">{content.title || 'Vidéo'}</h2>
            {content.description && <p className="text-lg text-gray-600 mt-2 max-w-4xl">{content.description}</p>}
          </div>
        );

      case 'text':
        return (
          <div key={block.id} className="prose prose-lg max-w-none mb-12 text-gray-800 leading-relaxed">
            {renderWithLatex(content.content)}
          </div>
        );

      case 'image':
        return (
          <div key={block.id} className="mb-12 text-center">
            <img src={content.url} alt={content.alt || 'Image de la leçon'} className="max-w-full h-auto rounded-lg shadow-lg mx-auto" />
            {content.caption && <p className="text-base text-gray-500 mt-3 italic">{content.caption}</p>}
          </div>
        );

      case 'file':
        return (
          <BlockWrapper icon={<Download size={20} className="text-gray-600" />} title="Fichier à télécharger">
            <a href={content.url} download target="_blank" rel="noopener noreferrer">
              <Button>
                <Download className="mr-2" size={16} />
                {content.title || 'Télécharger'}
              </Button>
            </a>
          </BlockWrapper>
        );

      case 'quiz':
        return (
            <BlockWrapper icon={<Brain size={20} className="text-gray-600" />} title="Quiz Interactif">
                <div className="space-y-4">
                    {content.questions?.map((question: any, qIndex: number) => (
                        <div key={question.id || qIndex} className="border rounded-lg p-4">
                            <div className="font-medium mb-3">
                                Question {qIndex + 1}: {question.question}
                            </div>
                        </div>
                    ))}
                </div>
            </BlockWrapper>
        );

      case 'exercice':
        return (
          <BlockWrapper icon={<Brain size={20} className="text-gray-600" />} title="Exercice d'application">
            <StudentExerciseAnswer
              question={content.question}
              solution={user?.role === 'professeur' && showSolution[block.id] ? content.solution : undefined}
            />
            {user?.role === 'professeur' && (
              <div className="text-right mt-2">
                 <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowSolution(prev => ({ ...prev, [block.id]: !prev[block.id] }));
                    }}
                  >
                    {showSolution[block.id] ? <EyeOff size={16} /> : <Eye size={16} />}
                    <span className="ml-2">{showSolution[block.id] ? 'Cacher' : 'Voir'} la solution</span>
                  </Button>
              </div>
            )}
          </BlockWrapper>
        );

      case 'desmos':
        return (
          <BlockWrapper icon={<ExternalLink size={20} className="text-gray-600" />} title="Grapheur Desmos">
            <div className="h-[500px] border rounded-lg overflow-hidden">
              <DesmosGraph expression={content.expression} />
            </div>
          </BlockWrapper>
        );

      default:
        return (
          <div key={block.id} className="mb-6 p-4 bg-gray-50 rounded-lg">
            <div className="text-gray-500 italic">Type de bloc non reconnu: {block.type}</div>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-96"></div>
        </div>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Erreur</h1>
          <p className="text-gray-600 mb-6">{error || 'Leçon introuvable'}</p>
          <Button onClick={() => navigate(`/module/${moduleId}`)}>
            <ArrowLeft className="mr-2" size={16} />
            Retour au module
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        <div className="mb-10">
          <Button
            variant="ghost"
            onClick={() => navigate(`/module/${moduleId}`)}
            className="text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="mr-2" size={16} />
            Retour au module
          </Button>
          <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight">{lesson.titre}</h1>
          <p className="mt-4 text-xl text-gray-500">{lesson.description}</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
          {/* Bandeau d'information si la vidéo n'est pas terminée */}
          {hasManimVideo && videoProgress < 90 && user?.role !== 'professeur' && (
            <div className="mb-8 p-4 bg-yellow-50 border-l-4 border-yellow-400">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700">
                    Vous devez regarder la vidéo jusqu'à la fin pour débloquer la leçon suivante. 
                    Progression : {Math.round(videoProgress)}%
                  </p>
                </div>
              </div>
            </div>
          )}

          {contentBlocks.length === 0 ? (
            <div className="text-center py-16">
              <FileText className="w-16 h-16 mx-auto mb-6 text-gray-300" />
              <h3 className="text-2xl font-semibold text-gray-900 mb-2">Cette leçon est vide</h3>
              <p className="text-lg text-gray-600">Il n'y a pas encore de contenu à afficher.</p>
              {user?.role === 'professeur' && (
                <Button 
                  className="mt-6" 
                  size="lg"
                  onClick={() => navigate(`/lesson/${lesson.id}/${moduleId}`)}
                >
                  <Edit className="mr-2" size={18} />
                  Commencer à éditer
                </Button>
              )}
            </div>
          ) : (
            contentBlocks.map((block) => renderContentBlock(block))
          )}
        </div>

      </div>
    </div>
  );
};

export default LessonView;