import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Loader2, Brain, BarChart, FileText } from "lucide-react";

interface ProcessingIndicatorProps {
  isVisible: boolean;
  currentStep?: string;
  progress?: number;
}

const ProcessingIndicator: React.FC<ProcessingIndicatorProps> = ({ 
  isVisible, 
  currentStep = "Initializing analysis...",
  progress = 0
}) => {
  if (!isVisible) return null;

  const steps = [
    { icon: Brain, label: "AI agents analyzing data structure", duration: "~30s" },
    { icon: BarChart, label: "Generating statistical insights", duration: "~45s" },
    { icon: FileText, label: "Creating visualizations and narrative", duration: "~60s" }
  ];

  return (
    <Card className="w-full max-w-2xl mx-auto border-0 bg-gradient-card shadow-card">
      <CardContent className="p-8 text-center space-y-6">
        {/* Main Spinner */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <Loader2 className="h-12 w-12 animate-spin text-primary" />
            <div className="absolute inset-0 h-12 w-12 animate-pulse-slow">
              <div className="h-full w-full rounded-full border-2 border-primary/20" />
            </div>
          </div>
        </div>
        
        {/* Status Text */}
        <div className="space-y-2">
          <h3 className="text-xl font-semibold">Analyzing Your Data</h3>
          <p className="text-muted-foreground">
            Our AI team is working on your data. This may take a few minutes.
          </p>
        </div>
        
        {/* Progress Bar */}
        <div className="space-y-2">
          <Progress value={progress} className="w-full" />
          <p className="text-sm text-muted-foreground">{Math.round(progress)}% complete</p>
        </div>
        
        {/* Current Step */}
        <div className="p-4 bg-muted/50 rounded-lg">
          <p className="text-sm font-medium text-primary">{currentStep}</p>
        </div>
        
        {/* Processing Steps */}
        <div className="space-y-3 text-left">
          <h4 className="text-sm font-medium text-center mb-4">Analysis Pipeline</h4>
          {steps.map((step, index) => (
            <div key={index} className="flex items-center gap-3 p-3 bg-muted/30 rounded-lg">
              <step.icon className="h-5 w-5 text-primary flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-medium">{step.label}</p>
              </div>
              <span className="text-xs text-muted-foreground">{step.duration}</span>
            </div>
          ))}
        </div>
        
        <p className="text-xs text-muted-foreground">
          Please don't close this window while analysis is in progress
        </p>
      </CardContent>
    </Card>
  );
};

export default ProcessingIndicator;