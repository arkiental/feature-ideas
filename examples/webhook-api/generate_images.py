"""Regenerate the five accessible SVG diagrams using Python 3 (standard library only).

From this directory: python generate_images.py
Optional PNGs: npm install --no-save --package-lock=false sharp && node render_images.mjs
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent / "images"
OUT.mkdir(exist_ok=True)
FEATURES = [
    dict(id="01-safe-replay", title="Safe replay after an endpoint outage", subtitle="Concept • Retry a selected failed delivery without creating an accidental second job.",
         cards=[("1 / TRIGGER", "Developer selects failure", ["evt_104 → ep_billing", "Last response: 503", "POST /deliveries/dlv_82/replays", "Idempotency-Key: repair-82"]),
                ("2 / MECHANISM", "Create one replay job", ["Check tenant + retention", "Reserve key atomically", "Copy original event body", "New delivery: dlv_83"]),
                ("3 / RESULT", "Trace the recovery", ["202 Accepted → dlv_83", "Repeat key → same job", "Delivery response: 204", "Replay-of: dlv_82"])],
         flow=[("Original attempt", "dlv_82 · 503"), ("One replay job", "dlv_83 · queued"), ("Receiver succeeds", "dlv_83 · 204")],
         notes=["A repeated request returns the existing replay job; it does not enqueue a second one.", "A successful delivery can still be received more than once: the receiver must deduplicate evt_104.", "Expired payload → 410 payload_expired; no empty replay job is created."]),
    dict(id="02-signing-key-rotation", title="Rotate signing secrets without a cutover outage", subtitle="Concept • Verify a new secret while the previous secret remains valid during a bounded overlap.",
         cards=[("1 / TRIGGER", "Create replacement key", ["POST /endpoints/ep_9/keys", "Old key: key_4", "New key: key_5", "Overlap: 24 hours"]),
                ("2 / MECHANISM", "Sign with both keys", ["Same timestamp + raw body", "Signatures tagged with key IDs", "Receiver installs key_5", "Old key remains usable"]),
                ("3 / RESULT", "Retire the old key", ["Receiver verifies key_5", "Deadline expires", "Sign only with key_5", "Audit key_4 retirement"])],
         flow=[("Before rotation", "key_4 signature"), ("Overlap window", "key_4 + key_5"), ("After deadline", "key_5 signature")],
         notes=["A rotation guide shows how to accept either valid signature over identical signed content.", "New secret is shown once. Logs expose only key IDs, never secrets or full signature headers.", "An unready receiver may fail after expiry; show the exact deadline and recovery instructions."]),
    dict(id="03-adaptive-retries", title="Respect endpoint backpressure", subtitle="Concept • Replace synchronized fixed retries with bounded, endpoint-aware scheduling.",
         cards=[("1 / TRIGGER", "Receiver asks for time", ["evt_105 → ep_orders", "HTTP 429 Too Many Requests", "Retry-After: 120", "Policy: max 6 attempts"]),
                ("2 / MECHANISM", "Schedule a safe retry", ["Parse delay or HTTP date", "Apply policy caps + jitter", "Persist next_attempt_at", "Release the worker slot"]),
                ("3 / RESULT", "Recover transparently", ["Retry no earlier than 120s", "Attempt 2 returns 204", "Status: delivered", "Attempts remain inspectable"])],
         flow=[("Attempt 1", "429 · wait requested"), ("Durable schedule", "120s + bounded jitter"), ("Attempt 2", "204 · delivered")],
         notes=["Retryable statuses are explicit; ordinary 4xx failures stop automatically by default.", "Missing or malformed Retry-After → documented exponential backoff with bounded jitter.", "A delay beyond the delivery deadline ends in a clear terminal state instead of an early retry."]),
    dict(id="04-event-contracts", title="Catch event contract errors before dispatch", subtitle="Concept • Validate a versioned event body at ingestion and return an actionable error path.",
         cards=[("1 / TRIGGER", "Producer submits event", ["type: invoice.paid", "schema_version: 2", "data.amount_minor: \"4900\"", "Contract expects integer"]),
                ("2 / MECHANISM", "Validate before queueing", ["Resolve immutable schema v2", "Validate supported keywords", "Locate invalid value", "Do not create a delivery"]),
                ("3 / RESULT", "Producer corrects input", ["422 schema_validation_failed", "path: /data/amount_minor", "expected: integer", "Resend 4900 → 202 Accepted"])],
         flow=[("Invalid payload", "\"4900\" · string"), ("Precise feedback", "/data/amount_minor"), ("Corrected payload", "4900 · integer")],
         notes=["Unconfigured event types preserve current ingestion behavior; strictness is opt-in per type.", "Schema versions are immutable, so old producers retain their explicit contract.", "Bound schema depth and validation time; reject remote references instead of fetching URLs."]),
    dict(id="05-tenant-budgets", title="Keep one tenant's burst from blocking others", subtitle="Concept • Allocate bounded delivery capacity per tenant with visible queue and quota feedback.",
         cards=[("1 / TRIGGER", "Two tenants send work", ["acme: 10,000 queued events", "birch: 2 queued events", "acme in-flight limit: 10", "birch in-flight limit: 10"]),
                ("2 / MECHANISM", "Schedule fair turns", ["Per-tenant ready queues", "Shared worker pool", "Atomic in-flight leases", "Per-tenant backlog cap"]),
                ("3 / RESULT", "Both tenants progress", ["birch gets eligible turns", "acme continues draining", "Quota state is inspectable", "No cross-tenant event access"])],
         flow=[("acme burst", "Bounded queue + concurrency"), ("Fair scheduler", "Eligible tenant turns"), ("birch requests", "Progress while acme drains")],
         notes=["Ordering remains unspecified. Fairness applies to runnable work, not slow external responses.", "At backlog cap, reject new ingestion with 429 and a documented retry policy; never silently drop.", "Lease expiry recovers crashed workers; receiver idempotency still handles duplicate attempts."]),
]

def text(x, y, value, size=21, weight=400, fill="#152A3A"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>'

def render(f):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="880" viewBox="0 0 1400 880" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(f["title"])}</title>', f'<desc id="desc">{escape(f["subtitle"])} {escape(" ".join(f["notes"]))}</desc>',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#2262C6"/></marker></defs>',
             '<rect width="1400" height="880" fill="#F7F5EF"/>', '<g font-family="Arial, Helvetica, sans-serif">',
             text(56, 55, 'RELAYBOX / ILLUSTRATED FEATURE IDEAS', 16, 700, '#2262C6'), text(56, 109, f['title'], 37, 700),
             text(56, 150, f['subtitle'], 21), '<line x1="56" y1="179" x2="1344" y2="179" stroke="#B4BFCA"/>']
    for idx, (label, title, lines) in enumerate(f['cards']):
        x = 56 + idx * 444
        parts += [f'<rect x="{x}" y="212" width="400" height="279" fill="#FFFFFF" stroke="#B4BFCA"/>',
                  text(x+22, 247, label, 16, 700, '#2262C6'), text(x+22, 288, title, 25, 700)]
        for j, line in enumerate(lines):
            parts.append(text(x+22, 335+j*37, line, 20))
        if idx < 2:
            parts.append(f'<path d="M{x+408} 351 H{x+435}" fill="none" stroke="#2262C6" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(56, 544, 'WHAT CHANGES', 16, 700, '#2262C6'))
    for i, (label, detail) in enumerate(f['flow']):
        x = 56+i*444
        parts += [text(x, 586, label, 24, 700), text(x, 621, detail, 20)]
        if i < 2:
            parts.append(f'<path d="M{x+365} 580 H{x+425}" fill="none" stroke="#2262C6" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append('<line x1="56" y1="658" x2="1344" y2="658" stroke="#B4BFCA"/>')
    for i, note in enumerate(f['notes']):
        parts += [text(56, 703+i*47, f'{i+1:02d}', 18, 700, '#2262C6'), text(98, 703+i*47, note, 19)]
    parts += [text(56, 850, 'Fictional project • Synthetic data • Proposed behavior, not a shipped feature or measured result', 15, 400, '#526675'), '</g></svg>']
    (OUT / f'{f["id"]}.svg').write_text('\n'.join(parts), encoding='utf-8')

if __name__ == '__main__':
    for feature in FEATURES:
        render(feature)
    print(f'Wrote {len(FEATURES)} SVG diagrams to {OUT}')
