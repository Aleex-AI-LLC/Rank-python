"""Engagement control — RoE, approvals, kill switch, and the audit chain.

This script shows the fail-closed control plane around a pentest:

  1. Inspect the approval-class catalog
  2. Create and activate a Rules of Engagement that covers the assets
  3. List pending approvals and decide them
  4. Read the hashed audit chain (and verify it)
  5. Emergency stop with the kill switch (distinct from cancel)

Create the pentest first; without an active RoE the run will not start.

Run:
    export RANK_API_KEY=rk_...
    python examples/engagement_control.py

Requirements:
    pip install rank-sdk
"""

from __future__ import annotations

import rank

client = rank.Rank()

PENTEST_ID = 1  # ID of a pentest whose assets fall inside the RoE below


def main() -> None:
    print("=" * 60)
    print("  Engagement Control")
    print("=" * 60)

    print("\n--- Approval classes ---\n")
    classes = client.catalogs.list_approval_classes()
    for c in classes.items:
        print(f"  [{c.id}] {c.description}")

    print("\n--- Current RoE ---\n")
    current = client.pentests.roe.retrieve(PENTEST_ID)
    if current.active:
        print(f"  Active v{current.active.version} status={current.active.status}")
    else:
        print("  No active RoE — the orchestrator will not start.")

    print("\n--- Create and activate RoE ---\n")
    try:
        roe = client.pentests.roe.create(
            PENTEST_ID,
            allowed_domains=["example.com"],
            timezone="Europe/Madrid",
            max_rps=10,
            max_concurrency=4,
            requires_approval_for=["exploit"],
            authorization_ref="ENG-2026-0042",
            activate=True,
        )
        print(f"  Activated v{roe.version} status={roe.status}")
    except rank.APIError as e:
        print(f"  Create skipped (assets may be outside example.com): {e}")

    print("\n--- Pending approvals ---\n")
    pending = client.pentests.approvals.list(PENTEST_ID, status="pending")
    print(f"  {pending.total} pending")
    for a in pending.approvals:
        print(f"  [{a.id}] {a.action_class} target={a.target}")
        try:
            decided = client.pentests.approvals.decide(
                PENTEST_ID, a.id,
                decision="approve",
                reason="In scope for this window",
            )
            print(f"    → {decided.status}")
        except rank.APIError as e:
            print(f"    Decide skipped: {e}")

    print("\n--- Audit chain ---\n")
    chain = client.pentests.audit_chain(PENTEST_ID)
    print(f"  Events: {chain.total if chain.total is not None else len(chain.events)}")
    verify = client.pentests.verify_audit_chain(PENTEST_ID)
    print(f"  Intact: {verify.intact}")

    print("\n--- Kill vs cancel ---\n")
    print("  cancel() asks a running stream to stop (Go).")
    print("  kill() is the terminal switch (PHP); evidence is preserved.")
    print("  Uncomment the next line to actually halt the run.")
    # client.pentests.kill(PENTEST_ID, reason="Out of authorized window")

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
