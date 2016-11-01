import indicoio
import csv

indicoio.config.api_key = 'afa48345219e962d108bbd173b100111'

def clean_article(article):
    return article.replace("\n", " ").decode('cp1252').encode('utf-8', 'replace')

def clean_articles(article_list):
    # data processing: clean up new lines and convert strings into utf-8 so the indico API can read the data
    # put all articles into a list for easy batch processing
    cleaned_articles = [clean_article(text) for row in article_list for text in row]
    print "Articles cleaned and ready for batch processing!"
    return cleaned_articles

def get_summary(cleaned_articles):
    # get article summaries
    summary = [indicoio.summarization(item) for item in cleaned_articles]
    # clean up result for easy readability
    print "Here are the summaries for all %d articles:" % (len(summary))
    for line in summary:
        print "\n" + " ".join(line)

if __name__ == "__main__":
    with open('articles.csv', 'rU') as f:
        article_list = csv.reader(f)
        cleaned_articles = clean_articles(article_list)
        get_summary(cleaned_articles)
