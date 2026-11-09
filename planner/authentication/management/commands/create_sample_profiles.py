from pathlib import Path
import secrets

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from authentication.models import Profile, RoleChoices, TechChoices


SAMPLE_PROFILES = [
    ("Maya", "Nair", "maya.nair", RoleChoices.PROJECT_COORDINATOR, None),
    ("Ethan", "Brooks", "ethan.brooks", RoleChoices.PROJECT_COORDINATOR, None),
    ("Aisha", "Rahman", "aisha.rahman", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Lucas", "Bennett", "lucas.bennett", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Sofia", "Chen", "sofia.chen", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Arjun", "Menon", "arjun.menon", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Chloe", "Martin", "chloe.martin", RoleChoices.DEVELOPER, TechChoices.TESTER),
    ("Noah", "Patel", "noah.patel", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Zara", "Wilson", "zara.wilson", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Daniel", "Kim", "daniel.kim", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Priya", "Shah", "priya.shah", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Oliver", "Reed", "oliver.reed", RoleChoices.DEVELOPER, TechChoices.TESTER),
    ("Fatima", "Ali", "fatima.ali", RoleChoices.DEVELOPER, TechChoices.FRONTEND),
    ("Leo", "Garcia", "leo.garcia", RoleChoices.DEVELOPER, TechChoices.BACKEND),
    ("Ananya", "Rao", "ananya.rao", RoleChoices.DEVELOPER, TechChoices.FULLSTACK),
    ("Grace", "Thompson", "grace.thompson", RoleChoices.DEVELOPER, TechChoices.UIUX),
    ("Mateo", "Rivera", "mateo.rivera", RoleChoices.DEVELOPER, TechChoices.TESTER),
]


class Command(BaseCommand):
    help = "Create 2 sample coordinators and 15 sample developers with credentials in Downloads."

    def handle(self, *args, **options):
        downloads_dir = Path.home() / "Downloads"
        credentials_path = downloads_dir / "credentials.txt"
        if credentials_path.exists():
            raise CommandError(
                f"Refusing to overwrite existing credentials file: {credentials_path}"
            )

        usernames = [profile[2] for profile in SAMPLE_PROFILES]
        existing_usernames = set(
            Profile.objects.filter(username__in=usernames).values_list("username", flat=True)
        )
        if existing_usernames:
            raise CommandError(
                "Sample profiles already exist for: "
                + ", ".join(sorted(existing_usernames))
                + ". No accounts were changed."
            )

        generated = []
        used_emails = set()
        for first_name, last_name, username, role, tech in SAMPLE_PROFILES:
            email_name = f"{first_name}{last_name}".lower()
            while True:
                email = f"{email_name}{secrets.randbelow(900000) + 100000}@maillinator.com"
                if email not in used_emails and not Profile.objects.filter(email=email).exists():
                    used_emails.add(email)
                    break

            generated.append(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "password": secrets.token_urlsafe(18),
                    "role": role,
                    "tech": tech,
                }
            )

        lines = [
            "Sample Project Planner credentials",
            "These are fictional development accounts. Change passwords before any shared use.",
            "",
            "Name | Role | Technology | Username | Email | Password",
        ]
        lines.extend(
            " | ".join(
                (
                    f"{account['first_name']} {account['last_name']}",
                    account["role"],
                    account["tech"] or "N/A",
                    account["username"],
                    account["email"],
                    account["password"],
                )
            )
            for account in generated
        )

        downloads_dir.mkdir(parents=True, exist_ok=True)
        with transaction.atomic():
            for account in generated:
                Profile.objects.create_user(
                    username=account["username"],
                    email=account["email"],
                    password=account["password"],
                    first_name=account["first_name"],
                    last_name=account["last_name"],
                    role=account["role"],
                    tech=account["tech"],
                )
            credentials_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(generated)} profiles and saved credentials to {credentials_path}"
            )
        )
