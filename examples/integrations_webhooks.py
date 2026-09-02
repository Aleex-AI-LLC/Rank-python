"""Webhooks and integrations — subscribe, verify, and file tickets.

Create these **before** you create and launch pentests. Tickets and callbacks
fire from live events; an integration connected after findings already exist
does not backfill them. Use ``sync`` to push a pentest after the fact.

  1. Register a tenant webhook and send a signed ping
  2. Verify a delivery with ``rank.verify_signature``
  3. List providers and create a Jira integration
  4. Test credentials, then sync a pentest
  5. Inspect finding↔ticket links

Run:
    export RANK_API_KEY=rk_...
    python examples/integrations_webhooks.py

Requirements:
    pip install rank-sdk
"""

from __future__ import annotations

import rank

client = rank.Rank()

PENTEST_ID = 1
WEBHOOK_URL = "https://example.com/rank/hooks"
JIRA_EMAIL = "bot@example.com"
JIRA_TOKEN = "replace-me"
JIRA_PROJECT = "SEC"


def main() -> None:
    print("=" * 60)
    print("  Webhooks and Integrations")
    print("=" * 60)

    print("\n--- Tenant webhook ---\n")
    print("  Create this before launching pentests so control and finding")
    print("  events reach your endpoint from the first finding onward.\n")

    try:
        created = client.webhooks.create(
            url=WEBHOOK_URL,
            events=[
                "vulnerability.validated",
                "vulnerability.retested",
                "pentest.killed",
                "control.approval_requested",
            ],
            description="SOC inbox",
        )
        print(f"  Webhook id={created.webhook.id if created.webhook else '?'}")
        print(f"  Secret (shown once): {created.secret}")
        if created.webhook:
            ping = client.webhooks.test(created.webhook.id)
            delivery = ping.delivery
            delivery_id = delivery.id if delivery else None
            status = delivery.status if delivery else None
            print(f"  Ping: {ping.message} status={status} delivery_id={delivery_id}")
    except rank.APIError as e:
        print(f"  Webhook create skipped: {e}")

    print("\n--- Signature helper ---\n")
    print("  HMAC-SHA256 of '{timestamp}.{raw_body}', header v1=..., 5 min window.")
    print("  Example:")
    print("    rank.verify_signature(raw_body, headers, secret)")

    print("\n--- Integration providers ---\n")
    providers = client.integrations.providers()
    for p in providers.providers:
        print(f"  {p.provider} ({p.label})")

    print("\n--- Create Jira integration (before the pentest) ---\n")
    try:
        integ = client.integrations.create(
            provider="jira",
            name="SecOps Jira",
            credentials={"email": JIRA_EMAIL, "api_token": JIRA_TOKEN},
            config={"project_key": JIRA_PROJECT},
            events=["vulnerability.validated"],
            sync_inbound=True,
        )
        integration = integ.integration
        print(f"  Integration id={integration.id if integration else '?'}")
        if integration:
            test = client.integrations.test(integration.id)
            detail = test.error or test.note or ""
            print(f"  Test: ok={test.ok} {detail}")

            print("\n--- Backfill an existing pentest ---\n")
            synced = client.integrations.sync(integration.id, pentest_id=PENTEST_ID)
            print(f"  Sync: {synced.message} {synced.summary}")

            links = client.integrations.links(integration.id)
            print(f"  Links: {len(links.items)}")
            for item in links.items[:5]:
                print(f"    {item}")
    except rank.APIError as e:
        print(f"  Integration skipped: {e}")

    print("\n" + "=" * 60)
    print("  DONE")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except rank.AuthenticationError:
        print("ERROR: Invalid or missing API key. Set RANK_API_KEY.")
    finally:
        client.close()
