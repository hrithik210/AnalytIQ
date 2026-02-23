import { useNavigate } from "react-router-dom";
import { ArrowRight, Gauge, Orbit, Radar } from "lucide-react";
import { Button } from "@/components/ui/button";

const stats = [
  {
    label: "Autonomous agents",
    value: "6",
    icon: Orbit,
  },
  {
    label: "Median run time",
    value: "~2 min",
    icon: Gauge,
  },
  {
    label: "Insight coverage",
    value: "Executive to chart-level",
    icon: Radar,
  },
];

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative overflow-hidden pb-16 pt-20 md:pt-24">
      <div className="container px-4 md:px-6">
        <div className="mx-auto max-w-5xl text-center">
          <div className="animate-enter-fade inline-flex items-center gap-2 rounded-full border border-primary/35 bg-primary/10 px-4 py-1.5 text-xs font-medium uppercase tracking-[0.18em] text-primary">
            Autonomous Data Operations
          </div>

          <h1 className="animate-enter-up mt-8 text-balance text-5xl font-semibold leading-[1.05] tracking-tight md:text-7xl">
            Your Data Gets a
            <span className="bg-gradient-primary bg-clip-text text-transparent"> World-Class AI Team</span>
            , Instantly.
          </h1>

          <p className="animate-enter-up-delay mx-auto mt-7 max-w-3xl text-balance text-lg leading-relaxed text-muted-foreground md:text-2xl">
            Drop in a CSV and launch a coordinated analyst swarm that structures, audits, explains, and visualizes your
            data into a board-ready report while you focus on decisions.
          </p>

          <div className="animate-enter-up-delay-2 mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Button
              size="lg"
              onClick={() => navigate("/upload")}
              className="group h-12 min-w-52 bg-gradient-primary text-base font-semibold text-primary-foreground shadow-glow transition-transform duration-300 hover:scale-[1.02]"
            >
              Start Analysis
              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              asChild
              className="h-12 min-w-52 border-border/70 bg-card/70 text-base hover:bg-card"
            >
              <a href="#workflow">See Pipeline</a>
            </Button>
          </div>

          <div className="mt-14 grid gap-4 md:grid-cols-3">
            {stats.map((stat) => (
              <article
                key={stat.label}
                className="panel-soft rounded-2xl border border-border/70 p-5 text-left animate-enter-fade"
              >
                <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-lg border border-primary/40 bg-primary/10 text-primary">
                  <stat.icon className="h-4 w-4" />
                </div>
                <p className="text-lg font-semibold text-foreground">{stat.value}</p>
                <p className="mt-1 text-sm text-muted-foreground">{stat.label}</p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
