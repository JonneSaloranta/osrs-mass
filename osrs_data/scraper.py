import requests
from bs4 import BeautifulSoup

class QuestScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.difficulty_levels = []
        self.quests_data = []

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def scrape_difficulty_levels(self, url):
        """Scrape the quest difficulty levels and their links."""
        soup = self.get_soup(url)
        difficulty_table = soup.find('table', {'class': 'wikitable'})

        for row in difficulty_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) > 1:
                difficulty_name = cells[1].find('a').text
                difficulty_link = cells[1].find('a')['href']
                self.difficulty_levels.append({
                    'name': difficulty_name,
                    'link': f"{self.base_url}{difficulty_link}"
                })

    def scrape_quests_for_difficulty(self, difficulty):
        """Scrape all quests for a given difficulty level."""
        difficulty_name = difficulty['name']
        difficulty_link = difficulty['link']
        soup = self.get_soup(difficulty_link)

        quest_table = soup.find('table', {'class': 'wikitable qc-active sortable lighttable autosort=1,a'})
        
        if quest_table:
            for row in quest_table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) > 1:
                    quest_name = cells[0].find('a').text.strip() if cells[0].find('a') else cells[0].text.strip()
                    quest_link = cells[0].find('a')['href'] if cells[0].find('a') else None
                    members = cells[1].text.strip()
                    length = cells[2].text.strip()
                    quest_points = cells[3].text.strip()
                    series = cells[4].text.strip().split(",")[0]

            
                    self.quests_data.append({
                        'difficulty': difficulty_name,
                        'name': quest_name,
                        'link': f"{self.base_url}{quest_link}" if quest_link else "N/A",
                        'members': members,
                        'length': length,
                        'quest_points': quest_points,
                        'series': series
                    })

    def scrape_all_quests(self):
        """Scrape quests from all difficulty levels."""
        for difficulty in self.difficulty_levels:
            self.scrape_quests_for_difficulty(difficulty)

    def print_quests_data(self):
        """Print the scraped quest data."""
        for quest in self.quests_data:
            print(f"Difficulty: {quest['difficulty']}")
            print(f"Quest Name: {quest['name']}")
            print(f"Link: {quest['link']}")
            print(f"Members: {quest['members']}")
            print(f"Length: {quest['length']}")
            print(f"Quest Points: {quest['quest_points']}")
            print(f"Series: {quest['series']}")
            print("-" * 50)

def main():
    base_url = "https://oldschool.runescape.wiki"
    quest_list_url = base_url + "/w/Quests/List"

    scraper = QuestScraper(base_url)
    scraper.scrape_difficulty_levels(quest_list_url)
    scraper.scrape_all_quests()
    scraper.print_quests_data()

if __name__ == "__main__":
    main()
