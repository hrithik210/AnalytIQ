import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiService } from "@/services/api";

const LandingHeader = () => {
  const navigate = useNavigate();
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    // Check backend health on component mount
    const checkBackendHealth = async () => {
      try {
        await apiService.healthCheck();
        setBackendStatus('online');
      } catch (error) {
        console.warn('Backend health check failed:', error);
        setBackendStatus('offline');
      }
    };

    checkBackendHealth();
  }, []);

  return (
    <header className="w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="w-full flex h-16 items-center justify-between px-4 md:px-6 lg:px-8 xl:px-12">
        {/* Logo Section - Left Side */}
        <div className="flex items-center gap-3 md:gap-4">
          <div className="h-10 w-10 md:h-12 md:w-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-sm ring-1 ring-border/40">
            <span className="text-white/95 font-bold text-lg md:text-xl leading-none drop-shadow-sm select-none">A</span>
          </div>
          <span className="text-2xl md:text-3xl font-extrabold bg-gradient-primary bg-clip-text text-transparent tracking-tight leading-none">
            AnalytIQ
          </span>
        </div>
        
        {/* Navigation and Actions - Right Side */}
        <nav className="flex items-center space-x-8">
          <a href="#features" className="hidden md:block text-base font-medium text-muted-foreground hover:text-primary transition-colors">
            Features
          </a>
          <a href="#agents" className="hidden md:block text-base font-medium text-muted-foreground hover:text-primary transition-colors">
            AI Agents
          </a>
          
          {/* Backend status indicator */}
          <div className="hidden md:flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
              backendStatus === 'online' ? 'bg-green-500' :
              backendStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
            }`} />
            <span className="text-xs text-muted-foreground">
              {backendStatus === 'online' ? 'API Online' :
               backendStatus === 'offline' ? 'API Offline' : 'Checking...'}
            </span>
          </div>
          
          <Button 
            variant="outline" 
            size="default"
            onClick={() => navigate("/upload")}
            disabled={backendStatus === 'offline'}
          >
            Get Started
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default LandingHeader;