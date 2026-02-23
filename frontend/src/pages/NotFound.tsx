import { Link, useLocation } from "react-router-dom";
import { useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="container flex min-h-screen items-center justify-center px-4 py-12 md:px-6">
      <div className="panel-soft w-full max-w-xl rounded-3xl border border-border/70 p-10 text-center">
        <p className="text-xs uppercase tracking-[0.18em] text-primary">Navigation Fault</p>
        <h1 className="mt-4 text-5xl font-semibold tracking-tight md:text-6xl">404</h1>
        <p className="mx-auto mt-4 max-w-md text-muted-foreground">
          The route <span className="font-medium text-foreground">{location.pathname}</span> is not available in this
          console session.
        </p>
        <div className="mt-8">
          <Button asChild size="lg" className="bg-gradient-primary text-primary-foreground shadow-glow">
            <Link to="/">
              <ArrowLeft className="h-4 w-4" />
              Return to Home
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
