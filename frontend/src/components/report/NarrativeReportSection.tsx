import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  FileText, 
  Target, 
  Database, 
  TrendingUp, 
  BarChart3, 
  ShieldCheck, 
  Lightbulb 
} from "lucide-react";

interface StorytellerOutput {
  executive_summary: string;
  key_findings: string[];
  data_overview: string;
  analysis_narrative: string;
  visualizations_summary: string;
  qa_considerations?: string;
  conclusion: string;
}

interface NarrativeReportSectionProps {
  storytellerOutput: StorytellerOutput;
}

const NarrativeReportSection: React.FC<NarrativeReportSectionProps> = ({ 
  storytellerOutput 
}) => {
  return (
    <div className="space-y-6">
      {/* Executive Summary */}
      <Card className="border-0 bg-gradient-primary/5 shadow-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-primary">
            <Target className="h-5 w-5" />
            Executive Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg leading-relaxed">{storytellerOutput.executive_summary}</p>
        </CardContent>
      </Card>

      {/* Key Findings */}
      <Card className="border-0 bg-gradient-card shadow-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5" />
            Key Findings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {storytellerOutput.key_findings.map((finding, index) => (
              <div key={index} className="flex items-start gap-3">
                <Badge variant="outline" className="mt-1 text-xs px-2 py-1">
                  {index + 1}
                </Badge>
                <p className="flex-1 leading-relaxed">{finding}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Data Overview */}
        <Card className="border-0 bg-gradient-card shadow-card">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Database className="h-5 w-5" />
              Data Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed">{storytellerOutput.data_overview}</p>
          </CardContent>
        </Card>

        {/* Visualizations Summary */}
        <Card className="border-0 bg-gradient-card shadow-card">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <BarChart3 className="h-5 w-5" />
              Visualizations Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed">{storytellerOutput.visualizations_summary}</p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analysis Narrative */}
      <Card className="border-0 bg-gradient-card shadow-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Detailed Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-gray max-w-none">
            <p className="leading-relaxed whitespace-pre-line">
              {storytellerOutput.analysis_narrative}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* QA Considerations (if present) */}
      {storytellerOutput.qa_considerations && (
        <Card className="border-0 bg-yellow-50 dark:bg-yellow-950/20 shadow-card">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-yellow-800 dark:text-yellow-200">
              <ShieldCheck className="h-5 w-5" />
              Quality Considerations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed text-yellow-700 dark:text-yellow-300">
              {storytellerOutput.qa_considerations}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Conclusion */}
      <Card className="border-0 bg-gradient-card shadow-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Conclusion
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg leading-relaxed font-medium">
            {storytellerOutput.conclusion}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default NarrativeReportSection;