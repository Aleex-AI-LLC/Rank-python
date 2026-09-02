"""Sealed reports, SARIF export, and retest of resolved findings.

  1. Inspect the effective report profile for a pentest
  2. Generate a report (seals files + emails the PDF)
  3. List issued reports and fetch a signed download URL
  4. Export findings as SARIF
  5. Enqueue a retest and inspect the run

The pentest must be completed before ``generate_report``. Create integrations
before the original run if you want tickets to open from live events.

Run:
    export RANK_API_KEY=rk_...
    python examples/reports_and_retest.py

Requirements:
    pip install rank-sdk
"""

from __future__ import annotations

import rank

client = rank.Rank()

PENTEST_ID = 1
RECIPIENT = "security@example.com"


def main() -> None:
    print("=" * 60)
    print("  Reports and Retest")
    print("=" * 60)

    print("\n--- Report settings ---\n")
    settings = client.pentests.report_settings.retrieve(PENTEST_ID)
    if settings.effective:
        print(f"  Audience : {settings.effective.audience}")
        print(f"  Formats  : {settings.effective.default_formats}")
        print(f"  Method   : {settings.effective.methodology}")

    print("\n--- Generate and seal ---\n")
    try:
        generated = client.pentests.generate_report(
            PENTEST_ID,
            recipient_email=RECIPIENT,
            recipient_name="Security Team",
            extended=1,
            formats=["pdf", "html", "json"],
            audience="technical",
        )
        print(f"  {generated.message} sealed={generated.sealed} emailed={generated.emailed}")
    except rank.APIError as e:
        print(f"  Generate skipped: {e}")

    print("\n--- Issued reports ---\n")
    reports = client.pentests.reports.list(PENTEST_ID)
    for r in reports.items:
        print(f"  [{r.id}] {r.format} sha256={r.payload_sha256} sealed_at={r.sealed_at}")
    if reports.items:
        download = client.pentests.reports.retrieve(PENTEST_ID, reports.items[0].id)
        print(f"  Download URL: {download.url}")

    print("\n--- Evidence manifest ---\n")
    try:
        manifest = client.pentests.manifest(PENTEST_ID)
        print(f"  merkle_root={manifest.merkle_root} valid={manifest.signature_valid}")
        artifacts = client.pentests.evidence.list(PENTEST_ID)
        print(f"  Artifacts: {len(artifacts.items)}")
    except rank.APIError as e:
        print(f"  Manifest skipped (run not sealed yet?): {e}")

    print("\n--- SARIF export ---\n")
    try:
        sarif = client.pentests.vulnerabilities.export(PENTEST_ID, format="sarif")
        if isinstance(sarif, rank.VulnerabilityExportFile):
            print(f"  {sarif.filename or 'findings.sarif'}: {len(sarif.content)} bytes")
    except rank.APIError as e:
        print(f"  SARIF skipped: {e}")

    print("\n--- Retest ---\n")
    vulns = client.pentests.vulnerabilities.list(PENTEST_ID)
    resolved = next((v for v in vulns.items if v.status == "resolved"), None)
    try:
        if resolved:
            run = client.pentests.vulnerabilities.retest(PENTEST_ID, resolved.id)
        else:
            run = client.pentests.retest(PENTEST_ID)
        print(f"  Run {run.id} status={run.status} origin={run.origin}")
    except rank.APIError as e:
        print(f"  Enqueue skipped: {e}")

    runs = client.pentests.retests.list(PENTEST_ID)
    print(f"  Retest runs: {len(runs.items)}")
    if runs.items:
        detail = client.pentests.retests.retrieve(PENTEST_ID, runs.items[0].id)
        print(f"  Detail findings: {len(detail.findings)}")

    print("\n" + "=" * 60)
    print("  DONE")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except rank.AuthenticationError:
        print("ERROR: Invalid or missing API key. Set RANK_API_KEY.")
    except rank.NotFoundError:
        print(f"ERROR: Pentest #{PENTEST_ID} not found. Update PENTEST_ID.")
    finally:
        client.close()
