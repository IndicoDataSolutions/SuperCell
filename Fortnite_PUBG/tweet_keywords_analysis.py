# imports
import json
import re
from tqdm import tqdm
import indicoio
import pandas as pd

indicoio.config.api_key = "YOUR_API_KEY"


def get_keywords_results(tweet_text_array):
    parsed_keywords = []
    raw_results = indicoio.keywords(tweet_text_array)
    for item_result in raw_results:
        tweet_keywords = []
        for keyword, score in item_result.items():
            tweet_keywords.append(keyword)
        parsed_keywords.append(tweet_keywords)
    return parsed_keywords


if __name__ == "__main__":
    # Initiate variables
    filename = "tweets.json"
    path = "data/"

    tweet_dict_list = json.load(open(path+filename))
    list_size = len(tweet_dict_list)
    job_size = list_size
    job_start = 0
    batch_size = 20

    analysed_items_url = []  # ID to pivot on
    analysed_items_timestamp = []
    analyzed_items_text = []
    analyzed_items_keywords = []
    keywords_results = []

    for batch_start in tqdm(range(job_start, job_size, batch_size)):
        batch_end = batch_start + batch_size if batch_start + batch_size < list_size else list_size - 1
        batch = tweet_dict_list[batch_start:batch_end]
        batch_text = []
        batch_timestamps = []
        batch_urls = []

        for tweet_item in batch:
            u_language = re.search(r"lang=....", tweet_item["html"]).group()
            u_language_raw = u_language.replace("lang=", " ").replace("\"", " ").strip()

            if u_language_raw == "en":
                batch_text.append(tweet_item["text"])
                batch_timestamps.append(tweet_item["timestamp"])
                batch_urls.append(tweet_item["url"])

        try:
            keywords_results.extend(get_keywords_results(batch_text))
            analysed_items_timestamp.extend(batch_timestamps)
            analyzed_items_text.extend(batch_text)
            analysed_items_url.extend(batch_urls)

        except Exception:
            print("Analysis failed at: %i" % batch_start)
            pass

    df = pd.DataFrame()
    df['date'] = analysed_items_timestamp
    df['url'] = analysed_items_url
    df['text'] = analyzed_items_text
    df['keywords'] = keywords_results
    df.to_csv('keywords_results.csv', encoding='utf-8-sig')
