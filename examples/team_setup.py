"""Team setup workflow — create a team, define roles, and invite members.

This script demonstrates how to set up a team from scratch with a proper
role and permission structure:

  1. Create a team
  2. List available permissions in the platform
  3. Create roles with specific permissions (Admin, Pentester, Viewer)
  4. Invite members with assigned roles
  5. Share agents with the team
  6. Check team usage
  7. Cleanup

Run:
    export RANK_API_KEY=rk_...
    python examples/team_setup.py

Requirements:
    pip install rank-sdk
"""

from __future__ import annotations

import rank

client = rank.Rank()


def main() -> None:
    print("=" * 60)
    print("  Team Setup Workflow")
    print("=" * 60)

    # -----------------------------------------------------------------
    # 1. Create a team
    # -----------------------------------------------------------------
    print("\n--- Creating team ---\n")

    team = client.teams.create(
        name="Red Team Alpha",
        description="Offensive security team for quarterly pentests",
    )
    team_id = team.id
    print(f"  Team created: id={team_id}, name={team.name}")

    # -----------------------------------------------------------------
    # 2. List available permissions
    # -----------------------------------------------------------------
    print("\n--- Available permissions ---\n")

    permissions = client.permissions.list()
    for p in permissions.items:
        print(f"  [{p.id}] {p.name}")

    all_perm_ids = [p.id for p in permissions.items]

    # -----------------------------------------------------------------
    # 3. Create roles with different permission levels
    # -----------------------------------------------------------------
    print("\n--- Creating roles ---\n")

    # Team Admin — full access
    admin_role = client.teams.roles.create(
        team_id,
        role_name="Team Admin",
        color="#E74C3C",
        description="Full access to all team resources",
    )
    client.teams.roles.add_permissions(team_id, admin_role.id, permission_ids=all_perm_ids)
    print(f"  Created: [{admin_role.id}] Team Admin ({len(all_perm_ids)} permissions)")

    # Pentester — can run pentests and manage vulnerabilities
    pentester_perm_ids = all_perm_ids[:6]  # first N permissions as example
    pentester_role = client.teams.roles.create(
        team_id,
        role_name="Pentester",
        color="#3498DB",
        description="Can execute pentests and triage vulnerabilities",
    )
    client.teams.roles.add_permissions(team_id, pentester_role.id, permission_ids=pentester_perm_ids)
    print(f"  Created: [{pentester_role.id}] Pentester ({len(pentester_perm_ids)} permissions)")

    # Viewer — read-only access
    viewer_perm_ids = all_perm_ids[:2]  # minimal permissions
    viewer_role = client.teams.roles.create(
        team_id,
        role_name="Viewer",
        color="#95A5A6",
        description="Read-only access to team resources",
    )
    client.teams.roles.add_permissions(team_id, viewer_role.id, permission_ids=viewer_perm_ids)
    print(f"  Created: [{viewer_role.id}] Viewer ({len(viewer_perm_ids)} permissions)")

    # -----------------------------------------------------------------
    # 4. List roles and their permissions
    # -----------------------------------------------------------------
    print("\n--- Team roles ---\n")

    roles = client.teams.roles.list(team_id)
    for r in roles.items:
        perms = client.teams.roles.list_permissions(team_id, r.id)
        perm_names = [p.name for p in perms]
        print(f"  [{r.id}] {r.role_name} — {len(perm_names)} permissions")

    # -----------------------------------------------------------------
    # 5. Invite members
    # -----------------------------------------------------------------
    print("\n--- Inviting members ---\n")

    invites = [
        ("lead@example.com", admin_role.id),
        ("pentester@example.com", pentester_role.id),
        ("manager@example.com", viewer_role.id),
    ]

    for email, role_id in invites:
        try:
            client.teams.invitations.create(team_id, email=email, role_id=role_id)
            print(f"  Invited {email} with role_id={role_id}")
        except rank.APIError as e:
            print(f"  Could not invite {email}: {e}")

    # List pending invitations
    print("\n--- Pending invitations ---\n")

    invitations = client.teams.invitations.list(team_id)
    for inv in invitations.items:
        print(f"  {inv.email} — status: {inv.status}")

    # -----------------------------------------------------------------
    # 6. Share agents with the team
    # -----------------------------------------------------------------
    print("\n--- Sharing agents ---\n")

    try:
        my_agents = client.agents.mine()
        if my_agents.items:
            agent = my_agents.items[0]
            client.teams.agents.create(team_id, agent_id=agent.id)
            print(f"  Shared agent [{agent.id}] {agent.name} with the team")
        else:
            print("  No personal agents to share")
    except rank.APIError as e:
        print(f"  Could not share agent: {e}")

    # List team agents
    team_agents = client.teams.agents.list(team_id)
    for ta in team_agents.items:
        print(f"  [{ta.agent_id}] {ta.name}")

    # -----------------------------------------------------------------
    # 7. Check usage
    # -----------------------------------------------------------------
    print("\n--- Team usage ---\n")

    try:
        usage = client.teams.usage.summary(team_id)
        print(f"  Usage summary: {usage}")
    except rank.APIError as e:
        print(f"  Usage not available: {e}")

    # -----------------------------------------------------------------
    # 8. View team details
    # -----------------------------------------------------------------
    print("\n--- Team details ---\n")

    team_detail = client.teams.retrieve(team_id)
    print(f"  Name        : {team_detail.name}")
    print(f"  Description : {team_detail.description}")
    print(f"  Owner       : {team_detail.owner_id}")

    # List members (just the owner at this point)
    members = client.teams.members.list(team_id)
    for m in members.items:
        print(f"  Member: [{m.user_id}] {m.username}")

    # -----------------------------------------------------------------
    # 9. My roles in this team
    # -----------------------------------------------------------------
    print("\n--- My roles ---\n")

    my_roles = client.teams.roles.my_roles(team_id)
    for r in my_roles:
        print(f"  [{r.id}] {r.role_name}")

    if not my_roles:
        print("  Owner (no explicit role assigned)")

    # -----------------------------------------------------------------
    # Cleanup
    # -----------------------------------------------------------------
    print("\n--- Cleanup ---\n")

    confirm = input("  Delete the team? (y/n): ").strip().lower()
    if confirm == "y":
        try:
            client.teams.delete(team_id)
            print(f"  Team {team_id} deleted.")
        except rank.APIError as e:
            print(f"  ERROR: {e}")
    else:
        print(f"  Team {team_id} kept. You can manage it from the dashboard.")

    print("\n" + "=" * 60)
    print("  SETUP COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except rank.AuthenticationError:
        print("ERROR: Invalid or missing API key. Set RANK_API_KEY.")
    finally:
        client.close()
