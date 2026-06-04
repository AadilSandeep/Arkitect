import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AuthLayout, Field } from "./login";
import { useAuth } from "@/lib/auth-context";

export const Route = createFileRoute("/signup")({
  head: () => ({ meta: [{ title: "Sign up — Arkitect" }] }),
  component: Signup,
});

function Signup() {
  const navigate = useNavigate();
  const { signUp } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  return (
    <AuthLayout title="Create your account" subtitle="Start architecting plans in under a minute.">
      {success ? (
        <div className="rounded-md border border-success/30 bg-success/10 px-4 py-3 text-sm text-success">
          <p className="font-semibold">Check your email!</p>
          <p className="mt-1 text-success/80">
            We sent a confirmation link to your email address. Click it to activate your account, then{" "}
            <Link to="/login" className="font-semibold underline">log in</Link>.
          </p>
        </div>
      ) : (
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            setLoading(true);
            setError(null);

            const formData = new FormData(e.currentTarget);
            const fullName = formData.get("name") as string;
            const email = formData.get("email") as string;
            const password = formData.get("password") as string;

            if (password.length < 8) {
              setError("Password must be at least 8 characters.");
              setLoading(false);
              return;
            }

            const result = await signUp(email, password, fullName);

            if (result.error) {
              setError(result.error);
              setLoading(false);
            } else {
              // Supabase may require email confirmation.
              // If auto-confirm is on, redirect immediately.
              // Otherwise show the success message.
              setSuccess(true);
              setLoading(false);
            }
          }}
          className="space-y-4"
        >
          {error && (
            <div className="rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">
              {error}
            </div>
          )}
          <Field label="Full name" type="text" name="name" placeholder="Ada Lovelace" required />
          <Field label="Email" type="email" name="email" placeholder="you@company.com" required />
          <Field label="Password" type="password" name="password" placeholder="At least 8 characters" required />
          <button
            type="submit"
            disabled={loading}
            className="inline-flex h-10 w-full items-center justify-center rounded-md text-sm font-semibold text-primary-foreground shadow-pop transition-opacity hover:opacity-90 disabled:opacity-60"
            style={{ background: "var(--gradient-primary)" }}
          >
            {loading ? "Creating account…" : "Create account"}
          </button>
          <p className="text-center text-xs text-muted-foreground">
            By signing up, you agree to our Terms and Privacy Policy.
          </p>
        </form>
      )}
      <p className="mt-6 text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link to="/login" className="font-semibold text-primary hover:underline">Log in</Link>
      </p>
    </AuthLayout>
  );
}
