import React from "react";
import { Info } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "./tooltip";

interface GuideTooltipProps {
  title: string;
  content: React.ReactNode;
  side?: "top" | "right" | "bottom" | "left";
  className?: string;
}

export function GuideTooltip({ 
  title, 
  content, 
  side = "right",
  className = ""
}: GuideTooltipProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button 
          className={`inline-flex items-center justify-center p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-300 ${className}`}
          aria-label="Guide d'aide"
          type="button"
        >
          <Info className="h-4 w-4 text-blue-500" />
        </button>
      </TooltipTrigger>
      <TooltipContent 
        side={side} 
        sideOffset={8}
        className="max-w-md p-4 bg-white border border-gray-200 shadow-lg rounded-lg"
      >
        <h4 className="font-semibold text-blue-600 mb-2 text-base">{title}</h4>
        <div className="text-sm text-gray-700">
          {content}
        </div>
      </TooltipContent>
    </Tooltip>
  );
}
