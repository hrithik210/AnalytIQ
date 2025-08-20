import LandingHeader from "@/components/LandingHeader";
import HeroSection from "@/components/HeroSection";
import ValueProposition from "@/components/ValueProposition";

const Landing = () => {
  return (
    <div className="min-h-screen bg-background">
      <LandingHeader />
      <main>
        <HeroSection />
        <ValueProposition />
      </main>
      <footer className="border-t border-border/40 py-8">
        <div className="container px-4 md:px-6 text-center">
          <p className="text-sm text-muted-foreground">
            © 2024 AnalytIQ. Powered by AI-driven data analysis.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;