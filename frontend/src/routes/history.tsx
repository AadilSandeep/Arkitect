import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { AppShell } from "@/components/layout";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api";
import type { WorkflowSummary } from "@/lib/api";
import { Clock, Trash2, ArrowRight, Search, Loader2 } from "lucide-react";

export const Route = createFileRoute("/history")({
  head: () => ({ meta: [{ title: "Workflow History — Arkitect" }] }),
  component: History,
});

function History() {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [items, setItems] = useState<WorkflowSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [deletingId, setDeletingId] = useState<string | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate({ to: "/login" });
    }
  }, [authLoading, user, navigate]);

  // Load workflows from API
  useEffect(() => {
    if (!user) return;
    setLoading(true);
    api
      .listWorkflows(1, 100)
      .then((data) => {
        setItems(data.items);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load workflows:", err);
        setLoading(false);
      });
  }, [user]);

  const handleDelete = async (id: string) => {
    setDeletingId(id);
    try {
      await api.deleteWorkflow(id);
      setItems((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      console.error("Failed to delete workflow:", err);
    } finally {
      setDeletingId(null);
    }
  };

  const filtered = items.filter((w) =>
    w.goal.toLowerCase().includes(query.toLowerCase())
  );

  if (authLoading || loading) {
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
      <div className="container-page py-8 md:py-10">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">Workflow History</h1>
            <p className="mt-1 text-sm text-muted-foreground">All the plans you've architected.</p>
          </div>
          <Link
            to="/app"
            className="inline-flex h-9 items-center gap-2 rounded-md px-4 text-sm font-semibold text-primary-foreground shadow-pop"
            style={{ background: "var(--gradient-primary)" }}
          >
            New workflow
          </Link>
        </div>

        <div className="mt-6 flex h-10 items-center gap-2 rounded-md border border-border bg-card px-3 shadow-card">
          <Search className="h-4 w-4 text-muted-foreground" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search workflows..."
            className="h-full w-full bg-transparent text-sm text-foreground placeholder:text-muted-foreground/70 focus:outline-none"
          />
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {filtered.map((w) => (
            <div key={w.id} className="group rounded-xl border border-border bg-card p-5 shadow-card transition-shadow hover:shadow-pop">
              <div className="flex items-start justify-between gap-3">
                <h2 className="text-base font-semibold text-foreground">{w.goal}</h2>
                <span className="rounded-full bg-secondary px-2 py-0.5 text-xs text-muted-foreground">{w.domain}</span>
              </div>
              <div className="mt-3 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
                <span className="inline-flex items-center gap-1"><Clock className="h-3 w-3" />{w.estimated_time}</span>
                <span>Created {new Date(w.created_at).toLocaleDateString()}</span>
                <span className="capitalize">{w.complexity} complexity</span>
              </div>
              <div className="mt-5 flex items-center justify-between border-t border-border pt-4">
                <button
                  onClick={() => handleDelete(w.id)}
                  disabled={deletingId === w.id}
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground hover:text-destructive disabled:opacity-50"
                >
                  {deletingId === w.id ? (
                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  ) : (
                    <Trash2 className="h-3.5 w-3.5" />
                  )}
                  Delete
                </button>
                <Link
                  to="/workflow/$id"
                  params={{ id: w.id }}
                  className="inline-flex items-center gap-1.5 text-sm font-semibold text-primary hover:underline"
                >
                  Open <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="col-span-full rounded-xl border border-dashed border-border bg-card p-10 text-center">
              <p className="text-sm text-muted-foreground">
                {items.length === 0
                  ? "No workflows yet. Generate your first one!"
                  : "No workflows match your search."}
              </p>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
