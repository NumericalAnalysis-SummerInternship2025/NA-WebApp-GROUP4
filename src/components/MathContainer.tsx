
import { ReactNode } from "react";
import { Card } from "@/components/ui/card";

interface MathContainerProps {
  children: ReactNode;
  title?: ReactNode;  // Changé de string à ReactNode pour accepter du contenu riche
  className?: string;
}

export const MathContainer = ({ children, title, className = "" }: MathContainerProps) => {
  return (
    <Card className={`p-6 bg-white/90 backdrop-blur-sm ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-gray-900">{title}</h3>
      )}
      <div className="space-y-4">
        {children}
      </div>
    </Card>
  );
};
