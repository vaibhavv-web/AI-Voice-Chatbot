from duckduckgo_search import DDGS

def web_search(query):

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)

    output = ""

    for r in results:
        output += r["title"] + "\n" + r["body"] + "\n\n"

    return output