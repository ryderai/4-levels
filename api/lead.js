/* ============================================================
   4Levels Sports Advisory — LEAD FORM handler (Vercel serverless function)
   ------------------------------------------------------------
   Same handler pattern as our other client sites: it actually
   sends the email server-side and tells the browser whether it
   worked. The page only says "sent" when it really did.

   ENVIRONMENT VARIABLES (Vercel → Settings → Environment Variables)
     RESEND_API_KEY   required to send. Without it this returns 503
                      and the page tells the visitor the form is not
                      connected yet — never a fake thank-you.
     LEAD_TO_EMAIL    required — where 4Levels wants leads to land.
                      Not set yet: we do not have the client's email.
     LEAD_FROM_EMAIL  set to an address on our verified domain, e.g.
                      "4Levels Website <leads@contact.aisyndicate.com>"
                      NEVER leave this on onboarding@resend.dev — the
                      sandbox sender only delivers to the Resend
                      account owner's own address.
     LEAD_BCC_EMAIL   optional — a copy for AI Syndicate, so we can
                      prove leads are arriving.

   Debug without guessing: GET /api/lead?diag=1 (sends no email,
   names the fault in plain English, never prints the key).
   ============================================================ */

const RESEND_URL   = "https://api.resend.com/emails";
const DEFAULT_TO   = "";  // deliberately empty — set LEAD_TO_EMAIL in Vercel
const DEFAULT_FROM = "4Levels Website <onboarding@resend.dev>";

const MAX_FIELD  = 4000;    // per answer
const MAX_FIELDS = 30;

/* Field names the form uses for its own plumbing, not real answers. */
const META_FIELDS = new Set(["_form", "_page", "_started", "website"]);

const esc = (s) => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/* Header injection guard: a newline in the reply-to would let a spammer
   append their own headers. */
const oneLine = (s) => String(s || "").replace(/[\r\n]+/g, " ").trim().slice(0, 200);

const looksLikeEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(s || "").trim());

function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") {
    try { return JSON.parse(req.body); } catch { return {}; }
  }
  return {};
}

/* ---------- diag: why did a send fail? ----------
   GET /api/lead?diag=1 — sends NO email, never prints the key. */
async function diag(res) {
  const key  = process.env.RESEND_API_KEY;
  const from = process.env.LEAD_FROM_EMAIL || DEFAULT_FROM;
  const to   = process.env.LEAD_TO_EMAIL   || DEFAULT_TO;

  const out = {
    ok: true,
    keySet: Boolean(key),
    keyLooksLikeResend: Boolean(key && key.startsWith("re_")),
    from, to: to || "(NOT SET — set LEAD_TO_EMAIL)",
    bcc: process.env.LEAD_BCC_EMAIL || null,
    usingSandboxSender: /resend\.dev/i.test(from)
  };

  if (!key) {
    out.verdict = "No RESEND_API_KEY set. Nothing can send.";
    return res.status(200).json(out);
  }
  if (!to) {
    out.verdict = "No LEAD_TO_EMAIL set. There is nowhere to deliver leads.";
    return res.status(200).json(out);
  }

  try {
    const r = await fetch("https://api.resend.com/domains", {
      headers: { Authorization: `Bearer ${key}` }
    });
    out.resendStatus = r.status;
    const body = await r.json().catch(() => ({}));

    if (r.status === 401 || r.status === 403) {
      out.verdict = "Resend rejected the key. It is wrong, revoked, or was rotated without updating Vercel.";
      return res.status(200).json(out);
    }

    const domains = (body.data || body || []);
    out.domains = Array.isArray(domains)
      ? domains.map(d => ({ name: d.name, status: d.status, region: d.region }))
      : domains;
    const verified = (Array.isArray(domains) ? domains : []).filter(d => d.status === "verified");
    out.verifiedDomains = verified.map(d => d.name);

    const fromDomain = String(from).split("@").pop().replace(/>$/, "").trim();
    out.fromDomainVerified = out.verifiedDomains.includes(fromDomain);

    if (!verified.length) {
      out.verdict = "No verified sending domain in Resend. With the sandbox sender, Resend " +
        "only delivers to the email address the Resend account was created with. Set " +
        "LEAD_FROM_EMAIL to an address on contact.aisyndicate.com (already verified).";
    } else if (!out.fromDomainVerified) {
      out.verdict = `LEAD_FROM_EMAIL uses "${fromDomain}", which is not verified. ` +
        `Verified: ${out.verifiedDomains.join(", ")}. Set LEAD_FROM_EMAIL to an address on one of those.`;
    } else {
      out.verdict = "Key and sending domain both look correct. If sends still fail, read the " +
        "exact Resend error in the Vercel function logs for /api/lead.";
    }
    return res.status(200).json(out);

  } catch (err) {
    out.verdict = "Could not reach Resend: " + err.message.slice(0, 140);
    return res.status(200).json(out);
  }
}

export default async function handler(req, res) {
  if (req.query && req.query.diag) return diag(res);

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "METHOD", message: "Use POST." });
  }

  const body = readBody(req);

  /* Honeypot. A real person never fills a hidden field; bots fill everything.
     Answer 200 so the bot believes it worked and does not retry. */
  if (body.website) {
    console.log("[lead] honeypot triggered, dropped");
    return res.status(200).json({ ok: true, dropped: true });
  }

  /* Bots also submit instantly. A human needs at least a couple of seconds. */
  const started = Number(body._started);
  if (started && Date.now() - started < 1500) {
    console.log("[lead] submitted too fast, dropped");
    return res.status(200).json({ ok: true, dropped: true });
  }

  const formName = oneLine(body._form || "Website enquiry");
  const pagePath = oneLine(body._page || "");

  const answers = Object.entries(body)
    .filter(([k, v]) => !META_FIELDS.has(k) && v != null && String(v).trim() !== "")
    .slice(0, MAX_FIELDS)
    .map(([k, v]) => [oneLine(k), String(v).slice(0, MAX_FIELD)]);

  if (!answers.length) {
    return res.status(400).json({ ok: false, error: "EMPTY",
      message: "Please fill in the form before sending." });
  }

  /* Reply-To so 4Levels can just hit reply. */
  const emailField = answers.find(([k, v]) => /e-?mail/i.test(k) && looksLikeEmail(v));
  const nameField  = answers.find(([k]) => /name/i.test(k));
  const replyTo    = emailField ? oneLine(emailField[1]) : null;

  const subject = `[Website] ${formName}` + (nameField ? ` — ${oneLine(nameField[1])}` : "");

  const rows = answers.map(([k, v]) =>
    `<tr><td style="padding:6px 14px 6px 0;vertical-align:top;color:#666;white-space:nowrap">${esc(k)}</td>` +
    `<td style="padding:6px 0;vertical-align:top"><b>${esc(v).replace(/\n/g, "<br>")}</b></td></tr>`).join("");

  const html =
    `<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:15px;color:#111">` +
    `<p style="margin:0 0 14px">New enquiry from the <b>4Levels Sports Advisory</b> website</p>` +
    `<table style="border-collapse:collapse">${rows}</table>` +
    `<p style="margin:18px 0 0;font-size:12px;color:#888">Form: ${esc(formName)}` +
    (pagePath ? ` &middot; Page: ${esc(pagePath)}` : "") +
    (replyTo ? ` &middot; Reply goes straight to ${esc(replyTo)}` : "") + `</p></div>`;

  const text = answers.map(([k, v]) => `${k}: ${v}`).join("\n") +
    `\n\n---\nForm: ${formName}${pagePath ? ` | Page: ${pagePath}` : ""}`;

  /* Log every lead before trying to send. If the email provider is down, the
     lead still exists in the Vercel logs and can be recovered by hand. A lead
     must never vanish without a trace. */
  console.log("[lead]", JSON.stringify({ formName, pagePath, answers }));

  const key = process.env.RESEND_API_KEY;
  const to  = process.env.LEAD_TO_EMAIL || DEFAULT_TO;
  if (!key || !to) {
    return res.status(503).json({ ok: false, error: "NOTCONFIGURED",
      message: "The form is not connected yet." });
  }

  try {
    const payload = {
      from: process.env.LEAD_FROM_EMAIL || DEFAULT_FROM,
      to: [to],
      subject,
      html,
      text
    };
    if (replyTo) payload.reply_to = replyTo;
    if (process.env.LEAD_BCC_EMAIL) payload.bcc = [process.env.LEAD_BCC_EMAIL];

    const r = await fetch(RESEND_URL, {
      method: "POST",
      headers: { "Authorization": `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!r.ok) {
      const detail = await r.text().catch(() => "");
      console.error("[lead] send failed", r.status, detail.slice(0, 300));
      return res.status(502).json({ ok: false, error: "SENDFAILED",
        message: "We could not send that just now." });
    }

    return res.status(200).json({ ok: true });

  } catch (err) {
    console.error("[lead]", err.message);
    return res.status(502).json({ ok: false, error: "SENDFAILED",
      message: "We could not send that just now." });
  }
}
