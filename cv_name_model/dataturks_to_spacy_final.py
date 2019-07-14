import json

training_data = []
lines=[]
with open('cv sliced.json', 'r') as f:
    lines = f.readlines()

for line in lines:
    data = json.loads(line)
    text = data['content']
    entities = []
    if data['annotation'] == None:
        pass
    else:
        for annotation in data['annotation']:
            #only a single point in text annotation.
            point = annotation['points'][0]
            labels = annotation['label']
            # handle both list of labels or a single label.
            if not isinstance(labels, list):
                labels = [labels]
    
            for label in labels:
                #dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                entities.append((point['start'], point['end'] + 1 ,label))
    training_data.append((text, {"entities" : entities}))