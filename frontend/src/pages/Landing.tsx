import LandingHeader from "@/components/LandingHeader";
import HeroSection from "@/components/HeroSection";
import ValueProposition from "@/components/ValueProposition";

const Landing = () => {
  const currentYear = new Date().getFullYear();

  return (
    <div className="min-h-screen">
      <LandingHeader />
      <main>
        <HeroSection />
        <ValueProposition />
      </main>
      <footer className="border-t border-border/60 py-10">
        <div className="container flex flex-col items-center justify-between gap-4 px-4 text-center md:flex-row md:px-6 md:text-left">
          <div>
            <p className="text-sm font-medium text-foreground">AnalytIQ Mission Console</p>
            <p className="text-sm text-muted-foreground">
              Autonomous analysis workflows for teams that operate at decision speed.
            </p>
          </div>
          <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">
            © {currentYear} AnalytIQ
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
