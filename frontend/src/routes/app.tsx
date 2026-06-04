import { api } from "@/lib/api";
import type { WorkflowSummary } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { AppShell } from "@/components/layout";
import { Sparkles, ArrowRight, Clock, Zap } from "lucide-react";

export const Route = createFileRoute("/app")({
  head: () => ({ meta: [{ title: "New Workflow — Arkitect" }] }),
  component: AppPage,
});

const examples = [
  "Launch a SaaS startup in 90 days",
  "Write and self-publish a technical book",
  "Run a successful Product Hunt launch",
  "Build a personal brand on LinkedIn",
];

const stages = [
  "Understanding Goal",
  "Detecting Deliverables",
  "Selecting Tools",
  "Generating Workflow",
  "Preparing Results",
];

function AppPage() {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [goal, setGoal] = useState("");
  const [generating, setGenerating] = useState(false);
  const [stage, setStage] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [recentWorkflows, setRecentWorkflows] = useState<WorkflowSummary[]>([]);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate({ to: "/login" });
    }
  }, [authLoading, user, navigate]);

  // Load recent workflows
  useEffect(() => {
    if (!user) return;
    api
      .listWorkflows(1, 4)
      .then((data) => setRecentWorkflows(data.items))
      .catch((err) => console.error("Failed to load recent workflows:", err));
  }, [user]);

  const generate = async () => {
    if (!goal.trim()) return;

    setGenerating(true);
    setStage(0);
    setError(null);

    // Animate pipeline stages
    stages.forEach((_, i) => {
      setTimeout(() => setStage(i + 1), (i + 1) * 700);
    });

    try {
      const result = await api.generateWorkflow(goal.trim());

      // Wait for animation to finish, then navigate
      const animationDuration = stages.length * 700 + 500;
      setTimeout(() => {
        navigate({
          to: "/workflow/$id",
          params: { id: result.id },
        });
      }, animationDuration);
    } catch (err) {
      console.error(err);
      setError(
        err instanceof Error ? err.message : "Failed to generate workflow. Please try again."
      );
      setGenerating(false);
    }
  };

  if (authLoading) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      {generating ? (
        <GenerationPipeline currentStage={stage} goal={goal} />
      ) : (
        <div className="container-page py-10 md:py-16">
          <div className="mx-auto max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground">
              <Sparkles className="h-3 w-3 text-primary" /> New Workflow
            </div>
            <h1 className="mt-4 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              What do you want to achieve?
            </h1>
            <p className="mt-2 text-muted-foreground">
              Describe your goal in a sentence. Arkitect will design the deliverables, tools, and step-by-step plan.
            </p>

            {error && (
              <div className="mt-4 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
                {error}
              </div>
            )}

            <div className="mt-8 rounded-xl border border-border bg-card p-2 shadow-pop focus-within:ring-2 focus-within:ring-ring">
              <textarea
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="e.g. Launch a SaaS startup in 90 days"
                rows={4}
                className="block w-full resize-none rounded-md bg-transparent px-4 py-3 text-base text-foreground placeholder:text-muted-foreground/70 focus:outline-none"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) generate();
                }}
              />
              <div className="flex items-center justify-between gap-2 border-t border-border p-2">
                <p className="px-2 text-xs text-muted-foreground hidden sm:block">
                  ⌘ + Enter to generate
                </p>
                <button
                  onClick={generate}
                  disabled={!goal.trim()}
                  className="inline-flex h-9 items-center gap-2 rounded-md px-4 text-sm font-semibold text-primary-foreground shadow-pop transition-opacity hover:opacity-90 disabled:opacity-40"
                  style={{ background: "var(--gradient-primary)" }}
                >
                  Generate Workflow <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {examples.map((ex) => (
                <button
                  key={ex}
                  onClick={() => setGoal(ex)}
                  className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
                >
                  {ex}
                </button>
              ))}
            </div>

            <div className="mt-14">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-foreground">Recent workflows</h2>
                <Link to="/history" className="text-sm font-medium text-primary hover:underline">
                  View all
                </Link>
              </div>
              {recentWorkflows.length > 0 ? (
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {recentWorkflows.map((w) => (
                    <Link
                      key={w.id}
                      to="/workflow/$id"
                      params={{ id: w.id }}
                      className="group rounded-lg border border-border bg-card p-4 shadow-card transition-shadow hover:shadow-pop"
                    >
                      <p className="text-sm font-semibold text-foreground group-hover:text-primary">{w.goal}</p>
                      <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                        <span>{w.domain}</span>
                        <span className="inline-flex items-center gap-1"><Clock className="h-3 w-3" />{w.estimated_time}</span>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="mt-4 rounded-xl border border-dashed border-border bg-card p-10 text-center">
                  <p className="text-sm text-muted-foreground">
                    No workflows yet. Generate your first one above!
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}

function GenerationPipeline({ currentStage, goal }: { currentStage: number; goal: string }) {
  return (
    <div className="container-page flex min-h-[calc(100vh-4rem)] items-center justify-center py-10">
      <div className="w-full max-w-lg">
        <div className="rounded-xl border border-border bg-card p-8 shadow-pop">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg" style={{ background: "var(--gradient-primary)" }}>
              <Zap className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Architecting</p>
              <p className="text-sm font-semibold text-foreground line-clamp-1">{goal || "Your workflow"}</p>
            </div>
          </div>

          <ul className="mt-8 space-y-3">
            {stages.map((s, i) => {
              const done = i < currentStage;
              const active = i === currentStage;
              return (
                <li key={s} className="flex items-center gap-3">
                  <span
                    className={`grid h-6 w-6 place-items-center rounded-full border text-xs transition-colors ${
                      done
                        ? "border-success bg-success text-success-foreground"
                        : active
                        ? "border-primary text-primary"
                        : "border-border text-muted-foreground"
                    }`}
                  >
                    {done ? (
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="h-3 w-3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                    ) : active ? (
                      <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
                    ) : null}
                  </span>
                  <span className={`text-sm ${done ? "text-foreground" : active ? "text-foreground" : "text-muted-foreground"}`}>
                    {s}
                  </span>
                  {active && (
                    <span className="ml-auto text-xs text-muted-foreground">working…</span>
                  )}
                </li>
              );
            })}
          </ul>

          <div className="mt-8 h-1 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full transition-all duration-500"
              style={{
                width: `${(currentStage / stages.length) * 100}%`,
                background: "var(--gradient-primary)",
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
