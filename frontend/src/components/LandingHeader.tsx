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
      <div className="container flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center space-x-2">
          <div className="h-8 w-8 rounded-lg bg-gradient-primary flex items-center justify-center">
            <span className="text-white font-bold text-sm">A</span>
          </div>
          <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            AnalytIQ
          </span>
        </div>
        
        <nav className="hidden md:flex items-center space-x-6">
          <a href="#features" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">
            Features
          </a>
          <a href="#agents" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">
            AI Agents
          </a>
          
          {/* Backend status indicator */}
          <div className="flex items-center space-x-2">
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
            size="sm"
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