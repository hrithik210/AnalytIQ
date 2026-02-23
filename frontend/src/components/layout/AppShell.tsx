import { type ReactNode } from "react";

interface AppShellProps {
  children: ReactNode;
}

const AppShell = ({ children }: AppShellProps) => {
  return (
    <div className="relative min-h-screen overflow-x-hidden bg-background text-foreground">
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-0 bg-shell-atmosphere"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-0 bg-shell-grid opacity-35"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none fixed -top-40 left-1/2 z-0 h-[26rem] w-[42rem] -translate-x-1/2 rounded-full bg-shell-glow blur-[120px]"
      />

      <div className="relative z-10">{children}</div>
    </div>
  );
};

export default AppShell;
