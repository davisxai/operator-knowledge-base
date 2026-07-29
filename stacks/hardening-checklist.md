# Hardening a Box You Own

The security posture for the stack in [self-hosted-stack.md](self-hosted-stack.md), in the order I actually apply it.

Nothing here is theoretical. Every item is either something I run or something I learned by getting it wrong.

## The one rule everything else supports

**The reverse proxy and the SSH daemon are the entire public attack surface.**

Applications, databases, caches, admin panels, metrics endpoints. All of them bind to `127.0.0.1` and are reachable only through the proxy or not at all. Database and internal service ports never get opened in either firewall.

If you do one thing from this file, do that one. It is worth more than every tool below.

## 1. Two firewall layers, both default-deny

A provider-level network firewall sits in front of the machine. The host firewall runs on it. Both must allow a port for it to be reachable.

- Only the web ports and the SSH port are open. Nothing else, ever.
- Rules that exist in only one layer do not work. That sounds obvious and it is the single most common wasted debugging hour on this setup.
- **The provider firewall usually requires an explicit sync call after a rule change.** Editing the rule is not applying the rule. Check your provider's behavior before you assume a change took effect.

Enumerate and delete stale firewall objects left over from old experiments. You want exactly one active rule set, not four, three of which you cannot remember writing.

## 2. SSH

**Key-only authentication.** Password auth off, no exceptions. The authoritative key list lives on the machine. Keep the provider's key registry in sync anyway, because it is what matters during a VM rebuild.

**Move the daemon off port 22.** Not because obscurity is security, but because the volume of automated noise on 22 is genuinely large and some providers now block it at the network level.

> [!WARNING]
> On a modern Ubuntu release, SSH is socket-activated. You change the port by overriding the socket unit, not by editing `sshd_config`. And the override must list both the IPv4 and IPv6 bindings explicitly, because a bare port number binds IPv6 only. Get this wrong and you lock yourself out of a machine that looks perfectly healthy from the provider panel.

**Run a hardening script rather than hand-editing.** Mine enforces an explicit user allowlist, a low maximum authentication attempt count, and a short login grace time. Critically, it validates the config syntax before restarting and refuses to restart on a syntax error. An SSH config that fails to parse after a restart is how one-way doors happen.

**fail2ban, tuned to observed traffic.** Three-strike threshold, ten minute window, day-long bans, with your own networks in the ignore list. Verify the ban action is compatible with your host firewall, because a mismatched action silently bans nothing.

**Profile the attempts before setting the policy.** A small script that reads the journal and reports attempts per hour, top source networks, and top targeted usernames tells you what your actual threat traffic looks like. Tune against that, not against a blog post.

## 3. Container flags

Every container runs with the full set. There is no "just this one for now."

```
--read-only                              root filesystem is immutable
--tmpfs /tmp                             writable scratch, gone on restart
--tmpfs /app/.next/cache                 framework cache, same deal
--cap-drop ALL                           drop every Linux capability
--cap-add NET_BIND_SERVICE               add back only what is needed
--security-opt no-new-privileges:true    no privilege escalation via setuid
--memory 512m                            hard ceiling
--cpus 1.0                               hard ceiling
--pids-limit 256                         hard ceiling
```

Plus, in the image itself: a dedicated non-root system user with a fixed numeric uid and gid, no build toolchain in the runtime stage, and a declared `HEALTHCHECK`.

The resource ceilings are as much an availability control as a security one. An unbounded container can take down every other service on the box by winning a memory fight.

**Log rotation is part of hardening.** A JSON log driver with size-capped rotating files means verbose logging cannot fill the disk. A full disk is an outage, and "the log file grew" is an unglamorous way to have one.

## 4. Delete rather than maintain

The most effective hardening pass I have run was not installing anything. It was removing things.

Executed removals from one audit:

- A retired TLS/SSH port multiplexer, masked so it stops reporting as failed
- An unused mesh VPN client, its package, and its state
- A never-started ingress container and its image
- Orphaned data volumes, each backed up to a tarball via a throwaway container before deletion
- An abandoned agent runtime with its daemon, global package installs, project directories, and open loopback ports
- Assorted stray installer scripts and stale config backups

Container count went from eleven to three. Roughly 24 GB of disk came back.

> [!TIP]
> Write a removal runbook for each service instead of just deleting it. The runbook records what it was, why it went, and how to roll back. Six months later that document is the difference between "deliberate" and "what happened to this?"

## 5. Package policy

**Mark critical packages as manually installed.** Runtime, container engine, proxy, certificate client. This stops automatic dependency removal from stripping them.

I learned this when an `autoremove` pass took out the Node binary on a live box.

- Routine security upgrades run unattended. Leave that on.
- Distribution upgrades and `autoremove` require reading the package list first. Every time.
- Never run dependency autoremoval casually. It is in my written "do not do this" list for a reason.

## 6. Secrets

- Production environment files live on the machine, outside the image, mode-restricted to the owning user.
- They are loaded at container start or read directly by whatever job needs them.
- They are excluded from the build context via `.dockerignore` and from version control via `.gitignore`.
- **Never commit an env file.** Not a "sanitized" one, not a test one with real-looking values. Git history is forever and a committed key is a rotated key.
- Rotation is a documented file edit plus a test run. Write down which services need a restart after rotation and which do not.

## 7. Application-layer hardening

Host hardening does not help if the app hands out admin. These are enforced in code, not on the box.

**Content Security Policy with a per-request nonce.** Generate a fresh nonce in middleware, set it on the response header, and inject it into the forwarded request headers so server components downstream read the same value. Use `strict-dynamic`.

> [!NOTE]
> A real-world CSP of this kind usually keeps `'unsafe-inline'` in `script-src` alongside the nonce. That is the documented backward-compatibility idiom: browsers that support `strict-dynamic` ignore `unsafe-inline`, older ones fall back. It is not a pure nonce-only policy, and anyone telling you theirs is should check the actual header.

**Exclude non-HTML responses from middleware.** Dynamically generated OG images, sitemaps, `robots.txt`, icons, and static assets do not need a nonce, and wrapping a generated PNG or XML in a middleware response can corrupt it. This is a real bug, not boilerplate.

**Host allowlist that accounts for proxies.** Gather candidate hostnames from `x-forwarded-host`, `x-original-host`, `x-forwarded-server`, the RFC 7239 `Forwarded` header, the `Host` header, and the parsed URL. Normalize all of them: strip IPv6 brackets, strip the port, strip the trailing dot, lowercase. Then match. Checking only `Host` behind a proxy checks nothing.

**CSRF check on mutations.** Compare the Origin host against the request host on POST, PUT, DELETE, and PATCH.

**Correlation id on every response.** A UUID per request, returned in a header and written to logs. Costs nothing, and it is the difference between "a user reported an error" and "here is the exact request."

**Rate limits keyed per identity, not just per IP.** If automated clients hit your API, key the limiter on the client identity so one runaway consumer cannot eat the whole budget. Tier the limits by endpoint class: heartbeats and polls high, reads moderate, mutations lower, expensive operations lowest, login always on. Build it behind a factory so the in-memory backend can be swapped for Redis when you outgrow one node.

**Scoped API keys instead of one global admin key.** A single global key that grants full admin means every client holding it can do everything, including rotating the key. Replace it with per-client keys carrying an explicit scope list and an expiry, revocable individually. Emit a security event every time the global key is used, and drive that number to zero.

**Deny access and record the denial.** When a cross-tenant or cross-workspace access is refused, write an audit row: actor, actor id, target type, target id, route, IP, user agent. Cheap to add, and it turns a 403 from a rejection into an intrusion signal.

**Retention as per-data-class settings.** Audit records should outlive debug logs by an order of magnitude. Make each class its own configurable window rather than one global retention number.

## 8. Repeatable audit tooling

Four scripts, in the operations repo, that produce the machine's state on demand:

1. General health and security audit
2. Full structural map of what is installed and listening
3. Brute force analysis from the auth journal
4. The SSH hardening script itself

Commit their output as **dated inventory snapshots that are regenerated, never hand-edited.** That is the whole trick. Hand-edited state docs are fiction within a month. Regenerated ones make drift between sessions visible at a glance.

Split your documentation by volatility:

- **Stable facts** in one file
- **Dated state snapshots** that are regenerated
- **Procedures** in runbooks, read before touching production
- **An explicit "what not to do" list** carrying the scars

## The expensive lesson

Public listeners on this box were once multiplexed, so SSH and HTTPS could share a single port, with the proxy listening on a private internal port behind the multiplexer. Clever. It worked.

The multiplexer died during a routine restart. The proxy kept listening on the now-orphaned internal address. Four subdomains went dark for two weeks.

Nobody noticed immediately, because the apex domain had already been migrated to the real public listener. The homepage stayed up the entire time while search indexing quietly collapsed underneath it.

The fix was not to restore the multiplexer. It was to point every virtual host at the real public listener and retire the multiplexer permanently.

Two conclusions, both written into the operations repo:

> [!WARNING]
> **Prefer a boring direct binding over a clever shared one.** Cleverness in the network path buys you very little and costs you a failure mode nobody on the team understands.
>
> **"The main site still works" is not evidence that the proxy layer is healthy.** Check every hostname, or check none of them and admit you are not checking.

## The checklist

**Network**
- [ ] Provider firewall default-deny, only web ports and SSH open
- [ ] Host firewall default-deny, same rules
- [ ] Firewall changes synced and verified, not just saved
- [ ] Stale firewall objects enumerated and deleted

**SSH**
- [ ] Key-only auth, passwords disabled
- [ ] Daemon on a non-default port via the socket override, both IPv4 and IPv6 listed
- [ ] User allowlist, low max auth tries, short grace time
- [ ] Config syntax validated before every restart
- [ ] fail2ban running with a ban action verified against your firewall
- [ ] Provider browser console tested as your lockout recovery path

**Containers**
- [ ] Read-only root, tmpfs for writable paths
- [ ] Non-root user with a fixed uid and gid
- [ ] All capabilities dropped, only required ones added back
- [ ] `no-new-privileges` set
- [ ] Memory, CPU, and PID ceilings set
- [ ] Log driver size-capped and rotating
- [ ] Every port bound to loopback, never `0.0.0.0`

**Surface**
- [ ] Every unused service removed, with a runbook recording the removal
- [ ] Critical packages marked manually installed
- [ ] Unattended security upgrades on, `autoremove` never casual

**Secrets**
- [ ] Env files outside the image, mode-restricted
- [ ] Excluded from build context and version control
- [ ] Rotation procedure written down

**Application**
- [ ] CSP with per-request nonce, non-HTML responses excluded from middleware
- [ ] Host allowlist that reads proxy headers
- [ ] CSRF check on mutating methods
- [ ] Correlation id on every response
- [ ] Rate limits keyed per identity, tiered by endpoint class
- [ ] Scoped, expiring API keys instead of one global admin key
- [ ] Denials written to an audit trail
- [ ] Retention windows set per data class

**Operations**
- [ ] Audit scripts committed and output regenerated, not hand-edited
- [ ] Runbooks with explicit rollback blocks
- [ ] A written "do not do this" list
- [ ] Snapshot taken before every risky session

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
