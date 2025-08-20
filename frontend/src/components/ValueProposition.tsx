import { Card, CardContent } from "@/components/ui/card";
import { 
  Database, 
  Sparkles, 
  BarChart3, 
  FileSpreadsheet, 
  ShieldCheck, 
  MessageSquare,
  Zap,
  Clock,
  Target
} from "lucide-react";

const agents = [
  {
    name: "Schema Expert",
    description: "Analyzes data structure and quality",
    icon: Database,
    color: "text-blue-500"
  },
  {
    name: "Data Cleaner", 
    description: "Identifies and handles data issues",
    icon: Sparkles,
    color: "text-purple-500"
  },
  {
    name: "Stats Guru",
    description: "Performs statistical analysis",
    icon: BarChart3,
    color: "text-green-500"
  },
  {
    name: "Chart Wizard",
    description: "Creates insightful visualizations",
    icon: FileSpreadsheet,
    color: "text-orange-500"
  },
  {
    name: "Quality Checker",
    description: "Validates analysis integrity",
    icon: ShieldCheck,
    color: "text-red-500"
  },
  {
    name: "Storyteller",
    description: "Generates narrative insights",
    icon: MessageSquare,
    color: "text-indigo-500"
  }
];

const benefits = [
  {
    title: "Lightning Speed",
    description: "Complete analysis in minutes, not hours",
    icon: Zap,
    color: "text-yellow-500"
  },
  {
    title: "Full Automation", 
    description: "Zero manual intervention required",
    icon: Clock,
    color: "text-blue-500"
  },
  {
    title: "Comprehensive Analysis",
    description: "Statistical insights, visualizations, and narratives",
    icon: Target,
    color: "text-green-500"
  }
];

const ValueProposition = () => {
  return (
    <section id="features" className="py-24 bg-muted/30">
      <div className="container px-4 md:px-6">
        {/* Benefits Section */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Why Choose{" "}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              AnalytIQ
            </span>
            ?
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform your data analysis workflow with AI-powered automation
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          {benefits.map((benefit, index) => (
            <Card key={index} className="text-center border-0 bg-gradient-card shadow-card hover:shadow-glow transition-all duration-300">
              <CardContent className="pt-8 pb-6">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-background mb-6 ${benefit.color}`}>
                  <benefit.icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold mb-3">{benefit.title}</h3>
                <p className="text-muted-foreground">{benefit.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* AI Agents Section */}
        <div id="agents" className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Meet Your{" "}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              AI Agent Team
            </span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Six specialized AI agents work together to deliver comprehensive data insights
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => (
            <Card key={index} className="group hover:shadow-glow transition-all duration-300 border-0 bg-gradient-card">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-lg bg-background ${agent.color}`}>
                    <agent.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-2 group-hover:text-primary transition-colors">
                      {agent.name}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {agent.description}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ValueProposition;