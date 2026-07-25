import * as React from "react";
import { cn } from "./card";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variantStyles = {
    default: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-slate-800 text-slate-200 hover:bg-slate-700",
    destructive: "bg-red-600 text-white hover:bg-red-700",
    outline: "border border-slate-700 text-slate-300",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border border-transparent px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2",
        variantStyles[variant],
        className
      )}
      {...props}
    />
  );
}
