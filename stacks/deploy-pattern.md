# The Deploy Pattern

How code gets from a laptop to a live URL on a box you own. Four layers, each with one job, no overlap.

This assumes the architecture in [self-hosted-stack.md](self-hosted-stack.md). It is generic enough to lift into any project that ships a containerized web app.

## The four layers

```
   1. LOCAL GATE          lint, typecheck, unit, build, e2e
      |                   one command, runs before you push
      v
   2. CI                  lint + typecheck in parallel on push and PR
      |                   validates only, never deploys
      v
   3. DEPLOY SCRIPT       pull, build, run, health gate, proxy, cert
      |                   one idempotent script, run on the box
      v
   4. POST-DEPLOY         search engine ping, verification commands
```

The division that matters: **CI validates, the box deploys.** CI never holds a production credential and never touches the server. If your CI can deploy, your CI can be compromised into deploying.

## Layer 1: the local quality gate

One command that runs everything, before anything gets pushed.

```json
{
  "scripts": {
    "quality:gate": "pnpm lint && pnpm typecheck && pnpm test && pnpm build && pnpm test:e2e"
  }
}
```

Lint, type check, unit tests, production build, end-to-end tests. In that order, because each one is more expensive than the last and there is no reason to run Playwright if the types do not compile.

Two details worth stealing:

- **Enforce the Node version twice.** Once in `engines.node`, once as a check script that every other script depends on. A native module compiled against the wrong Node major is a confusing failure, and the error message never says "wrong Node version."
- **Pin the package manager in `packageManager`.** Then read that same field in CI and in the Dockerfile. One source of truth for the tool version.

## Layer 2: CI that stays in its lane

Deliberately thin. A two-job matrix of lint and typecheck.

```yaml
name: ci
on:
  push:
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        task: [lint, typecheck]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm ${{ matrix.task }}
```

Why it looks like this:

- **`fail-fast: false`** so a lint failure does not hide a type error. You want both results, not the first one.
- **Concurrency cancellation per ref** so pushing three times in a minute does not run three full pipelines.
- **Node version from `.nvmrc`**, package manager from `packageManager`. CI reads the repo, it does not carry its own opinion.
- **Tests, build, and e2e are not here.** They are the local gate. This is a real tradeoff: you trade CI enforcement for speed and for keeping secrets off the runner. If you have a team, move the tests into CI. If you are one person with a gate you actually run, this is fine and honest about being fine.

## Layer 3: the deploy script

One script, on the box, idempotent. Running it twice does the same thing as running it once.

Here is the skeleton with the reasoning inline.

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_NAME="webapp"
APP_DIR="/opt/${APP_NAME}"
REPO="git@github.com:you/${APP_NAME}.git"
BRANCH="main"
HOST_PORT="3000"          # loopback only, the proxy talks to this
CONTAINER_PORT="3000"
DOMAIN="example.com"
CERT_EMAIL="you@example.com"

# 1. get the code
if [ -d "${APP_DIR}/.git" ]; then
  git -C "${APP_DIR}" fetch origin "${BRANCH}"
  git -C "${APP_DIR}" reset --hard "origin/${BRANCH}"
else
  git clone --branch "${BRANCH}" "${REPO}" "${APP_DIR}"
fi
cd "${APP_DIR}"

# 2. hard-fail on missing production env, and print the fix
if [ ! -f "${APP_DIR}/.env.production" ]; then
  echo "FATAL: ${APP_DIR}/.env.production not found."
  echo "Create it, chmod 600 it, then re-run this script."
  exit 1
fi

# 3. stop the previous container
docker rm -f "${APP_NAME}" 2>/dev/null || true

# 4. build
docker build -t "${APP_NAME}:latest" .

# 5. run with the full hardening flag set
docker run -d \
  --name "${APP_NAME}" \
  --restart unless-stopped \
  --env-file "${APP_DIR}/.env.production" \
  -p "127.0.0.1:${HOST_PORT}:${CONTAINER_PORT}" \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /app/.next/cache \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  --memory 512m \
  --cpus 1.0 \
  --pids-limit 256 \
  "${APP_NAME}:latest"

# 6. health gate: poll for 30s, fail the deploy if it never comes up
for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:${HOST_PORT}/api/health" >/dev/null 2>&1; then
    echo "healthy after ${i}s"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "FATAL: never became healthy. docker logs ${APP_NAME}"
    exit 1
  fi
  sleep 1
done

# 7. proxy config: install if missing, always config-test before reload
if [ ! -f "/etc/nginx/sites-available/${APP_NAME}" ]; then
  cp "ops/nginx-${APP_NAME}.conf" "/etc/nginx/sites-available/${APP_NAME}"
  ln -sf "/etc/nginx/sites-available/${APP_NAME}" \
         "/etc/nginx/sites-enabled/${APP_NAME}"
fi
nginx -t
systemctl reload nginx

# 8. certificate: only if one does not already exist
if [ ! -d "/etc/letsencrypt/renewal/${DOMAIN}" ]; then
  certbot --nginx -d "${DOMAIN}" -d "www.${DOMAIN}" \
    --non-interactive --agree-tos -m "${CERT_EMAIL}"
fi

# 9. print how to verify, so the next person does not have to guess
echo "verify:"
echo "  dig +short ${DOMAIN}"
echo "  curl -I https://${DOMAIN}"
echo "  docker logs -f ${APP_NAME}"
```

### The parts that carry the weight

**The env file check is a hard fail with the remediation printed.** Not a warning. Not a default. A container that starts with a missing production config is worse than a container that does not start, because it looks like it worked.

**The health gate is what makes this a deploy rather than a restart.** Poll the local endpoint once a second, up to thirty seconds, exit non-zero with a log hint if it never comes up. Without the gate, a broken build replaces a working one and you find out from a customer.

**`nginx -t` before every reload.** A syntax error in a reload takes down every site on the box, not just the one you were editing.

**Certificate issuance is conditional.** Requesting a cert you already have burns rate limit for nothing. Adding a hostname to an existing cert should be an expansion, not a fresh issue.

**Every step is safe to re-run.** Clone or fast-forward. Remove the container or ignore that it was not there. Install the vhost or leave the existing one. Issue the cert or skip it. Idempotent is not a nicety here, it is what lets you re-run after a failure without thinking.

> [!TIP]
> Read the last block again. Printing the verification commands at the end costs three lines and saves the next person, including future you at 2am, from having to remember the health endpoint path and the container name.

## Layer 4: post-deploy

**Ping the search engines that accept instant indexing.** A script that reads your sitemap and submits every URL to IndexNow gets Bing, Yandex, DuckDuckGo through Bing, and Seznam to recrawl immediately. Google does not participate in IndexNow, so this is not a full solution, it is the free half.

**Verify by hand the first few times.** DNS resolution, a `curl -I` against the public URL, container logs. Automate it after you have watched it work.

## The trigger

Normally a human in a shell session running the script. That is the correct default. You are present, you watch the health gate, you read the output.

A webhook listener service on the machine can trigger the same script from a repository event when you want push-to-deploy. Same code path, so there is nothing new to debug. Just be clear-eyed that you have traded "someone is watching" for "it happens fast."

## The bare-metal variant

When containers are not on the table, the same shape works directly against the host:

1. Fetch and fast-forward the branch.
2. Reinstall against the lockfile.
3. Rebuild from a clean output directory.
4. Stop whatever process currently holds the target port.
5. Restart through a launcher script that syncs static and public assets into the standalone bundle.
6. **Assert that the rendered page actually references a stylesheet, and that the stylesheet is served with the right content type.**

> [!WARNING]
> Step 6 is not paranoia. A silent static asset path break is the characteristic failure of standalone builds. The server returns 200, the HTML is correct, and the page renders completely unstyled. Nothing in the process exits non-zero. The only way to catch it is to assert on the actual response.

That last point generalizes past this one build mode. **Every deploy mode has one characteristic silent failure.** Find yours and write an assertion for it. A health check that only proves the process is alive is not enough.

## Checklist

- [ ] One local command runs lint, typecheck, tests, build, and e2e
- [ ] Node version and package manager version are pinned and read from the repo everywhere
- [ ] CI validates and holds no production credentials
- [ ] Deploy is one idempotent script that lives in the repo
- [ ] Missing production env is a hard fail with the fix printed
- [ ] Container runs read-only, non-root, capabilities dropped, resource-limited
- [ ] Port binds to loopback, never `0.0.0.0`
- [ ] Health gate polls and exits non-zero on failure
- [ ] Proxy config is tested before reload
- [ ] Certificate issuance is conditional and expands rather than reissues
- [ ] The script prints verification commands when it finishes
- [ ] You have an assertion for your deploy mode's characteristic silent failure

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
