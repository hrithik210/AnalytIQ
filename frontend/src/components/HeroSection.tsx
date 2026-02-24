import { useNavigate } from "react-router-dom";
import { ArrowRight, Gauge, Orbit, Radar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion, Variants } from "framer-motion";
import { useState } from "react";
import MultiAgentVideography from "./MultiAgentVideography";

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
  const [introComplete, setIntroComplete] = useState(false);

  // Main Hero Typography Track-in
  // Triggered only when introComplete is true.
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        type: "tween",
        ease: "circOut",
        duration: 0.8
      },
    },
  };

  return (
    <section className="relative overflow-hidden pb-16 pt-20 md:pt-32 min-h-[100vh] flex items-center">
      <CinematicIntro onSequenceComplete={() => setSequenceComplete(true)} />
      
      <div className="container px-4 md:px-6 relative z-10 pointer-events-none">
        
        {sequenceComplete && (
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            animate="show"
            className="mx-auto max-w-5xl text-center pointer-events-auto"
          >
            <motion.div variants={itemVariants} className="inline-flex items-center gap-2 rounded-[0.25rem] border border-border bg-card px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.18em] text-foreground">
              A Soothing Experience
            </motion.div>

            <motion.h1 variants={itemVariants} style={{ perspective: '1000px' }} className="bricolage mt-8 text-balance text-6xl font-semibold leading-[1.05] tracking-tight text-foreground md:text-7xl lg:text-8xl">
              Focus on Decisions.<br/>
              Let the Data Flow.
            </motion.h1>

            <motion.p variants={itemVariants} className="mx-auto mt-7 max-w-3xl text-balance text-xl leading-relaxed text-muted-foreground font-medium">
              Drop in a CSV and launch an automated analyst swarm that structures, audits, explains, and visualizes your
              data into a board-ready report instantly.
            </motion.p>

          <motion.div variants={itemVariants} className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                size="lg"
                onClick={() => navigate("/upload")}
                className="group h-14 min-w-[220px] bg-foreground text-background text-lg font-semibold hover:bg-foreground/90 transition-colors shadow-none rounded-[0.5rem] border border-transparent"
              >
                Start Analysis
                <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
              </Button>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                size="lg"
                variant="outline"
                asChild
                className="h-14 min-w-[220px] border-border bg-background text-foreground text-lg font-semibold hover:bg-secondary transition-colors rounded-[0.5rem]"
              >
                <a href="#workflow">See Pipeline</a>
              </Button>
            </motion.div>
          </motion.div>

            <motion.div variants={itemVariants} className="mt-24 grid gap-8 md:grid-cols-3">
              {stats.map((stat, i) => (
                <motion.article
                  key={stat.label}
                  whileHover={{ y: -5, transition: { type: "tween", ease: "easeOut", duration: 0.2 } }}
                  className="rounded-[0.5rem] border border-border p-8 text-left bg-card hover:border-muted-foreground transition-colors shadow-none"
                >
                  <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-[0.5rem] bg-background text-foreground border border-border">
                    <stat.icon className="h-6 w-6 text-foreground" />
                  </div>
                  <p className="bricolage text-3xl font-semibold text-foreground tracking-tight">{stat.value}</p>
                  <p className="mt-2 text-base font-medium text-muted-foreground">{stat.label}</p>
                </motion.article>
              ))}
            </motion.div>
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default HeroSection;
