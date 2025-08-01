export interface ContentBlock {
  id: string;
  type: 'video' | 'text' | 'image' | 'file' | 'quiz' | 'exercice' | 'video_manim' | 'desmos';
  content: any;
  order: number;
}