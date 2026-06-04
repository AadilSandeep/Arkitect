import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { Logo } from "@/components/layout";
import { useState } from "react";
import { useAuth } from "@/lib/auth-context";

export const Route = createFileRoute("/login")({
  head: () => ({ meta: [{ title: "Log in — Arkitect" }] }),
  component: Login,
});

function Login() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <AuthLayout title="Welcome back" subtitle="Log in to continue planning your next goal.">
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          setLoading(true);
          setError(null);

          const formData = new FormData(e.currentTarget);
          const email = formData.get("email") as string;
          const password = formData.get("password") as string;

          const result = await signIn(email, password);

          if (result.error) {
            setError(result.error);
            setLoading(false);
          } else {
            navigate({ to: "/app" });
          }
        }}
        className="space-y-4"
      >
        {error && (
          <div className="rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
            {error}
          </div>
        )}
        <Field label="Email" type="email" name="email" placeholder="you@company.com" required />
        <Field label="Password" type="password" name="password" placeholder="••••••••" required
          extra={<a href="#" className="text-xs font-medium text-primary hover:underline">Forgot?</a>}
        />
        <button
          type="submit"
          disabled={loading}
          className="inline-flex h-10 w-full items-center justify-center rounded-md text-sm font-semibold text-primary-foreground shadow-pop transition-opacity hover:opacity-90 disabled:opacity-60"
          style={{ background: "var(--gradient-primary)" }}
        >
          {loading ? "Logging in…" : "Log in"}
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-muted-foreground">
        Don't have an account?{" "}
        <Link to="/signup" className="font-semibold text-primary hover:underline">Sign up</Link>
      </p>
    </AuthLayout>
  );
}

export function AuthLayout({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-secondary/30">
      <header className="border-b border-border bg-background">
        <div className="container-page flex h-16 items-center justify-between">
          <Logo />
          <Link to="/" className="text-sm text-muted-foreground hover:text-foreground">Back to site</Link>
        </div>
      </header>
      <main className="flex flex-1 items-center justify-center p-6">
        <div className="w-full max-w-md rounded-xl border border-border bg-card p-8 shadow-card">
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
          <p className="mt-1.5 text-sm text-muted-foreground">{subtitle}</p>
          <div className="mt-6">{children}</div>
        </div>
      </main>
    </div>
  );
}

export function Field({
  label, type, name, placeholder, required, extra,
}: { label: string; type: string; name: string; placeholder?: string; required?: boolean; extra?: React.ReactNode }) {
  return (
    <label className="block">
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-sm font-medium text-foreground">{label}</span>
        {extra}
      </div>
      <input
        type={type}
        name={name}
        placeholder={placeholder}
        required={required}
        className="block h-10 w-full rounded-md border border-input bg-background px-3 text-sm text-foreground placeholder:text-muted-foreground/70 focus:outline-none focus:ring-2 focus:ring-ring"
      />
    </label>
  );
}
