import wikipediaapi
from speak import Speak


def get_final(page, about=None):
    if "may refer to" in page.summary:
#        if len(page.links) > 0:
        topics = list(page.links.keys())
        if len(topics) > 0:
            h=0
            Speak(f"This is many topics about {about}")
            for topic in topics:
                if page.exists():
                    hasil = page.links[list(page.links.keys())[h]]
                    if "ns: 0" in str(hasil):
                        print(f"""
>>>>>>>>>>>>>>>>>>>>>>>>>>>
Title : {topic}
{hasil.summary}
>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")
                        h+=1
                else:
                    print("Page for", topic, "does not exist.")

        else:
            Speak("No specific topics found in disambiguation page.")
            return True
    else:
        first_topic = page
        if len(list(first_topic.links.keys())) < 40:
            Speak(first_topic.summary)
            return True
        else:
            print(f"""
>>>>>>>>>>>>>>>>>>>>>>>>>>>
Title : {first_topic.title}
>>>>>>>>>>>>>>>>>>>>>>>>>>>
{first_topic.summary}
>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")
            return False

def get_wikipedia_summary(query):
    wiki_wiki = wikipediaapi.Wikipedia('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

    pages = wiki_wiki.page(query)
    if pages.exists():
        get_final(pages, about=query)
    else:
        no = 1
        while True:
            try:
                topic = query.split()[no:]
                topic = ' '.join(topic)
                again_pages = wiki_wiki.page(topic)
                if again_pages.exists():
                    get_final(again_pages, about=topic)
                    break
                else:
                    no+=1
                    continue
            
            except:
                Speak("Sorry, the topic doesn't exist on Wikipedia, please check keyword to be correct")
                return True
                break
            
def Wiki(sentence):
    topic = sentence.replace("?", "").split()[3:]
    topic = ' '.join(topic)
    get_wikipedia_summary(topic)

