import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

const config = {
  // If every page is force-dynamic and nothing revalidates, the
  // read-only build-time cache is enough. Swap for the R2 cache if ISR
  // or revalidateTag ever lands.
  ...defineCloudflareConfig({
    incrementalCache: staticAssetsIncrementalCache,
    enableCacheInterception: true,
  }),
  // Next 16.3.8 leaves the proxy bundle (server/middleware.js) out of the
  // standalone folder, and @opennextjs/aws copyTracedFiles asserts it there.
  // It already back-fills server/instrumentation.js the same way. Drop the
  // cp once upstream does the same for middleware.js.
  buildCommand:
    "next build && cp .next/server/middleware.js .next/standalone/.next/server/middleware.js",
};

export default config;
