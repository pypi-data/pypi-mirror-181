def proportional_train_validation_split(data: list, validation_size: float, classes: list, random_state: int = 0):
    """Splits data into two lists named train and validation, and validation has 'validation_size' records of the total records in data per class."""
    import copy, random, math
    classList = copy.deepcopy(classes)
    random.seed(random_state)
    random.shuffle(classList)
    validation = []
    for name in classList:
        objs = [obj for obj in data if obj["name"] == name]
        filenames = list(set(obj["filename"] for obj in objs))
        sample_size = math.ceil(validation_size * float(len(filenames)))
        filenames = random.sample(filenames, k=sample_size)
        for obj in [obj for obj in data if obj["filename"] in filenames]:
            validation.append(obj)
        data = [obj for obj in data if not obj["filename"] in filenames]
    return data, validation