# oferty/management/commands/init_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

ROLES_PERMS = {
    "student": [
        "view_user_profile",
        "change_user_profile",
        "add_offer_portal",
        "view_own_applications",
    ],
    "opiekun": [
        "view_user_profile",
        "change_user_profile",
        "view_assigned_applications",
    ],
    "pracodawca": [
        "view_user_profile",
        "change_user_profile",
        "add_offer_portal",
        "change_offer_portal",
    ],
    "pracownikBK": [
        "view_user_profile",
        "change_user_profile",
        "change_user_status",
        "view_students",
        "view_tutors",
        "view_employers",
        "add_offer_portal",
        "change_offer_portal",
        "delete_offer_portal",
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
