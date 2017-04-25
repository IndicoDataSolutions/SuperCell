import csv
import indicoio
from indicoio.custom import Collection

# insert your API key
indicoio.config.api_key = "YOUR_API_KEY"

def clean_article(article):
    return article.replace("\n", " ").decode('cp1252').encode('utf-8', 'replace')
    
def test_model(test_list):
    cleaned_test = [clean_article(text) for row in test_list for text in row]
    print "Articles cleaned and ready for analysis!"
    for data in cleaned_test:
        print collection.predict(data)

if __name__ == "__main__":
    # Replace "YOUR_COLLECTION_NAME" with the name you gave your dataset in CrowdLabel
    collection = Collection("YOUR_COLLECTION_NAME")

    with open('test_articles.csv', 'rU') as f:
        test_list = csv.reader(f)
        test_model(test_list)
