# 4Levels Sports Advisory — how to deploy

The site is static: one `index.html`, an `assets/` folder, and one serverless
function (`api/lead.js`) for the contact form. No build step. No frameworks.

## Push and deploy (the usual flow)

1. Open Cursor. Open the folder `~/Documents/AI-Syndicate/4Levels-Sports-Advisory`.
2. In the Cursor terminal, run: `git init && git add -A && git commit -m "4Levels site v1"`
3. Create a new GitHub repo named `4levels-site` and push to it.
4. Go to vercel.com → **Add New… → Project** → pick the `4levels-site` repo.
5. Framework Preset: leave as **Other**. Root Directory: leave as `./` (the repo root — do NOT set a subfolder; this repo has none).
6. Click **Deploy**. The site works immediately on the `.vercel.app` URL.

## Make the contact form actually send (2 minutes, after deploy)

Right now the form shows "The form is not connected yet" when someone submits.
That is on purpose — it never fakes a thank-you. To connect it:

1. In Vercel, open the project → **Settings → Environment Variables**.
2. Add `RESEND_API_KEY` — the key from our Resend account (ryder@aisyndicate.com login).
3. Add `LEAD_FROM_EMAIL` — paste exactly: `4Levels Website <leads@contact.aisyndicate.com>`
   (that domain is already verified in Resend — never use onboarding@resend.dev).
4. Add `LEAD_TO_EMAIL` — **we don't have the client's email yet.** This is the one
   thing blocked until 4Levels tells us where leads should land.
5. Optional: add `LEAD_BCC_EMAIL` = `growth@aisyndicate.com` so we get a copy as proof.
6. **Redeploy** (Deployments → ⋯ on the latest → Redeploy). Env changes do nothing
   until a redeploy — Vercel only mentions this in a small blue toast.
7. Test without sending an email: open `https://<the-site>/api/lead?diag=1` in a
   browser. It answers in plain English whether the key, sender, and recipient are right.
8. Then do one real test: fill the form on the live site, submit, and check the inbox.

## Before launch — two things to confirm with the client

1. **og:image URL.** Once the live URL exists, open `index.html` and replace
   `/assets/og.png` in the `og:image` meta tag with the full URL
   (`https://<the-site>/assets/og.png`). Link previews ignore relative paths.
2. **The footer line** "Educational guidance — not legal, tax, or investment advice"
   is a safe default, but it must match what 4Levels is actually licensed to do.
   Ask them before launch. Same for the "Coaches & Programs" column — confirm they
   actually serve programs, or cut it.

## Notes

- The font is self-hosted in `assets/fonts/` (Archivo variable, from
  @fontsource-variable/archivo v5.3.0). No Google Fonts request, nothing external at all.
- The logo is rebuilt as inline SVG (not an image file), which is what makes the
  bar animation possible. Click the big logo on the live site — it replays.
- `assets/og.png` is the social-share card. `assets/favicon.svg` is the tab icon.
