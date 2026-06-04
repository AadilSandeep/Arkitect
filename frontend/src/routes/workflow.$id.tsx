import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { AppShell } from "@/components/layout";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api";
import type { WorkflowDetail, WorkflowResponseData } from "@/lib/api";
import {
  ArrowLeft, Clock, Layers, Activity, ChevronDown, CheckCircle2,
  Zap, DollarSign, Award, GraduationCap, Copy, Sparkles, Loader2,
} from "lucide-react";

export const Route = createFileRoute("/workflow/$id")({
  head: () => ({
    meta: [{ title: "Workflow — Arkitect" }],
  }),
  component: WorkflowPage,
});

// ---------------------------------------------------------------------------
// Types for the alternative cards
// ---------------------------------------------------------------------------

type AlternativeType = "Fastest" | "Cheapest" | "Highest Quality" | "Beginner Friendly";

interface AlternativeDisplay {
  type: AlternativeType;
  summary: string;
  tools: string[];
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

function WorkflowPage() {
  const { id } = Route.useParams();
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();
  const [workflow, setWorkflow] = useState<WorkflowDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate({ to: "/login" });
    }
  }, [authLoading, user, navigate]);

  // Load workflow from API
  useEffect(() => {
    if (!user) return;
    setLoading(true);
    api
      .getWorkflow(id)
      .then((data) => {
        setWorkflow(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load workflow:", err);
        setError("Workflow not found or you don't have access.");
        setLoading(false);
      });
  }, [id, user]);

  if (authLoading || loading) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </AppShell>
    );
  }

  if (error || !workflow) {
    return (
      <AppShell>
        <div className="container-page py-20 text-center">
          <h1 className="text-2xl font-semibold text-foreground">Workflow not found</h1>
          <p className="mt-2 text-muted-foreground">
            {error || "It may have been deleted or the link is incorrect."}
          </p>
          <Link
            to="/app"
            className="mt-6 inline-flex h-10 items-center rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground"
          >
            New workflow
          </Link>
        </div>
      </AppShell>
    );
  }

  const data = workflow.response_data;

  // Build alternatives array for the card grid
  const alternatives: AlternativeDisplay[] = data.alternative_workflows
    ? [
        { type: "Fastest", ...data.alternative_workflows.fastest },
        { type: "Cheapest", ...data.alternative_workflows.cheapest },
        { type: "Highest Quality", ...data.alternative_workflows.highest_quality },
        { type: "Beginner Friendly", ...data.alternative_workflows.beginner_friendly },
      ]
    : [];

  // Build knowledge areas list
  const knowledgeGroups = data.knowledge_areas
    ? [
        { level: "high" as const, label: "High Importance", items: data.knowledge_areas.high || [] },
        { level: "medium" as const, label: "Medium Importance", items: data.knowledge_areas.medium || [] },
        { level: "low" as const, label: "Low Importance", items: data.knowledge_areas.low || [] },
      ]
    : [];

  return (
    <AppShell>
      <div className="container-page py-8 md:py-10">
        <Link to="/app" className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-4 w-4" /> Back
        </Link>

        {/* Goal summary */}
        <section className="mt-4 rounded-xl border border-border bg-card p-6 shadow-card md:p-8">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            <Sparkles className="h-3.5 w-3.5 text-primary" /> Goal
          </div>
          <h1 className="mt-2 text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            {data.goal?.user_input || workflow.goal}
          </h1>
          <div className="mt-5 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <Meta icon={<Layers className="h-4 w-4" />} label="Domain" value={data.goal?.domain || workflow.domain} />
            <Meta icon={<Activity className="h-4 w-4" />} label="Complexity" value={data.goal?.complexity || workflow.complexity} />
            <Meta icon={<Clock className="h-4 w-4" />} label="Est. time" value={data.estimated_time || workflow.estimated_time} />
            <Meta icon={<CheckCircle2 className="h-4 w-4" />} label="Steps" value={`${data.workflow?.length || 0}`} />
          </div>
        </section>

        {/* Deliverables */}
        {data.deliverables && data.deliverables.length > 0 && (
          <>
            <SectionHeader index="01" title="Deliverables" subtitle="What you'll have when you're done." />
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {data.deliverables.map((d) => (
                <div key={d.id} className="rounded-xl border border-border bg-card p-5 shadow-card">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-success" />
                    <h3 className="text-sm font-semibold text-foreground">{d.title}</h3>
                  </div>
                  <p className="mt-2 text-sm text-muted-foreground">{d.description}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Tools */}
        {data.recommended_tools && data.recommended_tools.length > 0 && (
          <>
            <SectionHeader index="02" title="Recommended Tools" subtitle="The stack we'd pick for this job." />
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {data.recommended_tools.map((t) => (
                <div key={t.name} className="rounded-xl border border-border bg-card p-5 shadow-card">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-sm font-semibold text-foreground">{t.name}</h3>
                    <span className="rounded-full bg-secondary px-2 py-0.5 text-xs text-muted-foreground">{t.category}</span>
                  </div>
                  <p className="mt-3 text-sm text-muted-foreground">{t.reason}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Workflow Steps */}
        {data.workflow && data.workflow.length > 0 && (
          <>
            <SectionHeader index="03" title="Workflow" subtitle="Step-by-step actions, prompts, and expected results." />
            <div className="space-y-3">
              {data.workflow.map((step) => (
                <WorkflowAccordion key={step.step_number} step={step} />
              ))}
            </div>
          </>
        )}

        {/* Alternatives */}
        {alternatives.length > 0 && (
          <>
            <SectionHeader index="04" title="Alternative Approaches" subtitle="Different paths to the same outcome." />
            <div className="grid gap-4 sm:grid-cols-2">
              {alternatives.map((a) => (
                <AlternativeCard key={a.type} alt={a} />
              ))}
            </div>
          </>
        )}

        {/* Knowledge Areas */}
        {knowledgeGroups.some((g) => g.items.length > 0) && (
          <>
            <SectionHeader index="05" title="Knowledge Areas" subtitle="What to learn — ranked by importance." />
            <div className="space-y-5 pb-12">
              {knowledgeGroups.map(({ level, label, items }) => {
                if (!items.length) return null;
                return (
                  <div key={level}>
                    <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      {label}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {items.map((k) => (
                        <span
                          key={k}
                          className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-medium ${
                            level === "high"
                              ? "border-primary/30 bg-primary/10 text-primary"
                              : level === "medium"
                              ? "border-accent/30 bg-accent/10 text-accent"
                              : "border-border bg-secondary text-muted-foreground"
                          }`}
                        >
                          {k}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}

// ---------------------------------------------------------------------------
// Sub-components (preserved from original)
// ---------------------------------------------------------------------------

function Meta({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="rounded-lg border border-border bg-background p-3">
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground">{icon}<span>{label}</span></div>
      <p className="mt-1 text-sm font-semibold text-foreground">{value}</p>
    </div>
  );
}

function SectionHeader({ index, title, subtitle }: { index: string; title: string; subtitle: string }) {
  return (
    <div className="mt-12 mb-5 flex items-end justify-between gap-4">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-primary">{index}</p>
        <h2 className="mt-1 text-xl font-bold tracking-tight text-foreground sm:text-2xl">{title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
      </div>
    </div>
  );
}

interface WorkflowStepData {
  step_number: number;
  title: string;
  tool: string;
  why: string;
  what_to_do: string;
  prompt: string;
  expected_result: string;
}

function WorkflowAccordion({ step }: { step: WorkflowStepData }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="overflow-hidden rounded-xl border border-border bg-card shadow-card">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center gap-4 px-5 py-4 text-left transition-colors hover:bg-secondary/50"
      >
        <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-primary/10 text-sm font-semibold text-primary">
          {step.step_number}
        </span>
        <span className="flex-1 text-sm font-semibold text-foreground">{step.title}</span>
        <ChevronDown className={`h-4 w-4 text-muted-foreground transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="grid gap-5 border-t border-border bg-background p-5 sm:grid-cols-2">
          <DetailBlock label="Tool" value={step.tool} />
          <DetailBlock label="Why this tool" value={step.why} />
          <DetailBlock label="What to do" value={step.what_to_do} className="sm:col-span-2" />
          {step.prompt && <PromptBlock label="AI Prompt" value={step.prompt} className="sm:col-span-2" />}
          <DetailBlock label="Expected result" value={step.expected_result} className="sm:col-span-2" />
        </div>
      )}
    </div>
  );
}

function DetailBlock({ label, value, className = "" }: { label: string; value: string; className?: string }) {
  return (
    <div className={className}>
      <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</p>
      <p className="mt-1 text-sm text-foreground">{value}</p>
    </div>
  );
}

function PromptBlock({ label, value, className = "" }: { label: string; value: string; className?: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className={className}>
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</p>
        <button
          onClick={() => {
            navigator.clipboard.writeText(value);
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
          }}
          className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground"
        >
          <Copy className="h-3 w-3" /> {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="mt-1 overflow-x-auto rounded-md border border-border bg-secondary/60 p-3 font-mono text-xs leading-relaxed text-foreground whitespace-pre-wrap">
        {value}
      </pre>
    </div>
  );
}

const altMeta: Record<AlternativeType, { icon: React.ComponentType<{ className?: string }>; color: string }> = {
  "Fastest": { icon: Zap, color: "text-warning" },
  "Cheapest": { icon: DollarSign, color: "text-success" },
  "Highest Quality": { icon: Award, color: "text-primary" },
  "Beginner Friendly": { icon: GraduationCap, color: "text-accent" },
};

function AlternativeCard({ alt }: { alt: AlternativeDisplay }) {
  const [open, setOpen] = useState(false);
  const meta = altMeta[alt.type];
  const Icon = meta.icon;
  return (
    <div className="rounded-xl border border-border bg-card p-5 shadow-card">
      <div className="flex items-center gap-2">
        <Icon className={`h-4 w-4 ${meta.color}`} />
        <h3 className="text-sm font-semibold text-foreground">{alt.type}</h3>
      </div>
      <p className="mt-2 text-sm text-muted-foreground">{alt.summary}</p>
      {open && alt.tools && alt.tools.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5 border-t border-border pt-3">
          {alt.tools.map((tool) => (
            <span key={tool} className="rounded-full bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
              {tool}
            </span>
          ))}
        </div>
      )}
      <button
        onClick={() => setOpen((v) => !v)}
        className="mt-3 text-xs font-semibold text-primary hover:underline"
      >
        {open ? "Show less" : "Show tools"}
      </button>
    </div>
  );
}
