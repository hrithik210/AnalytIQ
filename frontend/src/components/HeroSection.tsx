import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ArrowRight, Sparkles } from "lucide-react";
import heroImage from "@/assets/hero-bg.jpg";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-[80vh] flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10"
        style={{ backgroundImage: `url(${heroImage})` }}
      />
      
      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-hero" />
      
      <div className="relative container px-4 md:px-6 text-center z-10">
        <div className="space-y-8 max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium">
            <Sparkles className="h-4 w-4" />
            AI-Powered Data Analysis
          </div>
          
          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
            Meet Your{" "}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              Automated
            </span>
            <br />
            Data Analyst Team
          </h1>
          
          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Upload a CSV, and watch as AI agents analyze, visualize, and narrate 
            insights from your data—automatically. No manual work required.
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button 
              size="lg" 
              className="text-lg px-8 py-6 bg-gradient-primary hover:shadow-glow transition-all duration-300 group"
              onClick={() => navigate("/upload")}
            >
              Analyze My Data
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            
            <Button 
              variant="outline" 
              size="lg" 
              className="text-lg px-8 py-6"
            >
              Watch Demo
            </Button>
          </div>
          
          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 pt-12 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">6</div>
              <div className="text-sm text-muted-foreground">AI Agents</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">~2min</div>
              <div className="text-sm text-muted-foreground">Analysis Time</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">100%</div>
              <div className="text-sm text-muted-foreground">Automated</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;