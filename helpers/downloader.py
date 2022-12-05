from pytube import Search
import random

class ytdownload:
    def __init__(self):
        None

    def download(self,link):
        video = link.streams.filter(file_extension="mp4").first()
        fp = video.download()
        return fp

class YT:
    def __init__(self) -> None:
        pass

    def get_mcoc_links(self):
        queries = ['mcoc', 'Marvel Contest of Champions', 'Seatin MCOC', 'Rich the man MCOC', 'Lagacy MCOC', 'ContestChampion MCOC', 'Bero Man MCOC']
        query = random.choice(queries)
        s = Search(query)
        links = []
        results = s.results
        for result in results:
            if len(links) == 10:
                break
            else:
                id = result.video_id
                link = f'//youtube.com/embed/{id}'
                links.append(link)
        return links