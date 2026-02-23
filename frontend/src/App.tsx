import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactElement } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import AppShell from "./components/layout/AppShell";
import Landing from "./pages/Landing";
import NotFound from "./pages/NotFound";
import Report from "./pages/Report";
import Upload from "./pages/Upload";

const queryClient = new QueryClient();

const withShell = (page: ReactElement) => <AppShell>{page}</AppShell>;

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={withShell(<Landing />)} />
          <Route path="/upload" element={withShell(<Upload />)} />
          <Route path="/report" element={withShell(<Report />)} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={withShell(<NotFound />)} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
