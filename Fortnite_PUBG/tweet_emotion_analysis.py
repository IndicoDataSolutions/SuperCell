# imports
import json
import re
from tqdm import tqdm
import indicoio
import pandas as pd

indicoio.config.api_key = "YOUR_API_KEY"


# We are simply taking the emotion with the highest score
def get_emotion_results(tweet_text_array):
    parsed_sentiment = []
    raw_results = indicoio.emotion(tweet_text_array, top_n=1)
    for result in raw_results:
        field, value = result.items()[0]
        parsed_sentiment.append(field)
    return parsed_sentiment


# Again, we take the detected language with the highest score
def get_language_results(tweet_text_array):
    parsed_languages = []
    raw_results = indicoio.language(tweet_text_array, top_n=1)
    for result in raw_results:
        field, value = result.items()[0]
        parsed_languages.append(field)
    return parsed_languages


if __name__ == "__main__":
    filename = "tweets.json"
    path = "data/"

    tweet_dict_list = json.load(open(path+filename))
    list_size = len(tweet_dict_list)
    batch_size = 20  # It's recommended to limit batch sizes to 20 items or less

    # Aggregators for data parsed from CSV
    analysed_items_url = []  # Use as unique ID to pivot on
    analysed_items_timestamp = []
    analyzed_items_text = []
    analysed_items_user_lang = []
    engagement_retweets = []
    engagement_likes = []

    # Aggregators for indico API results
    language_results = []
    sentiment_results = []
    emotion_results = []

    for batch_start in tqdm(range(0, list_size, batch_size)):
        batch_end = batch_start + batch_size if batch_start + batch_size < list_size else list_size - 1
        batch = tweet_dict_list[batch_start:batch_end]
        batch_text = []
        batch_timestamps = []
        batch_urls = []
        batch_likes = []
        batch_retweets = []
        batch_user_lang = []

        for tweet_item in batch:
            u_language = re.search(r"lang=....", tweet_item["html"]).group()
            u_language_raw = u_language.replace("lang=", " ").replace("\"", " ").strip()

            # English based responses work best with the sentiment and emotion APIs.
            if u_language_raw == "en":
                batch_text.append(tweet_item["text"])
                batch_timestamps.append(tweet_item["timestamp"])
                batch_urls.append(tweet_item["url"])
                batch_likes.append(tweet_item["likes"])
                batch_retweets.append(tweet_item["retweets"])
                batch_user_lang.append(u_language_raw)

        try:
            # We attempt to get the API responses first, if that fails, the batch is skipped.
            sentiment_results.extend(indicoio.sentiment_hq(batch_text))
            emotion_results.extend(get_emotion_results(batch_text))
            language_results.extend(get_language_results(batch_text))

            analysed_items_timestamp.extend(batch_timestamps)
            analyzed_items_text.extend(batch_text)
            analysed_items_user_lang.extend(batch_user_lang)
            analysed_items_url.extend(batch_urls)
            engagement_likes.extend(batch_likes)
            engagement_retweets.extend(batch_retweets)

        except indicoio.IndicoError as e:
            print("Analysis failed at: %i" % batch_start)
            pass

    df = pd.DataFrame()
    df['date'] = analysed_items_timestamp
    df['url'] = analysed_items_url
    df['text'] = analyzed_items_text
    df['likes'] = engagement_likes
    df['shares'] = engagement_retweets
    df['lang_user'] = analysed_items_user_lang
    df['lang_detected'] = language_results
    df['sentiment'] = sentiment_results
    df['emotion'] = emotion_results
    df.to_csv('emotion_results.csv', encoding='utf-8-sig')
