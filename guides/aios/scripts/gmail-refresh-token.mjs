// Usage: GMAIL_CLIENT_ID=... GMAIL_CLIENT_SECRET=... node gmail-refresh-token.mjs
// Mints one long-lived Gmail refresh token for one mailbox. Run it once per inbox.
// Needs: npm install google-auth-library, and a Google Cloud OAuth client of type "Desktop app".
import http from "node:http";
import { OAuth2Client } from "google-auth-library";

const clientId = process.env.GMAIL_CLIENT_ID;
const clientSecret = process.env.GMAIL_CLIENT_SECRET;
if (!clientId || !clientSecret) {
  console.error("Set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET first.");
  process.exit(1);
}

const PORT = Number(process.env.PORT ?? 53682);
const redirectUri = `http://127.0.0.1:${PORT}`;
// gmail.modify covers read, labels, archive, trash, and drafts. It cannot permanently delete.
const SCOPES = ["https://www.googleapis.com/auth/gmail.modify"];

const client = new OAuth2Client({ clientId, clientSecret, redirectUri });
const authUrl = client.generateAuthUrl({
  access_type: "offline",
  prompt: "consent",
  scope: SCOPES,
});

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", redirectUri);
  const code = url.searchParams.get("code");
  if (!code) {
    res.writeHead(400).end("No code in the redirect. Close this tab and run the script again.");
    return;
  }
  try {
    const { tokens } = await client.getToken(code);
    res.writeHead(200, { "Content-Type": "text/plain" }).end("Done. Go back to the terminal.");
    if (!tokens.refresh_token) {
      console.error("Google returned no refresh token. Remove the app's access at myaccount.google.com/permissions and run again.");
      process.exitCode = 1;
    } else {
      console.log("\nPaste this into your .env (one line per mailbox, rename the key):\n");
      console.log(`GMAIL_PRIMARY_REFRESH_TOKEN=${tokens.refresh_token}\n`);
    }
  } catch (err) {
    res.writeHead(500).end("Token exchange failed. Check the terminal.");
    console.error(err);
    process.exitCode = 1;
  } finally {
    server.close();
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log("Open this URL in the browser signed into the mailbox you want to connect:\n");
  console.log(authUrl);
});
