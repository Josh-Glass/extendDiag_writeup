'''
Generalized Context Model (Nosofsky | from: Formal Approaches in Categorization, Pothos & Wills, 2011)
- - - - - - - - - - - - - - - - - - - - - - - - - - - 

--- Functions ---
    - forward <-- get model outputs
    - response <-- luce-choice rule (ie, softmax without exponentiation)
    - predict <-- gets class predictions
    - build_params <-- returns dictionary of weights

'''
## external requirements
import numpy as np

## minkowski pairwise distance function (https://en.wikipedia.org/wiki/Minkowski_distance)
def pdist(a1, a2, r, **kwargs):
    attention_weights = kwargs.get('attention_weights', np.ones([1,a1.shape[1]]) / a1.shape[1])

    # format inputs & exemplars for (i think vectorized) pairwise distance calculations
    a1_tiled = np.tile(a1, a2.shape[0]).reshape(a1.shape[0], a2.shape[0], a1.shape[1])
    a2_tiled = np.repeat([a2], a1.shape[0], axis=0)

    distances = np.power(
        np.sum(
            np.multiply(
                attention_weights,
                np.abs(a1_tiled - a2_tiled) ** r
            ),
            axis = 2,
        ),
        1/r
    )

    return distances


## "forward pass"
def forward(model, inputs, exemplars, c, r):

    distances = pdist(inputs, exemplars, r, attention_weights = params['attention_weights'])

    # exemplar layer activations
    hidden_activation = np.exp(
        (-c) * distances
    )
    # class predictions (luce-choiced)
    output_activation = np.matmul(
            hidden_activation,
            params['association_weights']
        )

    return [hidden_activation, output_activation]


def response(params, inputs, exemplars, c, r, phi): # softmax
    output_activation = forward(params, inputs, exemplars, c, r)[-1]
    return np.divide(
        np.exp(output_activation * phi),
      #---------#
        np.sum(
            np.exp(output_activation * phi), 
            axis=1, keepdims=True
        )
    )


def build_params(num_features, exemplar_one_hot_targets):
    '''
    num_features <-- (numeric) number of feature in the dataset
    num_categories <-- (list) 
    '''
    return {
        'attention_weights': np.ones([1, num_features]) / num_features, # <-- input -to- hidden 
        'association_weights': exemplar_one_hot_targets, # <-- hidden -to- output
    }

## predict
def predict(params, inputs, exemplars, c, r):
    return np.argmax(
        response(params, inputs, exemplars, c, r, 1),
        axis = 1
    )


## - - - - - - - - - - - - - - - - - -
## RUN MODEL
## - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    # np.random.seed(0)

    inputs = np.array([
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 0],

        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
    ])

    exemplars = inputs

    labels = [
        # 'A','A','A','A', 'B','B','B','B', # <-- type 1
        # 'A','A','B','B', 'B','B','A','A', # <-- type 2
        # 'A','A','A','B', 'B','B','B','A', # <-- type 4
        'B','A','A','B', 'A','B','B','A', # <-- type 6
    ]

    categories = np.unique(labels)
    idx_map = {category: idx for category, idx in zip(categories, range(len(categories)))}
    labels_indexed = [idx_map[label] for label in labels]
    one_hot_targets = np.eye(len(categories))[labels_indexed]

    exemplar_labels_indexed = [idx_map[label] for label in labels]
    exemplar_one_hot_targets = np.eye(len(categories))[labels_indexed]


    hps = {
        'c': 2, # <-- specificity
        'r': 1, # <-- distance metric (1: cityblock, 2: euclidean)
        'phi': 1, # <-- response mapping parameter
    }

    params = build_params(
        inputs.shape[1],  # <-- num features
        exemplar_one_hot_targets, # <-- association_strengths

    )

    p = predict(params, inputs, exemplars, hps['c'], hps['r'])
    print(p)