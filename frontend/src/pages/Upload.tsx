import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Upload as UploadIcon } from "lucide-react";
import FileUploader from "@/components/upload/FileUploader";
import ProcessingIndicator from "@/components/upload/ProcessingIndicator";
import { useToast } from "@/hooks/use-toast";

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
    
    // Simulate the analysis process with progress updates
    const steps = [
      { message: "Uploading file and initializing agents...", duration: 2000, progress: 20 },
      { message: "Schema Expert analyzing data structure...", duration: 3000, progress: 40 },
      { message: "Data Cleaner processing quality issues...", duration: 2500, progress: 60 },
      { message: "Stats Guru generating insights...", duration: 3500, progress: 80 },
      { message: "Chart Wizard creating visualizations...", duration: 2000, progress: 90 },
      { message: "Storyteller crafting narrative...", duration: 1500, progress: 100 }
    ];

    for (const step of steps) {
      setCurrentStep(step.message);
      setProgress(step.progress);
      await new Promise(resolve => setTimeout(resolve, step.duration));
    }

    // Simulate navigation to report page
    toast({
      title: "Analysis Complete!",
      description: "Your data has been successfully analyzed.",
    });
    
    // Navigate to report page with mock data
    navigate("/report", { 
      state: { 
        reportData: {
          report_id: "mock-uuid-123",
          storyteller_output: {
            executive_summary: "This dataset contains sales data with 1,247 records across 8 columns. The analysis reveals strong seasonal trends and significant growth opportunities in the Q4 period.",
            key_findings: [
              "Sales peak during Q4 with 45% higher revenue than Q1",
              "Product Category A shows 23% year-over-year growth",
              "Regional performance varies significantly, with East region outperforming by 18%",
              "Customer retention rate improved by 12% compared to previous period"
            ],
            data_overview: "The dataset contains comprehensive sales information including transaction dates, product categories, regional data, customer segments, and revenue figures. Data quality is high with minimal missing values.",
            analysis_narrative: "Our analysis reveals several key patterns in your sales data. The seasonal trend shows a clear preference for purchases during the holiday season, with November and December accounting for nearly 40% of annual sales.\n\nThe geographic distribution shows the East region significantly outperforming other regions, suggesting successful regional strategies that could be replicated elsewhere.\n\nCustomer segmentation analysis indicates that premium customers contribute disproportionately to revenue, representing 20% of customers but 60% of total revenue.",
            visualizations_summary: "Generated 4 key visualizations: quarterly sales trends, regional performance comparison, product category analysis, and customer segment distribution. Charts highlight seasonal patterns and growth opportunities.",
            qa_considerations: "Note: Some records had missing customer segment data (3.2% of total). These were handled using statistical imputation methods.",
            conclusion: "The data shows a healthy business with strong seasonal performance and clear growth opportunities in underperforming regions. Recommend focusing on Q4 strategies and expanding successful East region tactics to other territories."
          },
          chart_data: [
            { data: [], layout: {}, config: {} },
            { data: [], layout: {}, config: {} },
            { error: "Insufficient data for correlation analysis" },
            { data: [], layout: {}, config: {} }
          ]
        }
      }
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/40 bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between px-4 md:px-6">
          <Button 
            variant="ghost" 
            onClick={() => navigate("/")}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Button>
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <span className="text-white font-bold text-sm">A</span>
            </div>
            <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              AnalytIQ
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container px-4 md:px-6 py-12">
        <div className="max-w-4xl mx-auto">
          {!isProcessing ? (
            <div className="text-center space-y-8">
              {/* Title */}
              <div className="space-y-4">
                <h1 className="text-4xl md:text-5xl font-bold">
                  Upload Your{" "}
                  <span className="bg-gradient-primary bg-clip-text text-transparent">
                    CSV File
                  </span>
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                  Upload your CSV file to begin the automated analysis. 
                  Our AI team will handle the rest.
                </p>
              </div>

              {/* Instructions */}
              <Card className="border-0 bg-gradient-card shadow-card max-w-2xl mx-auto">
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
                className="text-lg px-8 py-6 bg-gradient-primary hover:shadow-glow transition-all duration-300"
              >
                Start Analysis
              </Button>
            </div>
          ) : (
            <div className="space-y-8">
              <div className="text-center">
                <h1 className="text-4xl md:text-5xl font-bold mb-4">
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