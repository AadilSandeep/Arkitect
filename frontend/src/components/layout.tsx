import { Link, useRouterState, useNavigate } from "@tanstack/react-router";
import { Layers, LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api";
import type { WorkflowSummary } from "@/lib/api";
import { useState, useEffect } from "react";

export function Logo({ className = "" }: { className?: string }) {
  return (
    <Link to="/" className={`flex items-center gap-2 font-semibold tracking-tight ${className}`}>
      <span className="grid h-7 w-7 place-items-center rounded-md" style={{ background: "var(--gradient-primary)" }}>
        <Layers className="h-4 w-4 text-white" />
      </span>
      <span className="text-foreground">Arkitect</span>
    </Link>
  );
}

export function MarketingNav() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="container-page flex h-16 items-center justify-between">
        <Logo />
        <nav className="hidden items-center gap-8 text-sm text-muted-foreground md:flex">
          <a href="#features" className="transition-colors hover:text-foreground">Features</a>
          <a href="#example" className="transition-colors hover:text-foreground">Example</a>
          <Link to="/history" className="transition-colors hover:text-foreground">History</Link>
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/login" className="hidden text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex">
            Log in
          </Link>
          <Link
            to="/app"
            className="inline-flex h-9 items-center rounded-md px-4 text-sm font-medium text-primary-foreground shadow-pop transition-opacity hover:opacity-90"
            style={{ background: "var(--gradient-primary)" }}
          >
            Open app
          </Link>
        </div>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-border/60 bg-background">
      <div className="container-page flex flex-col items-start justify-between gap-6 py-10 md:flex-row md:items-center">
        <div className="space-y-2">
          <Logo />
          <p className="text-sm text-muted-foreground">Architect your path to execution.</p>
        </div>
        <div className="grid grid-cols-3 gap-8 text-sm text-muted-foreground">
          <div className="space-y-2">
            <p className="font-medium text-foreground">Product</p>
            <a href="#features" className="block hover:text-foreground">Features</a>
            <a href="#example" className="block hover:text-foreground">Example</a>
          </div>
          <div className="space-y-2">
            <p className="font-medium text-foreground">Company</p>
            <a href="#" className="block hover:text-foreground">About</a>
            <a href="#" className="block hover:text-foreground">Contact</a>
          </div>
          <div className="space-y-2">
            <p className="font-medium text-foreground">Legal</p>
            <a href="#" className="block hover:text-foreground">Privacy</a>
            <a href="#" className="block hover:text-foreground">Terms</a>
          </div>
        </div>
      </div>
      <div className="border-t border-border/60">
        <div className="container-page py-4 text-xs text-muted-foreground">
          © {new Date().getFullYear()} Arkitect. All rights reserved.
        </div>
      </div>
    </footer>
  );
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const [recentWorkflows, setRecentWorkflows] = useState<WorkflowSummary[]>([]);

  // Load recent workflows for the sidebar
  useEffect(() => {
    if (!user) return;
    api
      .listWorkflows(1, 3)
      .then((data) => setRecentWorkflows(data.items))
      .catch(() => {});
  }, [user]);

  const handleSignOut = async () => {
    await signOut();
    navigate({ to: "/login" });
  };

  const navItems = [
    { to: "/app", label: "New Workflow", icon: "plus" as const },
    { to: "/history", label: "History", icon: "clock" as const },
  ];

  // User initials for avatar
  const initials = user?.user_metadata?.full_name
    ? (user.user_metadata.full_name as string)
        .split(" ")
        .map((n: string) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : user?.email?.[0]?.toUpperCase() ?? "?";

  return (
    <div className="flex min-h-screen w-full bg-background">
      {/* Sidebar (desktop) */}
      <aside className="hidden w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar md:flex">
        <div className="flex h-16 items-center border-b border-sidebar-border px-5">
          <Logo />
        </div>
        <nav className="flex-1 space-y-1 p-3">
          {navItems.map((item) => {
            const active = pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  active
                    ? "bg-sidebar-accent text-sidebar-accent-foreground"
                    : "text-muted-foreground hover:bg-sidebar-accent/60 hover:text-sidebar-accent-foreground"
                }`}
              >
                <SidebarIcon name={item.icon} />
                {item.label}
              </Link>
            );
          })}
          {recentWorkflows.length > 0 && (
            <div className="pt-4">
              <p className="px-3 pb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
                Recent
              </p>
              {recentWorkflows.map((w) => (
                <Link
                  key={w.id}
                  to="/workflow/$id"
                  params={{ id: w.id }}
                  className="block truncate rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-sidebar-accent/60 hover:text-sidebar-accent-foreground"
                >
                  {w.goal}
                </Link>
              ))}
            </div>
          )}
        </nav>

        {/* User section at bottom */}
        <div className="border-t border-sidebar-border p-3 space-y-1">
          {user && (
            <div className="flex items-center gap-3 rounded-md px-3 py-2">
              <div className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                {initials}
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-foreground">
                  {(user.user_metadata?.full_name as string) || "User"}
                </p>
                <p className="truncate text-xs text-muted-foreground">{user.email}</p>
              </div>
            </div>
          )}
          <button
            onClick={handleSignOut}
            className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-sidebar-accent/60 hover:text-destructive"
          >
            <LogOut className="h-4 w-4" />
            Log out
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex min-w-0 flex-1 flex-col pb-16 md:pb-0">
        {/* Mobile top bar */}
        <header className="flex h-14 items-center justify-between border-b border-border bg-background px-4 md:hidden">
          <Logo />
          {user ? (
            <button
              onClick={handleSignOut}
              className="text-sm font-medium text-muted-foreground"
            >
              Log out
            </button>
          ) : (
            <Link to="/login" className="text-sm font-medium text-muted-foreground">
              Log in
            </Link>
          )}
        </header>
        <main className="flex-1">{children}</main>
      </div>

      {/* Mobile bottom nav */}
      <nav className="fixed inset-x-0 bottom-0 z-30 flex h-16 border-t border-border bg-background md:hidden">
        {[
          { to: "/app", label: "Workflow", icon: "plus" as const },
          { to: "/history", label: "History", icon: "clock" as const },
        ].map((item) => {
          const active = pathname === item.to;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`flex flex-1 flex-col items-center justify-center gap-1 text-xs ${
                active ? "text-primary" : "text-muted-foreground"
              }`}
            >
              <SidebarIcon name={item.icon} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

function SidebarIcon({ name }: { name: "plus" | "clock" | "settings" }) {
  const cls = "h-4 w-4";
  if (name === "plus") return (<svg className={cls} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M5 12h14"/></svg>);
  if (name === "clock") return (<svg className={cls} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>);
  return (<svg className={cls} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9c.36.12.69.32.96.59"/></svg>);
}
