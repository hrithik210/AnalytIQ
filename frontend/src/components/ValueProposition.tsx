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
  Target,
  UploadCloud,
  Layers3,
  LineChart,
  FileText
} from "lucide-react";

const agents = [
  {
    name: "Schema Expert",
    role: "Structural audit",
    output: "Column map, type confidence, anomaly surface",
    icon: Database,
    color: "text-cyan-300"
  },
  {
    name: "Data Cleaner", 
    role: "Quality remediation",
    output: "Missing values, duplicates, and outlier treatment",
    icon: Sparkles,
    color: "text-emerald-300"
  },
  {
    name: "Stats Guru",
    role: "Statistical core",
    output: "Distribution checks, trend extraction, signal ranking",
    icon: BarChart3,
    color: "text-sky-300"
  },
  {
    name: "Chart Wizard",
    role: "Visualization engine",
    output: "Plot-ready charts optimized for decision review",
    icon: FileSpreadsheet,
    color: "text-amber-300"
  },
  {
    name: "Quality Checker",
    role: "Integrity guard",
    output: "Cross-agent consistency and confidence controls",
    icon: ShieldCheck,
    color: "text-rose-300"
  },
  {
    name: "Storyteller",
    role: "Narrative synthesis",
    output: "Executive summary, findings, and recommended next moves",
    icon: MessageSquare,
    color: "text-violet-300"
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

const workflow = [
  {
    title: "Upload once",
    description: "Drop your CSV and trigger the full workflow in one click.",
    icon: UploadCloud,
  },
  {
    title: "Multi-agent execution",
    description: "Specialists coordinate quality checks, analysis, and chart generation.",
    icon: Layers3,
  },
  {
    title: "Insight synthesis",
    description: "Statistical outcomes and visuals are connected into one narrative.",
    icon: LineChart,
  },
  {
    title: "Executive-ready output",
    description: "Receive a concise report built for action, not just observation.",
    icon: FileText,
  }
];

const ValueProposition = () => {
  return (
    <section id="features" className="py-24 bg-muted/30">
      <div className="container px-4 md:px-6">
        <div id="workflow" className="mb-20">
          <div className="mx-auto mb-10 max-w-3xl text-center">
            <p className="mb-3 text-xs uppercase tracking-[0.18em] text-primary">How It Works</p>
            <h2 className="text-balance text-3xl font-semibold leading-tight md:text-5xl">
              One pipeline. Zero handoffs. Relentless output.
            </h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {workflow.map((step, index) => (
              <Card key={step.title} className="panel-soft border-border/70">
                <CardContent className="p-6">
                  <div className="mb-6 flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-primary/40 bg-primary/10 text-primary">
                      <step.icon className="h-5 w-5" />
                    </div>
                    <span className="text-xs font-semibold text-muted-foreground">0{index + 1}</span>
                  </div>
                  <h3 className="text-lg font-semibold">{step.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{step.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

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
        <div id="agents" className="mb-12 text-center">
          <p className="mb-3 text-xs uppercase tracking-[0.18em] text-primary">Agent Fleet</p>
          <h2 className="text-balance text-3xl font-semibold leading-tight md:text-5xl">
            Each specialist owns one job.
            <span className="bg-gradient-primary bg-clip-text text-transparent"> Together, they own the outcome.</span>
          </h2>
          <p className="mx-auto mt-4 max-w-3xl text-lg text-muted-foreground">
            AnalytIQ orchestrates six focused agents so every report ships with structure, confidence, and narrative
            clarity.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => (
            <Card key={index} className="group panel-soft border-border/70 transition-all duration-300 hover:-translate-y-1 hover:shadow-glow">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className={`rounded-lg border border-border/80 bg-background/60 p-3 ${agent.color}`}>
                    <agent.icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <p className="mb-1 text-xs uppercase tracking-[0.13em] text-muted-foreground">{agent.role}</p>
                    <h3 className="mb-2 font-semibold text-foreground group-hover:text-primary transition-colors">
                      {agent.name}
                    </h3>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                      {agent.output}
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
