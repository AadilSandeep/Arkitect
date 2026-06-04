/**
 * Supabase client initialization.
 *
 * Uses environment variables for the Supabase URL and anon key.
 * The anon key is safe to expose in client-side code — it's
 * restricted by Row Level Security (RLS) policies.
 */

import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL ?? "";
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY ?? "";

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn(
    "[Supabase] VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY is not set. " +
      "Auth features will not work."
  );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
