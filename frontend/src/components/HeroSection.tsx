import { useNavigate } from "react-router-dom";
import { ArrowRight, Gauge, Orbit, Radar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion, Variants } from "framer-motion";
import DataNodeNetwork from "./DataNodeNetwork";

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
    hidden: { opacity: 0, y: 30 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 80,
        damping: 15,
      },
    },
  };

  return (
    <section className="relative overflow-hidden pb-16 pt-20 md:pt-32 min-h-[90vh] flex items-center">
      <DataNodeNetwork />
      
      <div className="container px-4 md:px-6 relative z-10">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="mx-auto max-w-5xl text-center"
        >
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 rounded-full border border-primary/35 bg-primary/10 px-4 py-1.5 text-xs font-medium uppercase tracking-[0.18em] text-primary backdrop-blur-sm">
            Autonomous Data Operations
          </motion.div>

          <motion.h1 variants={itemVariants} className="bricolage mt-8 text-balance text-5xl font-bold leading-[1.05] tracking-tight md:text-7xl lg:text-8xl">
            Your Data Gets a<br/>
            <span className="bg-gradient-primary bg-clip-text text-transparent italic">World-Class AI Team</span>
            <br/>Instantly.
          </motion.h1>

          <motion.p variants={itemVariants} className="mx-auto mt-7 max-w-3xl text-balance text-lg leading-relaxed text-muted-foreground md:text-2xl font-medium">
            Drop in a CSV and launch a coordinated analyst swarm that structures, audits, explains, and visualizes your
            data into a board-ready report while you focus on decisions.
          </motion.p>

          <motion.div variants={itemVariants} className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                size="lg"
                onClick={() => navigate("/upload")}
                className="group h-14 min-w-[220px] bg-gradient-primary text-lg font-semibold text-primary-foreground shadow-glow border-none"
              >
                Start Analysis
                <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
              </Button>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                size="lg"
                variant="outline"
                asChild
                className="h-14 min-w-[220px] border-border/70 bg-card/40 backdrop-blur-md text-lg hover:bg-card/80 transition-colors"
              >
                <a href="#workflow">See Pipeline</a>
              </Button>
            </motion.div>
          </motion.div>

          <motion.div variants={itemVariants} className="mt-20 grid gap-6 md:grid-cols-3">
            {stats.map((stat, i) => (
              <motion.article
                key={stat.label}
                whileHover={{ y: -5, transition: { type: "spring", stiffness: 300, damping: 20 } }}
                className="panel-soft rounded-2xl border border-border/70 p-6 text-left backdrop-blur-sm bg-card/40 hover:bg-card/60 transition-colors"
              >
                <div className="mb-5 flex h-10 w-10 items-center justify-center rounded-xl border border-primary/40 bg-primary/10 text-primary shadow-[0_0_15px_rgba(11,244,243,0.2)]">
                  <stat.icon className="h-5 w-5" />
                </div>
                <p className="bricolage text-2xl font-bold text-foreground tracking-tight">{stat.value}</p>
                <p className="mt-1.5 text-sm font-medium text-muted-foreground">{stat.label}</p>
              </motion.article>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
