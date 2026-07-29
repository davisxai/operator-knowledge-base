# The Self-Hosted Stack

One long-lived Linux server runs everything. This file describes what is on it, how the pieces fit, and what it costs.

The deploy flow lives in [deploy-pattern.md](deploy-pattern.md). The security posture lives in [hardening-checklist.md](hardening-checklist.md). This file is the map.

## The substrate

A single-tenant KVM virtual machine from a fixed-price VPS host. Not a hyperscaler. Ubuntu LTS. Roughly workstation-class capacity: high single-digit vCPU, tens of gigabytes of RAM, hundreds of gigabytes of disk, one flat monthly fee.

Why this category and not a managed platform:

- **Predictable cost.** The bill is the same in a traffic spike as it is at 3am on a Tuesday.
- **Full root control.** Nothing is abstracted away at the moment you need to debug at the process level.
- **One machine is enough.** Every workload fits. There is no reason to distribute what one box handles.
- **No vendor abstraction to fight.** When something breaks you read the logs, not a status page.

The tradeoff you accept in exchange: you own patching, hardening, and uptime. That is the whole deal. Take it seriously or pick a managed platform.

### The control surface split

The provider gives you two ways in, and you should write down which one owns what.

- **The provider API and web panel own the infrastructure layer.** VM lifecycle, network firewall rules, DNS records, snapshots, backups, metrics, recovery mode, password reset.
- **The shell owns the service layer.** systemd, Docker, file edits, package installs, certificate issuance, proxy config.

Keep that boundary explicit in your notes. The failure mode is doing service work through a panel that then drifts from the machine, or trying to fix a network firewall from a shell that cannot see it.

> [!TIP]
> The provider's browser-based console is your guaranteed recovery path. It works with no key, no agent, and no network route to the SSH daemon. Make it step one of your written lockout procedure before you ever need it.

## Architecture

```
                            internet
                                |
                                v
                +-------------------------------+
                |  provider network firewall    |  default deny
                |  open: 80, 443, ssh port      |
                +-------------------------------+
                                |
                +-------------------------------+
                |  host firewall (ufw)          |  default deny
                +-------------------------------+
                                |
   ==============================================================
   ||                    one linux vm                          ||
   ||                                                          ||
   ||   nginx            <- the only public listener           ||
   ||     |  terminates TLS, one vhost per hostname            ||
   ||     |                                                    ||
   ||     +---> 127.0.0.1:3000   app container (next.js)       ||
   ||     +---> 127.0.0.1:5678   automation container (n8n)    ||
   ||     +---> 127.0.0.1:xxxx   any other internal service    ||
   ||                                                          ||
   ||   postgres container   <- loopback only, no host port    ||
   ||   redis container      <- loopback only, no host port    ||
   ||                                                          ||
   ||   sshd        (non-default port, key auth only)          ||
   ||   fail2ban    unattended-upgrades    cron                ||
   ==============================================================
```

Read the diagram as one rule: **every application, database, and cache binds to the loopback interface only.** Nothing but the proxy and the SSH daemon holds a listener reachable from outside the machine. Database ports and internal service ports are never opened in either firewall. Not once, not temporarily.

## What runs on the box

Steady state, after a deliberate consolidation pass:

- **Reverse proxy.** nginx holds the only public listeners, plain HTTP and HTTPS, and terminates TLS for every hostname.
- **Application containers.** The production Next.js site runs as a container. A Postgres container backs application data. A Redis container provides cache.
- **Process-manager workloads.** A small PM2 setup supervises long-running Node and Python processes that predate the container path. These are legacy and are being folded into containers.
- **Platform services.** systemd manages the SSH socket, Docker and containerd, fail2ban, cron, unattended security upgrades, and a small webhook listener that can trigger a deploy from a repository event.

### The consolidation story

The same box previously ran a self-hosted n8n instance, a local LLM runtime, and a full metrics stack (Prometheus, Grafana, node exporter, container advisor). Each was added for a reason. Each stopped earning its keep.

An audit pass removed them. Container count went from eleven to three. Roughly 24 GB of disk came back.

> [!WARNING]
> Unused services are open ports, confusing audits, and wasted disk. They are not free just because you already installed them. Delete rather than maintain, and write the removal down as a runbook so the next person knows it was deliberate.

n8n on this box is a good example of the honest version of this story. Self-hosting it is genuinely worth doing when you have workflows running daily. It was not worth a running container when the workflows had moved elsewhere. The pattern hosts it fine. Whether you should run it is a question about your workload, not about the stack.

## Docker layout

### The image

A four-stage Dockerfile on a slim Node base:

**base**
Pins the Node minor version. Enables corepack. Takes the package manager version from the `packageManager` field in `package.json`, never a floating `@latest` tag.

That last detail is not style. A major package manager release changed build-dependency handling and broke the build. Pinning through `packageManager` means the lockfile and the tooling move together.

**deps**
Copies only the manifest and the lockfile first, so the dependency layer caches independently of source changes. Installs frozen against the lockfile. If a native addon is in play, the compile toolchain is installed in this stage only, so it never reaches the runtime image.

**build**
Copies the cached modules plus source and runs the production build. Build-time public environment variables are declared as build args, because the framework inlines them at compile time. Getting this wrong produces an image that builds fine and ships the wrong config.

**runtime**
A fresh slim base with no build toolchain. Installs a minimal runtime set only: an HTTP client for health checking, CA certificates for outbound TLS. Creates a dedicated system group and user with fixed numeric ids. Copies in the framework's standalone output plus static and public assets. Writes a tiny inline health check script. Drops to the non-root user. Declares a container-level `HEALTHCHECK` with an interval, timeout, start period, and retry count.

Image metadata uses standard OCI labels for source, description, license, and a version passed as a build argument.

The build context gets trimmed by a `.dockerignore` that excludes node modules, version control, local data, prior build output, environment files, documentation, and CI config.

### The entrypoint

A short shell script that sources an environment file if one is mounted, then `exec`s the server. The `exec` matters: it makes the application PID 1 so it receives signals directly and shuts down cleanly.

### Compose: base plus overlay

Two files, composed as a base plus an overlay. Not two duplicated environment definitions that drift.

**Base compose** defines the service, the port mapping from a host loopback port to the container port, environment passthrough, an optional env file, a named volume for persistent data, and the security posture:

- read-only root filesystem
- tmpfs mounts for the temp directory and the framework cache directory
- all Linux capabilities dropped, with only the bind-privileged-port capability added back
- `no-new-privileges`
- hard ceilings on memory, CPU, and process count
- restart policy `unless-stopped`

**Hardened overlay** adds production-only concerns: a JSON log driver with size-capped rotating files so verbose logging cannot fill the disk, a strict hostname allowlist, secure and strict-samesite cookies, HSTS, and an internal-only bridge network.

> [!TIP]
> The deploy script applies the same posture through explicit `docker run` flags rather than compose. Whichever path you use, the running container ends up with the identical read-only filesystem, tmpfs mounts, dropped capabilities, `no-new-privileges`, and resource limits. If those two paths disagree, one of them is a security hole you did not know you had.

## Reverse proxy and TLS

nginx is the single public entry point. One virtual host per hostname, each proxying to a loopback port.

- The plain HTTP server block exists for exactly one purpose: a permanent redirect to HTTPS.
- A separate HTTPS block redirects the `www` form to the apex.
- TLS is restricted to the two current protocol versions, with a conservative cipher selection and server cipher preference.
- Certificates come from Let's Encrypt through certbot with automatic renewal.
- Proxy blocks set the upgrade and connection headers for WebSocket support, forward the real client address and original protocol, and use very long read and send timeouts so server-sent event streams are not cut mid-stream.
- Static asset paths get long-lived immutable cache headers at the proxy layer, not in the application.

**Adding a hostname expands the existing certificate rather than reissuing it.** Expansion keeps the old material archived and makes the change non-destructive. Reissuing throws it away.

### The procedure for a new service, written down

1. Create the virtual host.
2. Issue or expand the certificate.
3. Open a firewall rule **only if** the service needs external reachability. Most do not, because they sit behind the proxy.
4. Sync the provider firewall so the rule actually takes effect.

## Observability

A daily cron pipeline collects a 24 hour state snapshot: uptime, load, memory, disk, container list, process list, failed units, certificate expiry, SSH activity, ban counts, pending package upgrades, public HTTP health, latest deployed commit, and container restart history.

It writes that to a dated JSON file, sends it plus the prior week of snapshots to an LLM for synthesis, and emails a short operations brief through a transactional email API.

Model spend for this runs under a dollar a month.

> [!WARNING]
> This is not an uptime monitor. It runs on the machine it reports on. If the box is dead, the brief does not arrive, and a missing email is a weak signal. An external pinger is the companion layer, and it is a genuinely separate job.

Health gets checked at three depths, and each one catches a different failure class:

1. **Container HEALTHCHECK.** Catches a process that is up but not serving.
2. **Deploy-time health gate.** Catches a bad release before it becomes production.
3. **Daily synthesized brief.** Catches slow drift by comparing today against the prior week.

## Backups and recovery

- **Provider level.** Automated weekly backups retained by the host, plus manual snapshots taken deliberately before any risky session. A snapshot before you touch something dangerous is the cheapest insurance in this whole document.
- **Volume level.** Before deleting any data volume, mount it into a throwaway minimal container and write a timestamped tarball to a backup directory. Inspect first, then delete.
- **Config level.** Copy the proxy site directory before edits. Every runbook ships an explicit rollback block that restores the copy and reload-tests the config before reloading.
- **Repository as recovery aid.** The deploy script, proxy config, compose files, and Dockerfile live in the application repository. Server facts, runbooks, dated state snapshots, and audit scripts live in a separate operations repository. Between them the machine is reconstructible, and that is exactly what makes aggressive cleanup tolerable.

### The recovery ladder

In increasing order of risk. Go down it, not up it.

1. Browser console from the provider panel.
2. Snapshot restore.
3. Provider rescue mode with the real disk mounted.
4. Root password reset plus serial console.

### Known gaps, stated plainly

Application data protection currently leans on provider snapshots. There is no independent offsite copy of the database volumes, and no external uptime monitor.

Both are tracked as open items. Neither is assumed solved. If you copy this pattern, copy the gaps too, then close them.

## Cost posture

- **Server:** one fixed monthly fee. Same number every month.
- **Certificates:** free, Let's Encrypt.
- **Transactional email for the ops brief:** free tier.
- **Model spend for the daily brief:** under a dollar a month.

There is no usage-scaled infrastructure bill anywhere in this stack. That is the point. Traffic changes what the machine does, not what it costs.

## Why this travels to client work

The core principle in every engagement is that the client owns the accounts. They create the VPS, the DNS, the email provider. I get admin access to build, and full ownership transfers at handoff. Nothing to migrate at the end, because nothing was ever in my name.

The pattern is what travels: containerized app, proxy with automatic certificates, two firewall layers, loopback-bound services, script-driven deploy, runbook-backed recovery. Same shape, different account holder.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
