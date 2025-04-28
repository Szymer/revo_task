from django.core.management.base import BaseCommand

from  sdtt.api_requester.api_call.ApiRequester import download_data


class Command(BaseCommand):
    help = "impoert revo data from the server"

    def handle(self, *args, **kwargs):
        from sdtt.revo.menagment.revo_data import RevoData

        revo_data = download_data()
        if not revo_data:
            self.stdout.write(self.style.ERROR("Failed to download Revo data."))
            return
        self.stdout.write(self.style.SUCCESS("Revo data downloaded successfully."))
        for data in revo_data:
            id = data.get("id")
            name = data.get("name")
            is_active = data.get("is_active")
            tags = data.get("tags", [])
            print (f"ID: {id}, Name: {name}, Is Active: {is_active}, tags : {tags}")
            
       