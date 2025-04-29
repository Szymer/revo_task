import os
from django.core.management.base import BaseCommand
from  api_requester.api_call.api_call import ApiRequester


class Command(BaseCommand):
    help = "impoert revo data from the server"

    def handle(self, *args, **kwargs):
        endpoint = os.getenv('REVO_ENDPIONT', 'revo')  # Replace with your actual endpoint
        # Initialize the API requester
        api_requester = ApiRequester()
        revo_data = api_requester.download_data(endpoint=endpoint)
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
            
       