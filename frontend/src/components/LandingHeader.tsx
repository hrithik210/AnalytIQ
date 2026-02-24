import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { apiService } from "@/services/api";

const LandingHeader = () => {
  const navigate = useNavigate();
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await apiService.healthCheck();
        setBackendStatus("online");
      } catch (error) {
        console.warn("Backend health check failed:", error);
        setBackendStatus("offline");
      }
    };

    checkBackendHealth();
  }, []);

  const statusCopy = useMemo(() => {
    if (backendStatus === "online") {
      return {
        dot: "bg-emerald-400",
        label: "System online",
      };
    }

    if (backendStatus === "offline") {
      return {
        dot: "bg-rose-400",
        label: "System degraded",
      };
    }

    return {
      dot: "bg-amber-400 animate-pulse",
      label: "Running checks",
    };
  }, [backendStatus]);

  return (
    <header className="sticky top-0 z-50 border-b border-border/60 bg-background/80 backdrop-blur-xl">
      <div className="container flex h-20 items-center justify-between px-4 md:px-6">
        <button
          type="button"
          onClick={() => navigate("/")}
          className="group flex items-center gap-3 text-left"
          aria-label="Go to homepage"
        >
          <img src="/analytiq_logo.png" alt="AnalytIQ" className="h-16 md:h-20 w-auto object-contain transition-transform duration-300 group-hover:scale-105" />
        </button>

        <nav className="hidden items-center gap-7 lg:flex">
          <a href="#workflow" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Pipeline
          </a>
          <a href="#agents" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Agent Fleet
          </a>
          <a href="#launch" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Launch
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2 rounded-full border border-border/70 bg-card/70 px-3 py-1.5 text-xs text-muted-foreground md:flex">
            <span className={`h-2.5 w-2.5 rounded-full ${statusCopy.dot}`} aria-hidden="true" />
            {statusCopy.label}
          </div>
          <Button
            variant="outline"
            className="border-primary/40 bg-primary/10 text-primary hover:bg-primary/20 hover:text-primary"
            onClick={() => navigate("/upload")}
            disabled={backendStatus === "offline"}
          >
            Start Analysis
          </Button>
        </div>
      </div>
    </header>
  );
};

export default LandingHeader;
