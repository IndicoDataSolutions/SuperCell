import os
from operator import itemgetter

from indicoio.custom import Collection

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
    with open(fname, "rb") as f:
        for line in f:
            shirt, targets = line.split(":")
            shirt_path = "training_shirts/{image}.jpg".format(
                image=shirt.strip()
            )
            shirt_path = os.path.abspath(shirt_path)

            # parse out the list of targets
            target_list = targets.strip()[1:-1].split(",")
            labels = map(lambda target: "label" + target.strip(), target_list)
            yield [ (shirt_path, label) for label in labels]
    raise StopIteration


if __name__ == "__main__":
    collection = Collection("clothes_collection_1")

    # Clear any previous changes
    try:
        collection.clear()
    except:
        pass

    train = generate_training_data("clothes_match_labeled_data_1.txt")

    total = 0
    for samples in train:
        print "Adding {num} samples to collection".format(num=len(samples))
        collection.add_data(samples)
        total += len(samples)
        print "Added {total} samples to collection thus far".format(total=total)

    collection.train()
    collection.wait()

    sort_key = itemgetter(1)
    print sorted(collection.predict("test_shirts/9915.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/12770.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/13668.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/14195.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/11896765.jpg").items(), key=sort_key)
