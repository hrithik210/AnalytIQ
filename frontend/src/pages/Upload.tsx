import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Upload as UploadIcon } from "lucide-react";
import FileUploader from "@/components/upload/FileUploader";
import ProcessingIndicator from "@/components/upload/ProcessingIndicator";
import { useToast } from "@/hooks/use-toast";
import { apiService, type UploadResponse } from "@/services/api";
import { supabase } from "@/services/supabase";

const Upload = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState("");
  const [progress, setProgress] = useState(0);

  const handleFileSelect = (file: File | null) => {
    setSelectedFile(file);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      toast({
        title: "No file selected",
        description: "Please select a CSV file to analyze.",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setCurrentStep("Uploading file and initializing AI agents...");
    setProgress(10);
    
    try {
      // Upload to Supabase Storage first to reduce backend I/O
      setCurrentStep("Uploading file to storage...");
      const bucket = import.meta.env.VITE_SUPABASE_BUCKET as string;
      const ext = selectedFile.name.split('.').pop()?.toLowerCase();
      if (ext !== 'csv') {
        throw new Error('Only CSV files are allowed.');
      }
      const uniquePath = `${Date.now()}_${selectedFile.name}`;
      const { error: uploadError } = await supabase.storage.from(bucket).upload(uniquePath, selectedFile, {
        contentType: 'text/csv',
        upsert: false,
      });
      if (uploadError) {
        throw new Error(`Upload to storage failed: ${uploadError.message}`);
      }

      // Start the actual API call pointing to Supabase path
      const analysisPromise = apiService.analyzeSupabaseCSV(bucket, uniquePath);
      
      // Simulate progress updates while analysis is running
      const progressSteps = [
        { message: "Schema Expert analyzing data structure...", progress: 25 },
        { message: "Data Cleaner processing quality issues...", progress: 45 },
        { message: "Stats Guru generating insights...", progress: 65 },
        { message: "Chart Wizard creating visualizations...", progress: 80 },
        { message: "Storyteller crafting narrative...", progress: 95 }
      ];

      // Update progress every 3 seconds
      const progressInterval = setInterval(() => {
        const currentIndex = Math.floor((progress - 10) / 20);
        if (currentIndex < progressSteps.length) {
          const step = progressSteps[currentIndex];
          setCurrentStep(step.message);
          setProgress(step.progress);
        }
      }, 3000);

      // Wait for the actual analysis to complete
      const result: UploadResponse = await analysisPromise;
      
      // Clear progress interval
      clearInterval(progressInterval);
      
      // Final progress update
      setCurrentStep("Analysis complete!");
      setProgress(100);

      // Show success toast
      toast({
        title: "Analysis Complete!",
        description: "Your data has been successfully analyzed.",
      });
      
      // Navigate to report page with actual data
      navigate("/report", { 
        state: { 
          reportData: result
        }
      });
      
    } catch (error) {
      console.error('Analysis failed:', error);
      setIsProcessing(false);
      setProgress(0);
      setCurrentStep("");
      
      toast({
        title: "Analysis Failed",
        description: error instanceof Error ? error.message : "An unexpected error occurred during analysis.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-xl">
        <div className="container flex h-20 items-center justify-between px-4 md:px-6">
          <Button 
            variant="ghost" 
            onClick={() => navigate("/")}
            className="gap-2 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Button>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-primary text-sm font-semibold text-primary-foreground shadow-glow">
              A
            </div>
            <div className="hidden text-left sm:block">
              <p className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">Mission Console</p>
              <p className="text-lg font-semibold tracking-tight">AnalytIQ</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container px-4 py-12 md:px-6 md:py-14">
        <div className="max-w-4xl mx-auto">
          {!isProcessing ? (
            <div className="text-center space-y-8">
              {/* Title */}
              <div className="space-y-4">
                <h1 className="text-balance text-4xl font-semibold tracking-tight md:text-6xl">
                  Launch Your{" "}
                  <span className="bg-gradient-primary bg-clip-text text-transparent">
                    Analysis Run
                  </span>
                </h1>
                <p className="mx-auto max-w-2xl text-lg text-muted-foreground md:text-xl">
                  Upload one CSV and dispatch the full agent fleet for structured analysis, visual output, and
                  narrative synthesis.
                </p>
              </div>

              {/* Instructions */}
              <Card className="panel-soft mx-auto max-w-2xl border-border/70">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-center justify-center">
                    <UploadIcon className="h-5 w-5" />
                    Getting Started
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 text-left">
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold mt-0.5">
                        1
                      </div>
                      <p className="text-sm">Select your CSV file using the uploader below</p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold mt-0.5">
                        2
                      </div>
                      <p className="text-sm">Click "Start Analysis" to begin the automated process</p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold mt-0.5">
                        3
                      </div>
                      <p className="text-sm">Wait for our AI agents to analyze and visualize your data</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* File Uploader */}
              <FileUploader
                onFileSelect={handleFileSelect}
                selectedFile={selectedFile}
                disabled={isProcessing}
              />

              {/* Submit Button */}
              <Button
                size="lg"
                onClick={handleSubmit}
                disabled={!selectedFile || isProcessing}
                className="h-12 bg-gradient-primary px-8 text-base font-semibold text-primary-foreground shadow-glow transition-transform duration-300 hover:scale-[1.02]"
              >
                Start Analysis
              </Button>
            </div>
          ) : (
            <div className="space-y-8">
              <div className="text-center">
                <h1 className="mb-4 text-4xl font-semibold tracking-tight md:text-6xl">
                  Analyzing Your{" "}
                  <span className="bg-gradient-primary bg-clip-text text-transparent">
                    Data
                  </span>
                </h1>
              </div>
              
              <ProcessingIndicator
                isVisible={isProcessing}
                currentStep={currentStep}
                progress={progress}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Upload;
