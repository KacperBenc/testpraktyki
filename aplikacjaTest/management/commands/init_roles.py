# oferty/management/commands/init_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

ROLES_PERMS = {
    "student": [
        "add_offer_portal",
        "view_own_applications",
    ],
    "opiekun": [
        "view_assigned_applications",
    ],
    "pracodawca": [
        "add_offer_portal",
    ],
    "pracownikBK": [
        "add_offer_portal",
        "view_students",
        "view_tutors",
        "view_employers",
    ],
}

class Command(BaseCommand):
    help = "Inicjalizacja ról i uprawnień"

    def handle(self, *args, **options):
        for role, perms in ROLES_PERMS.items():
            group, _ = Group.objects.get_or_create(name=role)
            for codename in perms:
                perm = Permission.objects.get(codename=codename)
                group.permissions.add(perm)
