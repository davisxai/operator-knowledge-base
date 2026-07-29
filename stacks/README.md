# Stacks

Self-hosted stack blueprints. One Linux box, one reverse proxy, containers behind it, and a deploy script you run from a shell.

This is the infrastructure I actually run. The marketing site, the databases, the automation workflows, the scheduled jobs. All of it sits on a single virtual machine that costs a flat monthly fee. No orchestrator. No managed platform. No bill that scales with traffic.

The same shape travels to client work. The client creates the accounts, I get admin access to build, and ownership transfers at handoff. The pattern does not change, only whose name is on the invoice.

## Index

- **[self-hosted-stack.md](self-hosted-stack.md)** What runs on the box and why. Architecture diagram, container layout, reverse proxy and TLS, backups, observability, and the honest cost picture.
- **[deploy-pattern.md](deploy-pattern.md)** Ship to a VPS, step by step. Local quality gate, CI that validates but does not deploy, one idempotent deploy script, health gate that aborts a bad release.
- **[hardening-checklist.md](hardening-checklist.md)** The security posture, in order. Two firewall layers, SSH lockdown, container flags, attack surface deletion, secrets handling, and the outage that taught the loudest lesson.

## The thesis

One box. One public listener. Everything else bound to loopback.

The reverse proxy and the SSH daemon are the entire public attack surface. Applications, databases, and caches never hold a port reachable from outside the machine. If a service does not need to be on the internet, it is not on the internet.

That single rule does more for security than any tool you can install.

## What this is not

> [!NOTE]
> This is a pattern for one operator running a handful of workloads. It is not Kubernetes, and it should not be. The tradeoff you accept is that you own patching, hardening, and uptime. The tradeoff you get back is that nothing between you and the process is a vendor abstraction you cannot debug.

If you are running a fleet of services across a team of engineers, you have outgrown this. If you are one person or a small shop shipping real software for real businesses, this is more than enough and considerably less painful.

## Read them in order

Start with `self-hosted-stack.md` to understand the shape. Read `deploy-pattern.md` when you are ready to ship something. Read `hardening-checklist.md` before you point a domain at it.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
