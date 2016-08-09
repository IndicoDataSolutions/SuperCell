import os
from tqdm import tqdm

def generate_training_data(fname):
    """
    Read in text file and generate training data.
    Each line looks like the following:

    1050: [1, 2, 3, 4, 5]
    1349: [1, 2, 3, 4, 5]
    4160: [1, 2, 3]
    ...

    First we split on the colon of each row, where the first
    half is the image filename and the second half is its
    associated labels.
    """
    lines = open(fname).read().split("\n")

    all_shirts = []
    all_labels = []

    for line in lines:
        if not line:
    		continue

        row = line.split(":")
        shirt_name = "training_shirts/" + row[0] + ".jpg"
        shirt_name = os.path.abspath(shirt_name)

        # clean up extra punctuation marks, brackets, white space etc.
    	cleanup = row[1].replace("[", "").replace("]", "")
        labels = cleanup.split(",")
    	labels = ["label"+label.strip() for label in labels]

        for l in labels:
            all_shirts.append(shirt_name)
            all_labels.append(l)

    # put split shirts and labels into a single list to pass into the Custom Collections API
    all_data = [list(x) for x in zip(all_shirts, all_labels)]
    return all_data


if __name__ == "__main__":
    train = generate_training_data("#UPDATE")
    collection = Collection(#UPDATE)

    '''
    print collection.predict("test_shirts/9915.jpg")
    print collection.predict("test_shirts/12770.jpg")
    print collection.predict("test_shirts/13668.jpg")
    print collection.predict("test_shirts/14195.jpg")
    print collection.predict("test_shirts/11896765.jpg")
    '''
