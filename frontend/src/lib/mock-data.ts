export type Deliverable = { title: string; description: string };
export type Tool = { name: string; category: string; reason: string };
export type WorkflowStep = {
  number: number;
  title: string;
  tool: string;
  why: string;
  what: string;
  prompt: string;
  result: string;
};
export type Alternative = {
  type: "Fastest" | "Cheapest" | "Highest Quality" | "Beginner Friendly";
  summary: string;
  details: string;
};
export type KnowledgeArea = { name: string; importance: "high" | "medium" | "low" };

export type Workflow = {
  id: string;
  goal: string;
  domain: string;
  complexity: "Low" | "Medium" | "High";
  estimatedTime: string;
  createdAt: string;
  deliverables: Deliverable[];
  tools: Tool[];
  steps: WorkflowStep[];
  alternatives: Alternative[];
  knowledge: KnowledgeArea[];
};

export const mockWorkflows: Workflow[] = [
  {
    id: "launch-saas-startup",
    goal: "Launch a SaaS Startup",
    domain: "Product · Business",
    complexity: "High",
    estimatedTime: "8–12 weeks",
    createdAt: "2026-05-28",
    deliverables: [
      { title: "Validated Problem Statement", description: "A crisp articulation of the pain point and target customer backed by interviews." },
      { title: "Landing Page & Waitlist", description: "Conversion-optimized landing page with email capture and analytics." },
      { title: "MVP Product", description: "Shippable v1 covering the core job-to-be-done end-to-end." },
      { title: "Pricing & Packaging", description: "Tiered pricing model with positioning and competitive benchmarks." },
      { title: "Go-to-Market Plan", description: "30/60/90 launch plan across channels with measurable KPIs." },
      { title: "Analytics & Feedback Loop", description: "Instrumented funnel with retention, activation, and qualitative feedback." },
    ],
    tools: [
      { name: "Linear", category: "Project Management", reason: "Best-in-class issue tracking for small product teams shipping fast." },
      { name: "Figma", category: "Design", reason: "Collaborative design and prototyping for landing page and MVP screens." },
      { name: "Vercel", category: "Hosting", reason: "Zero-config deploy for the landing page and MVP frontend." },
      { name: "Supabase", category: "Backend", reason: "Auth, database, and storage in one—ideal for an early MVP." },
      { name: "Stripe", category: "Payments", reason: "Industry-standard billing with subscription primitives built-in." },
      { name: "PostHog", category: "Analytics", reason: "Product analytics, session replay, and feature flags in one stack." },
    ],
    steps: [
      {
        number: 1,
        title: "Validate the problem with 10 customer interviews",
        tool: "Notion + Zoom",
        why: "Structured interview notes let you spot patterns and shared language quickly.",
        what: "Recruit 10 target users. Run 30-min interviews focused on the problem, not the solution. Synthesize insights into a one-page brief.",
        prompt: "Act as a B2B research analyst. Given the following interview notes, extract the top 3 recurring pain points, the language customers used, and the workflows they currently rely on.",
        result: "A one-page validated problem statement with quotes and an opportunity score.",
      },
      {
        number: 2,
        title: "Design the landing page and capture a waitlist",
        tool: "Figma + Framer",
        why: "Visual fidelity before code keeps iteration cheap and conversion-focused.",
        what: "Draft hero, value props, social proof, and CTA. Publish to Framer with an email capture connected to a CRM.",
        prompt: "Generate 5 hero headline variations for a SaaS targeting <ICP> solving <pain>. Each headline must be under 9 words, benefit-driven, and avoid jargon.",
        result: "Live landing page collecting 50+ qualified signups in 2 weeks.",
      },
      {
        number: 3,
        title: "Scope and build the MVP",
        tool: "Linear + Cursor",
        why: "A tight scope shipped weekly beats a broad scope shipped never.",
        what: "Break the core flow into 6–10 issues. Build vertically (one full flow) before horizontally. Ship to staging weekly.",
        prompt: "You are a senior product manager. Given this PRD, output a prioritized issue list using MoSCoW and estimate complexity (XS–XL) for each.",
        result: "A shippable MVP covering the core job-to-be-done.",
      },
      {
        number: 4,
        title: "Instrument analytics and launch",
        tool: "PostHog + Stripe",
        why: "If you can't measure activation, you can't improve it.",
        what: "Define your North Star metric and 3 supporting funnels. Wire events. Launch on Product Hunt and to your waitlist.",
        prompt: "Given a SaaS in the <category> space, propose a North Star metric and 3 supporting funnel events with definitions.",
        result: "Live product with measurable activation and your first paying customers.",
      },
    ],
    alternatives: [
      { type: "Fastest", summary: "No-code MVP in 2 weeks using Framer + Airtable + Stripe.", details: "Skip custom code entirely. Use Framer for the marketing site, Airtable as your database, and Stripe Payment Links for billing. Trade flexibility for speed." },
      { type: "Cheapest", summary: "Solo founder stack under $50/mo.", details: "Vercel hobby, Supabase free tier, PostHog free tier, Stripe pay-as-you-go. No paid tools until you have revenue." },
      { type: "Highest Quality", summary: "Investor-grade launch with design partner program.", details: "Recruit 5 paying design partners before launch. Hire a fractional designer. Custom branding, in-depth onboarding, and a hand-built dashboard." },
      { type: "Beginner Friendly", summary: "Guided path with templates and weekly checkpoints.", details: "Use proven templates (Tailwind UI, Stripe starter). Weekly 1-hour reviews with a mentor. Avoid premature optimization." },
    ],
    knowledge: [
      { name: "Customer Discovery", importance: "high" },
      { name: "Positioning", importance: "high" },
      { name: "Product Analytics", importance: "high" },
      { name: "Pricing Strategy", importance: "medium" },
      { name: "Growth Loops", importance: "medium" },
      { name: "Content Marketing", importance: "medium" },
      { name: "SEO Basics", importance: "low" },
      { name: "Brand Design", importance: "low" },
    ],
  },
  {
    id: "publish-technical-book",
    goal: "Write and self-publish a technical book",
    domain: "Writing · Publishing",
    complexity: "Medium",
    estimatedTime: "16 weeks",
    createdAt: "2026-05-20",
    deliverables: [
      { title: "Detailed Outline", description: "Chapter-by-chapter outline with learning objectives." },
      { title: "First Draft", description: "Complete draft of ~50,000 words." },
      { title: "Edited Manuscript", description: "Professionally edited and proofread version." },
      { title: "Cover & Layout", description: "Cover design and interior typesetting." },
      { title: "Distribution Setup", description: "Configured KDP and Gumroad listings." },
    ],
    tools: [
      { name: "Scrivener", category: "Writing", reason: "Built for long-form structured writing." },
      { name: "Grammarly", category: "Editing", reason: "Catches style and grammar issues continuously." },
      { name: "Canva", category: "Design", reason: "Quick cover prototyping before hiring a designer." },
      { name: "KDP", category: "Distribution", reason: "Largest reach for self-published technical books." },
    ],
    steps: [
      { number: 1, title: "Define audience and outline", tool: "Notion", why: "Clarity upfront prevents rewrites.", what: "Define ICP, scope, and chapter outline with learning outcomes.", prompt: "Generate a chapter outline for a 50k-word technical book on <topic> for <audience>.", result: "Approved outline with 10–12 chapters." },
      { number: 2, title: "Write daily in 90-minute blocks", tool: "Scrivener", why: "Cadence beats inspiration.", what: "Aim for 1,000 words/day in focused blocks. Track in a streak log.", prompt: "Expand this bullet outline into a 1,200-word section in a clear, conversational tone with 2 examples.", result: "Complete first draft." },
    ],
    alternatives: [
      { type: "Fastest", summary: "Repurpose existing blog posts.", details: "Compile and rework existing content into book form in 6 weeks." },
      { type: "Cheapest", summary: "Self-edit, free tools only.", details: "Use Google Docs, free Canva, and KDP only. Zero tooling cost." },
      { type: "Highest Quality", summary: "Hire pro editor + designer.", details: "Invest $3–5k in editing and cover design." },
      { type: "Beginner Friendly", summary: "Use a guided course like Write of Passage.", details: "Cohort accountability and step-by-step framework." },
    ],
    knowledge: [
      { name: "Long-form Writing", importance: "high" },
      { name: "Audience Research", importance: "high" },
      { name: "Self-publishing", importance: "medium" },
      { name: "Cover Design", importance: "low" },
    ],
  },
  {
    id: "run-product-launch",
    goal: "Run a successful Product Hunt launch",
    domain: "Marketing · Growth",
    complexity: "Medium",
    estimatedTime: "4 weeks",
    createdAt: "2026-05-10",
    deliverables: [
      { title: "Launch Assets", description: "Gallery, GIFs, tagline, and first-comment copy." },
      { title: "Hunter & Supporter List", description: "Pre-aligned hunters and 200+ activated supporters." },
      { title: "Launch-day Playbook", description: "Hour-by-hour run-of-show." },
    ],
    tools: [
      { name: "Product Hunt", category: "Distribution", reason: "Primary launch platform." },
      { name: "Loom", category: "Video", reason: "Quick founder demo videos." },
      { name: "Typefully", category: "Social", reason: "Schedule Twitter/X threads." },
    ],
    steps: [
      { number: 1, title: "Pre-launch outreach", tool: "Email + DMs", why: "Day-1 momentum decides ranking.", what: "Build a list of 200 supporters and notify them 24h before.", prompt: "Draft a warm pre-launch DM (under 80 words) inviting a friend to support our PH launch.", result: "200 confirmed supporters." },
    ],
    alternatives: [
      { type: "Fastest", summary: "Stealth launch with no prep.", details: "Skip preparation, post and let it ride. Lower ranking but ships today." },
      { type: "Cheapest", summary: "Zero paid tools.", details: "Free tier of everything; rely on organic outreach." },
      { type: "Highest Quality", summary: "Hire a launch consultant.", details: "Work with a top hunter and proven launch agency." },
      { type: "Beginner Friendly", summary: "Use the official PH launch guide.", details: "Follow the templated checklist step-by-step." },
    ],
    knowledge: [
      { name: "Copywriting", importance: "high" },
      { name: "Community Building", importance: "high" },
      { name: "Video Production", importance: "medium" },
      { name: "Twitter/X Strategy", importance: "low" },
    ],
  },
];

export function getWorkflow(id: string): Workflow | undefined {
  return mockWorkflows.find((w) => w.id === id);
}
