import { createFileRoute, Link } from "@tanstack/react-router";
import { MarketingNav, Footer } from "@/components/layout";
import {
  Sparkles,
  Wrench,
  GitBranch,
  MessageSquareCode,
  Shuffle,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Arkitect — Architect Your Path to Execution" },
      { name: "description", content: "AI-powered workflow planning with deliverables, tools, workflows, and AI prompts. Turn any goal into a clear execution plan." },
      { property: "og:title", content: "Arkitect — Architect Your Path to Execution" },
      { property: "og:description", content: "Turn any goal into an execution plan with AI-generated deliverables, tools, and workflows." },
    ],
  }),
  component: Landing,
});

const features = [
  { icon: Sparkles, title: "Deliverables Detection", desc: "Automatically identifies the concrete outputs your goal requires." },
  { icon: Wrench, title: "Tool Recommendations", desc: "Curated tools matched to your domain and complexity." },
  { icon: GitBranch, title: "Workflow Generation", desc: "Step-by-step plans with clear actions and expected results." },
  { icon: MessageSquareCode, title: "Prompt Generation", desc: "Ready-to-use AI prompts for each step of your workflow." },
  { icon: Shuffle, title: "Alternative Approaches", desc: "Fastest, cheapest, highest quality, or beginner friendly paths." },
  { icon: GraduationCap, title: "Knowledge Areas", desc: "Know exactly what to learn — ranked by importance." },
];

function Landing() {
  return (
    <div className="min-h-screen bg-background">
      <MarketingNav />

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-x-0 -top-40 -z-10 h-[600px] opacity-60 blur-3xl"
          style={{ background: "radial-gradient(60% 50% at 50% 0%, oklch(0.85 0.13 277 / 0.35), transparent 70%)" }}
        />
        <div className="container-page py-20 md:py-28">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-elegant">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              AI workflow architect — not a chatbot
            </div>
            <h1 className="mt-6 text-4xl font-bold tracking-tight text-foreground sm:text-5xl md:text-6xl">
              Turn Any Goal Into an{" "}
              <span className="text-gradient">Execution Plan</span>
            </h1>
            <p className="mx-auto mt-5 max-w-2xl text-lg text-muted-foreground">
              AI-powered workflow planning with deliverables, tools, workflows, and AI prompts.
              Stop staring at a blank page — start executing.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link
                to="/app"
                className="inline-flex h-11 items-center gap-2 rounded-md px-6 text-sm font-semibold text-primary-foreground shadow-pop transition-opacity hover:opacity-90"
                style={{ background: "var(--gradient-primary)" }}
              >
                Generate Workflow <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                to="/workflow/$id"
                params={{ id: "launch-saas-startup" }}
                className="inline-flex h-11 items-center rounded-md border border-border bg-card px-6 text-sm font-semibold text-foreground transition-colors hover:bg-secondary"
              >
                See Example
              </Link>
            </div>
            <p className="mt-4 text-xs text-muted-foreground">No credit card required · Free to try</p>
          </div>

          {/* Hero illustration mock */}
          <div className="mx-auto mt-16 max-w-5xl">
            <div className="rounded-xl border border-border bg-card shadow-pop">
              <div className="flex items-center gap-2 border-b border-border px-4 py-3">
                <span className="h-2.5 w-2.5 rounded-full bg-muted" />
                <span className="h-2.5 w-2.5 rounded-full bg-muted" />
                <span className="h-2.5 w-2.5 rounded-full bg-muted" />
                <div className="ml-4 flex-1 rounded-md bg-secondary px-3 py-1 text-xs text-muted-foreground">
                  arkitect.app / workflow / launch-a-saas-startup
                </div>
              </div>
              <div className="grid grid-cols-12 gap-0">
                <div className="col-span-12 border-b border-border p-6 md:col-span-3 md:border-b-0 md:border-r">
                  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Goal</p>
                  <p className="mt-1 text-sm font-semibold text-foreground">Launch a SaaS Startup</p>
                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex justify-between"><span className="text-muted-foreground">Domain</span><span className="text-foreground">Product</span></div>
                    <div className="flex justify-between"><span className="text-muted-foreground">Complexity</span><span className="text-foreground">High</span></div>
                    <div className="flex justify-between"><span className="text-muted-foreground">Time</span><span className="text-foreground">8–12 wks</span></div>
                  </div>
                </div>
                <div className="col-span-12 p-6 md:col-span-9">
                  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Deliverables</p>
                  <div className="mt-3 grid grid-cols-2 gap-3 md:grid-cols-3">
                    {["Problem Statement","Landing Page","MVP","Pricing","GTM Plan","Analytics"].map((d) => (
                      <div key={d} className="rounded-lg border border-border bg-background p-3">
                        <div className="flex items-center gap-2">
                          <CheckCircle2 className="h-3.5 w-3.5 text-success" />
                          <span className="text-xs font-medium text-foreground">{d}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="border-t border-border bg-secondary/30 py-20">
        <div className="container-page">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-sm font-semibold uppercase tracking-wider text-primary">Capabilities</p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Every part of a plan, generated for you
            </h2>
            <p className="mt-4 text-muted-foreground">
              Arkitect breaks your goal into the parts that actually matter — and tells you exactly how to ship each one.
            </p>
          </div>
          <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {features.map((f) => (
              <div key={f.title} className="group rounded-xl border border-border bg-card p-6 shadow-elegant transition-shadow hover:shadow-pop">
                <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <f.icon className="h-5 w-5" />
                </div>
                <h3 className="mt-4 text-base font-semibold text-foreground">{f.title}</h3>
                <p className="mt-1.5 text-sm text-muted-foreground">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Example */}
      <section id="example" className="py-20">
        <div className="container-page">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-sm font-semibold uppercase tracking-wider text-primary">Example</p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Goal: Launch a SaaS Startup
            </h2>
            <p className="mt-4 text-muted-foreground">A real workflow generated by Arkitect.</p>
          </div>

          <div className="mx-auto mt-12 grid max-w-5xl gap-6 lg:grid-cols-2">
            <div className="rounded-xl border border-border bg-card p-6 shadow-card">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Deliverables</p>
              <ul className="mt-4 space-y-3">
                {["Validated Problem Statement","Landing Page & Waitlist","MVP Product","Pricing & Packaging","Go-to-Market Plan"].map((d) => (
                  <li key={d} className="flex items-start gap-3">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                    <span className="text-sm text-foreground">{d}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-xl border border-border bg-card p-6 shadow-card">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Recommended Tools</p>
              <div className="mt-4 grid grid-cols-2 gap-3">
                {[
                  { name: "Linear", cat: "PM" },
                  { name: "Figma", cat: "Design" },
                  { name: "Vercel", cat: "Hosting" },
                  { name: "Supabase", cat: "Backend" },
                  { name: "Stripe", cat: "Payments" },
                  { name: "PostHog", cat: "Analytics" },
                ].map((t) => (
                  <div key={t.name} className="rounded-lg border border-border bg-background p-3">
                    <p className="text-sm font-semibold text-foreground">{t.name}</p>
                    <p className="text-xs text-muted-foreground">{t.cat}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mx-auto mt-6 max-w-5xl rounded-xl border border-border bg-card p-6 shadow-card">
            <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Workflow Preview</p>
            <ol className="mt-4 space-y-3">
              {[
                "Validate the problem with 10 customer interviews",
                "Design the landing page and capture a waitlist",
                "Scope and build the MVP",
                "Instrument analytics and launch",
              ].map((step, i) => (
                <li key={step} className="flex items-start gap-3">
                  <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-primary/10 text-xs font-semibold text-primary">{i + 1}</span>
                  <span className="text-sm text-foreground">{step}</span>
                </li>
              ))}
            </ol>
            <Link
              to="/workflow/$id"
              params={{ id: "launch-saas-startup" }}
              className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-primary hover:underline"
            >
              View full workflow <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="border-t border-border py-20">
        <div className="container-page">
          <div className="mx-auto max-w-3xl rounded-2xl border border-border p-10 text-center shadow-pop"
            style={{ background: "var(--gradient-primary)" }}
          >
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Start architecting your next move
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-white/85">
              Type your goal. Get a complete plan in seconds.
            </p>
            <Link
              to="/app"
              className="mt-6 inline-flex h-11 items-center gap-2 rounded-md bg-white px-6 text-sm font-semibold text-primary shadow-elegant transition-transform hover:scale-[1.02]"
            >
              Generate your first workflow <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
