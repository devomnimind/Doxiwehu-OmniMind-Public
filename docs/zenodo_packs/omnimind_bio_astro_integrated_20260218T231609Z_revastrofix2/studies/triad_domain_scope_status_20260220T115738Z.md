# Triad Domain Scope Status (20260220T115738Z)

This pack closes **bio + astro** and now also materializes the **social** vertex as a federation event stream.

- Bio: present
- Astro: present
- Social: present (materialized)

Social materialization path:
- Witness DB event stream (experiences + evolution + watermarks + territory snapshot)
- Hash Alien storage index (read-only metadata)
- Recent `reports_runtime` artifacts snapshot

Primary evidence:
- `data/social_federation/federation_social_dataset_summary_20260220T115413Z.json`
- `data/social_federation/federation_social_dataset_20260220T115413Z.jsonl`

Privacy guardrail:
- No raw URLs are included; only `url_hash` + `url_netloc` + provenance-tagged events.

