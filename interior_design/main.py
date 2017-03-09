import os
from tqdm import tqdm
import base64

def generate_training_data():
    d = []
    labels = []

    for root, dirs, files in os.walk("images"):
        for image in files:
            if image.endswith(".jpg") or image.endswith(".png"):

                # get file paths
                d.append(os.path.join(root, image))

                # turn filenames into labels for the images
                label = os.path.splitext(image)[0] # remove path elements from label
                l = ''.join([c for c in label if not c.isdigit()]) # remove numbers from label
                labels.append(l)

    # put images and labels into a single list to pass into the Custom Collections API
    all_data = [list(x) for x in zip(d, labels)]
    return all_data

def test_model():
    print "Test results for CONTEMPORARY category:"
    print collection.predict("test_images/contemporary-test.jpg")
    print collection.predict("test_images/contemporary-test2.jpg")
    print collection.predict("test_images/contemporary-test3.jpg")
    print "******"
    print "Test results for INDUSTRIAL category:"
    print collection.predict("test_images/industrial-test.jpg")
    print collection.predict("test_images/industrial-test2.jpg")
    print collection.predict("test_images/industrial-test3.jpg")
    print "******"
    print "Test results for MINIMALISM category:"
    print collection.predict("test_images/minimalism-test.jpg")
    print collection.predict("test_images/minimalism-test2.jpg")
    print collection.predict("test_images/minimalism-test3.jpg")

if __name__ == "__main__":
    # TODO
