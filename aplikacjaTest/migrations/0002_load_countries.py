from django.db import migrations

def load_countries(apps, schema_editor):
    Kraj = apps.get_model("aplikacjaTest", "Kraj")

    kraje = [
        "Polska",
        "Niemcy",
        "Czechy",
        "Słowacja",
        "Ukraina",
        "Litwa",
        "Łotwa",
        "Estonia",
        "Francja",
        "Włochy",
        "Hiszpania",
        "Portugalia",
        "Norwegia",
        "Szwecja",
        "Finlandia",
        "Dania",
        "Belgia",
        "Holandia",
        "Szwajcaria",
        "Austria",
        "Wielka Brytania",
        "Irlandia",
        "USA",
        "Kanada",
    ]

    for kraj in kraje:
        Kraj.objects.get_or_create(nazwa=kraj)

    Miasto = apps.get_model("aplikacjaTest", "Miasto")

    startowe_miasta = ["Kraków", "Gdańsk", "Wrocław", "Poznań"]

    for m in startowe_miasta:
        Miasto.objects.update_or_create(nazwa=m, defaults={})

def unload_countries(apps, schema_editor):
    Kraj = apps.get_model("aplikacjaTest", "Kraj")
    Kraj.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ("aplikacjaTest", "0001_initial"),  # ← zmień na ostatnią migrację
    ]

    operations = [
        migrations.RunPython(load_countries, unload_countries),
    ]