import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Article:
    def __init__(self, headline, date, authors):
        self.headline = headline
        self.date = date
        self.authors = authors
        self.quarter = self.quarter_place()
    
    def quarter_place(self):
        for _, quarter in all_quarters[self.date.year].items():
            if quarter.start <= self.date <= quarter.end:
                quarter.add_article(self)
                return quarter
        for _, quarter in all_quarters[self.date.year + 1].items():
            if quarter.start <= self.date <= quarter.end:
                quarter.add_article(self)
                return quarter

class Author:
    def __init__(self, name):
        self.name = name
        self.articles = []
        self.quarters = []
        
    def add_article(self, article):
        self.articles.append(article)

            
    def add_quarter(self, quarter):
        self.quarters.append(quarter)

class Quarter:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.articles = []
        self.authors = []
    
    def add_article(self, article):
        self.articles.append(article)
    
    def add_author(self, author):
        self.authors.append(author)
    


all_quarters = {2000: {}}
all_articles = []
all_authors = {}
with open("quarterdates.txt", "r") as file:
    lines = file.readlines()
    for i in range(0, len(lines), 6):
        year = int(lines[i].rstrip()[:4])
        all_quarters[year + 1] = {}
        

        start = lines[i + 1].split("  ")[0]
        date_with_year = f"{start}, {year}"
        date_obj = datetime.strptime(date_with_year, "%A, %B %d, %Y")
        u_end = date_obj

        start = lines[i + 2].split("  ")[0]
        date_with_year = f"{start}, {year}"
        date_obj = datetime.strptime(date_with_year, "%A, %B %d, %Y")
        a_end = date_obj
        all_quarters[year]["autumn"] = Quarter("autumn", u_end + timedelta(days=1), a_end)

        start = lines[i + 3].split("  ")[0]
        date_with_year = f"{start}, {year + 1}"
        date_obj = datetime.strptime(date_with_year, "%A, %B %d, %Y")
        w_end = date_obj
        all_quarters[year + 1]["winter"] = Quarter("winter", a_end + timedelta(days=1), w_end)

        start = lines[i + 4].split("  ")[0]
        date_with_year = f"{start}, {year + 1}"
        date_obj = datetime.strptime(date_with_year, "%A, %B %d, %Y")
        s_end = date_obj
        all_quarters[year + 1]["spring"] = Quarter("spring", w_end + timedelta(days=1), s_end)

        try:
            start = lines[i + 7].split("  ")[0]
            date_with_year = f"{start}, {year + 1}"
            date_obj = datetime.strptime(date_with_year, "%A, %B %d, %Y")
            u_end = date_obj
            all_quarters[year + 1]["summer"] = Quarter("summer", s_end + timedelta(days=1), u_end)
        except:
            pass

data_lines = []
with open("data.txt", "r") as file:
    data_lines = file.readlines()

for i, line in enumerate(data_lines):
    if "By" and " / " in line:
       if len(line) < 200:
            byline = data_lines[i].rstrip().split("/")
            authors = re.split(r'\s*(?: And |,)\s*', byline[0], flags=re.IGNORECASE)
            authors = [author.replace("By ", "").replace(",", "").replace("and", "").strip() for author in authors]
            date_obj = datetime.strptime(byline[1].strip(), "%B %d, %Y")
            headline = data_lines[i - 1].rstrip()
            current_article = Article(headline, date_obj, authors)
            all_articles.append(current_article)
            for author in authors:
                if author not in all_authors:
                    all_authors[author] = Author(author)
                all_authors[author].add_article(current_article)
                all_authors[author].add_quarter(current_article.quarter)
            
                


labels = []
counts = []
for year, quarters in all_quarters.items():
    for name, quarter in quarters.items():
        print(f"{name.capitalize()} {year}, {len(quarter.articles)} articles")
        labels.append(f"{name.capitalize()} {year}")
        counts.append(len(quarter.articles))

# plt.figure(figsize=(18, 6))
# plt.plot(labels[2:-1], counts[2:-1], marker='o', linestyle='-', color='maroon')
# plt.title('# of Articles Written Each Quarter')
# plt.xlabel('Quarter')
# plt.ylabel('Articles')
# plt.xticks(rotation=90, fontsize=10)
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# for name, author in all_authors.items():
#     author_count.append([name, len(author.articles)])
    