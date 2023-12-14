from keras.models import load_model
import numpy as np
from gensim.models import Word2Vec, KeyedVectors

pretrainedpath = 'word2vec/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(pretrainedpath, binary=True)

word_to_index = w2v_model.key_to_index
word_to_index = {key: value for key, value in list(word_to_index.items())[:1000000]}

print('word_to_index is done')

dict_idx = {'Happy': 0,
            'Sad': 1,
            'Laughing': 2,
            'Love': 3,
            'Cool': 4,
            'Angry': 5,
            'Thoughtful': 6,
            'Thumbs_Up': 7,
            'Confused': 8,
            'Sarcastic': 9,
            'Excited': 10,
            'Worried': 11,
            'Angelic': 12,
            'Displeased': 13,
            'Disgusted': 14,
            'Pleading': 15,
            'Fear': 16
            }

dict_emoji = {
    str(dict_idx['Happy']): ['\U0001F60A', '\U0001F607', '\U0001F600', '\U0001F618', '\U0001F496', '\U0001F970',
                             '\U0001F917'],
    str(dict_idx['Sad']): ['\U0001F622', '\U0001F62D', '\U0001F614'],
    str(dict_idx['Laughing']): ['\U0001F602', '\U0001F606', '\U0001F601', '\U0001F923'],
    str(dict_idx['Love']): ['\U0001F60D', '\U0001F618', '\U0001F496', '\U0001F970', '\U0001F60A', '\U0001F607',
                            '\U0001F600', '\U0001F917'],
    str(dict_idx['Cool']): ['\U0001F60E', '\U0001F913', '\U0001F609'],
    str(dict_idx['Angry']): ['\U0001F620', '\U0001F624', '\U0001F621'],
    str(dict_idx['Thoughtful']): ['\U0001F914', '\U0001F9D0'],
    str(dict_idx['Thumbs_Up']): ['\U0001F44D'],
    str(dict_idx['Confused']): ['\U0001F615', '\U0001F643', '\U0001F641'],
    str(dict_idx['Sarcastic']): ['\U0001F928'],
    str(dict_idx['Excited']): ['\U0001F929', '\U0001F920', '\U0001F973'],
    str(dict_idx['Worried']): ['\U0001F61F', '\U0001F628', '\U0001F629'],
    str(dict_idx['Angelic']): ['\U0001F47C'],
    str(dict_idx['Displeased']): ['\U0001F611', '\U0001F61E', '\U0001F612', '\U0001F616', '\U0001F614'],
    str(dict_idx['Disgusted']): ['\U0001F616', '\U0001F922', '\U0001F4A9', '\U0001F622'],
    str(dict_idx['Pleading']): ['\U0001F97A', '\U0001F633'],
    str(dict_idx['Fear']): ['\U0001F631', '\U0001F628', '\U0001F630', '\U0001F479', '\U0001F47B']
}


def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4).

    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this.

    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """

    # m = X.shape[0]
    m = X.shape[0]  # number of training examples

    ### START CODE HERE ###
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    # X_indices = np.zeros([m,max_len])
    X_indices = np.zeros([m, max_len])

    for i in range(m):  # loop over training examples

        # Convert the ith training sentence in lower case and split is into words. You should get a list of words.
        # sentence_words = X[i].lower().split()
        sentence_words = X[i].lower().split()

        # Initialize j to 0
        j = 0

        # Loop over the words of sentence_words

        for w in sentence_words:
            # if w exists in the word_to_index dictionary
            if w in word_to_index:
                # Set the (i,j)th entry of X_indices to the index of the correct word.
                # X_indices[i, j] = word_to_index[w]
                # print(f'row th is {i} and column is {j}')
                X_indices[i, j] = word_to_index[w]
                # Increment j to j + 1
                j = j + 1

    ### END CODE HERE ###

    return X_indices


model = load_model("model/custom_sentiment_model.h5")
print('load model is done')




def get_emoji(text):
    X_test = np.array([text])
    X_test_indices = sentences_to_indices(X_test, word_to_index, 31)
    out_arr = model.predict(X_test_indices)

    prob_distrib = []
    for i in out_arr[0]:
        prob_distrib.append(int(i * 100))
        # print(int(i*100))

    highest_number = 0
    second_highest_number = 0
    highest_number_idx = 0
    second_highest_number_idx = 0

    for i in prob_distrib:
        if i > highest_number:
            highest_number_idx = prob_distrib.index(i)
            highest_number = i

    for i in prob_distrib:
        if i > second_highest_number and i != highest_number:
            second_highest_number_idx = prob_distrib.index(i)
            second_highest_number = i
    print(f'probability distrbution is {prob_distrib}')
    print('---------------------------------------------------------------')
    print(highest_number)
    print(second_highest_number)

    emotion1 = list(dict_idx.items())[highest_number_idx][0]
    print(f'label is {highest_number_idx} representing {emotion1} emoji with {highest_number}% chance')
    emotion2 = list(dict_idx.items())[second_highest_number_idx][0]
    print(f'label is {second_highest_number_idx} representing {emotion2} emoji with {second_highest_number}% chance')
    print(f'Possible emojis for sentnce are {X_test[0]} ->')
    possible_emojis = []
    if (highest_number - second_highest_number < 60):
        for emoji in dict_emoji[str(highest_number_idx)]:
            possible_emojis.append(emoji)
        for emoji in dict_emoji[str(second_highest_number_idx)]:
            possible_emojis.append(emoji)

    else:
        for emoji in dict_emoji[str(highest_number_idx)]:
            possible_emojis.append(emoji)

    total_emoji = 1
    for emoji in possible_emojis:
        print(f'{total_emoji} {emoji} ')
        total_emoji += 1
    return possible_emojis
