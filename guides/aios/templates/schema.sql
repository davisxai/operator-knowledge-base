-- AIOS core schema. Run once in the Supabase SQL editor (or psql) on a fresh project.
-- The production version is managed by Drizzle; this is the same shape as plain SQL.


CREATE TABLE accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text NOT NULL UNIQUE,
  display_name text,
  account_key text NOT NULL UNIQUE,          -- e.g. 'primary' | 'internal' | 'automation'
  last_history_id text,                      -- Gmail incremental sync cursor
  watch_expiration timestamptz,              -- column exists; polling is used, not push watch
  status text DEFAULT 'active',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE email_threads (
  id text PRIMARY KEY,                       -- '<accountKey>:<gmailThreadId>'
  account_id uuid REFERENCES accounts(id),
  gmail_thread_id text NOT NULL,
  subject text,
  snippet text,
  participants jsonb,
  last_message_at timestamptz,
  message_count integer DEFAULT 0,
  is_unread boolean DEFAULT false,
  labels jsonb,
  updated_at timestamptz DEFAULT now()
);
CREATE INDEX email_threads_last_message_at_idx ON email_threads (last_message_at DESC);
CREATE INDEX email_threads_account_unread_idx ON email_threads (account_id, is_unread);

CREATE TABLE emails (
  id text PRIMARY KEY,                       -- '<accountKey>:<gmailMessageId>'
  account_id uuid REFERENCES accounts(id),
  thread_id text REFERENCES email_threads(id),
  gmail_message_id text NOT NULL,
  from_addr text,
  to_addrs jsonb,
  subject text,
  snippet text,
  body_text text,
  body_html text,
  internal_date timestamptz,
  labels jsonb,
  synced_at timestamptz DEFAULT now()
);
CREATE INDEX emails_account_internal_date_idx ON emails (account_id, internal_date DESC);

-- Triage result, one row per email. There is no separate triage-notes table:
-- the per-email human note is email_triage.user_note, and the standing
-- (global) triage guidance lives in sync_state under key 'triage_notes'.
CREATE TABLE email_triage (
  email_id text PRIMARY KEY REFERENCES emails(id),
  category text NOT NULL,                    -- action_needed | reply_needed | client | fyi | infra | newsletter | spamish
  priority integer NOT NULL,                 -- 1..5
  confidence numeric(3,2),
  is_automated boolean DEFAULT false,
  from_known_contact boolean DEFAULT false,
  contact_name text,
  notified boolean DEFAULT false,
  summary text,
  suggested_action text,
  corrected_category text,                   -- set when the human overrides / re-triages
  user_note text,                            -- per-email human note, fed back on re-triage
  model text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text,
  channel text DEFAULT 'chat',
  agent_session_id text,                     -- Claude Agent SDK session id, used for resume
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id uuid NOT NULL REFERENCES conversations(id),
  role text NOT NULL,
  content text NOT NULL DEFAULT '',
  content_blocks jsonb,
  created_at timestamptz DEFAULT now()
);
CREATE INDEX messages_conversation_created_idx ON messages (conversation_id, created_at);

CREATE TABLE agent_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id uuid REFERENCES conversations(id),
  trigger text NOT NULL,                     -- 'chat' | 'dream' | ...
  status text NOT NULL DEFAULT 'running',    -- running | completed | error
  summary text,
  tool_calls jsonb,
  tokens_in integer,
  tokens_out integer,
  cost_usd numeric(10,4),
  started_at timestamptz DEFAULT now(),
  finished_at timestamptz
);

CREATE TABLE daily_briefs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brief_date date NOT NULL UNIQUE,
  markdown text NOT NULL,
  stats jsonb,                               -- {actionItems,pendingActions,alerts,pipeline,tokens,costUsd}
  created_at timestamptz DEFAULT now()
);

CREATE TABLE notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL,                        -- triage | brief | dream | worker_alert | ...
  title text NOT NULL,
  body text,
  href text,
  dedupe_key text,                           -- collapses repeat pings, e.g. 'triage:<sender>' within 6h
  read_at timestamptz,
  created_at timestamptz DEFAULT now()
);

-- The dashboard <-> worker queue.
-- status lifecycle: proposed -> pending -> processing -> done | failed ; proposed -> denied
CREATE TABLE actions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL,                        -- mark_read | archive | trash | star | create_draft | retriage | sync
  payload jsonb NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  result jsonb,
  created_at timestamptz DEFAULT now(),
  processed_at timestamptz
);
CREATE INDEX actions_status_created_idx ON actions (status, created_at);

-- Key/value store. Keys seen in code: settings, triage_notes, worker_heartbeat,
-- last_history_id:<accountKey>, dream_state, dream_lock.
CREATE TABLE sync_state (
  key text PRIMARY KEY,
  value jsonb NOT NULL,
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE heartbeats (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  loop text NOT NULL,
  at timestamptz NOT NULL DEFAULT now(),
  ok boolean NOT NULL,
  detail text
);
CREATE INDEX heartbeats_loop_at_idx ON heartbeats (loop, at DESC);

-- People and companies projected from the vault so the worker (remote) can read them.
CREATE TABLE vault_entities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL,
  slug text NOT NULL,
  name text NOT NULL,
  aliases jsonb,
  relationship text,
  tier text,
  org text,
  domains jsonb,
  emails jsonb,
  note text,
  status text,
  source_path text,
  raw jsonb,
  synced_at timestamptz DEFAULT now()
);
CREATE UNIQUE INDEX vault_entities_kind_slug_idx ON vault_entities (kind, slug);
CREATE INDEX vault_entities_tier_idx ON vault_entities (tier);

-- Lead list (feeds the Atlas map).
CREATE TABLE leads (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  business text NOT NULL,
  contact_name text,
  title text,
  email text,
  phone text,
  website text,
  city text,
  state text,
  segment text,
  contact_type text,                         -- email | form | phone
  qualifier text,
  hook text,
  source text,
  source_url text,
  status text NOT NULL DEFAULT 'new',        -- new|queued|contacted|replied|booked|won|lost|bounced|dnc
  tags jsonb,
  notes text,
  lat double precision,
  lng double precision,
  last_contacted_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
CREATE UNIQUE INDEX leads_email_idx ON leads (email);
CREATE INDEX leads_segment_status_idx ON leads (segment, status);
CREATE INDEX leads_created_at_idx ON leads (created_at DESC);

-- US Census Gazetteer city centroids, joined in SQL to geocode leads.
CREATE TABLE city_centroids (
  state text NOT NULL,
  city text NOT NULL,                        -- normalized: lowercase, punctuation stripped
  lat double precision NOT NULL,
  lng double precision NOT NULL,
  PRIMARY KEY (state, city)
);

-- Calendar events shown on the Mission Control schedule card.
CREATE TABLE events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  kind text NOT NULL DEFAULT 'meeting',      -- meeting | deadline | reminder
  starts_at timestamptz NOT NULL,
  ends_at timestamptz,
  location text,
  notes text,
  source_ref text,
  created_at timestamptz DEFAULT now()
);
CREATE INDEX events_starts_at_idx ON events (starts_at);
