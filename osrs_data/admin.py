from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Quest
from .scraper import QuestScraper

class QuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'members', 'length', 'quest_points', 'series')

    actions = ['refetch_quests']

    # URL configuration for the custom button action
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('refetch/', self.admin_site.admin_view(self.refetch_quests), name='refetch_quests'),
        ]
        return custom_urls + urls

    # Add the refetch button in the changelist view
    def changelist_view(self, request, queryset=None):
        extra_context = {'refetch_url': 'refetch_quests'}

        return super().changelist_view(request, extra_context=extra_context)

    # Refetch quests logic, including scraping and rate limiting
    def refetch_quests(self, request):
        # Optional: Add rate-limiting logic here (using cache, timestamps, etc.)
        Quest.objects.all().delete()  # Clear all existing quest data

        base_url = "https://oldschool.runescape.wiki"
        quest_list_url = base_url + "/w/Quests/List"

        scraper = QuestScraper(base_url)
        scraper.scrape_difficulty_levels(quest_list_url)  # Scrape difficulty levels
        scraper.scrape_all_quests()  # Scrape quests for each difficulty

        # Save new quest data to the database
        for quest in scraper.quests_data:
            Quest.objects.create(
                difficulty=quest['difficulty'],
                name=quest['name'],
                link=quest['link'],
                members=quest['members'],
                length=quest['length'],
                quest_points=int(quest['quest_points']),
                series=quest['series']
            )

        self.message_user(request, "Quests successfully re-fetched and updated.", level=messages.SUCCESS)
        return redirect("..")  # Redirect back to the Quest list page

    refetch_quests.short_description = 'Refetch all quests from the OSRS wiki'


admin.site.register(Quest, QuestAdmin)
