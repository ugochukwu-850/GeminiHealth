from django.core.management.base import BaseCommand, CommandError
from api.models import Ingredients, Allergy

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("model", nargs=1, type=str, choices=["ingredients"], help="Generates and populates the data in that module with the expected data")

    def handle(self, *args, **options):
        if options["model"][0] == "ingredients":
            
            Ingredients.populate()
            
            self.stdout.write(
                self.style.SUCCESS('Successfully populated the  model "%s"' % options["model"])
            )