import sys
import time
import os
import numpy as np

import scipy.stats as scistats


def accuracy(labels, probs, clusters_id=None):
    preds = np.argmax(probs,axis=-1)
    if clusters_id is not None:
        relabelled_preds = np.choose(preds,clusters_id)
        correct_prediction = (relabelled_preds==labels)
    else:
        correct_prediction = (preds==labels)
    return np.mean(correct_prediction)

def get_mean_probs(opts,labels,probs):
    mean_probs = []
    num_pics = np.shape(probs)[0]
    for k in range(opts['nclasses']):
        prob = [probs[n] for n in range(num_pics) if labels[n]==k]
        # if len(prob)==0:
        #     pdb.set_trace()
        # if prob==[]:
        #     prob = np.zeros(np.shape(probs)[1])
        # else:
        #     prob = np.mean(np.stack(prob,axis=0),axis=0)
        prob = np.mean(np.stack(prob,axis=0),axis=0)
        mean_probs.append(prob)
    mean_probs = np.stack(mean_probs,axis=0) #[nclasses, nmixtures]
    return mean_probs

    # cluster_to_digit = relabelling_mask_from_probs(mean_probs)
    # return cluster_to_digit

def relabelling_mask_from_probs(opts, mean_probs):
    if opts['nmixtures']>1:
        assert opts['nmixtures']>=opts['nclasses'],\
        'Need more mixtures than classes to make accuracy'
        probs_copy = mean_probs.copy()
        k_vals = []
        min_prob = np.zeros(opts['nmixtures'])
        mask = np.arange(opts['nmixtures'])
        while np.amax(probs_copy) > 0.:
            max_probs = np.amax(probs_copy,axis=-1)
            digit_idx = np.argmax(max_probs)
            k_val_sort = np.argsort(probs_copy[digit_idx])
            i = -1
            k_val = k_val_sort[i]
            while k_val in k_vals:
                i -= 1
                if i < -opts['nclasses']:
                    break
                k_val = k_val_sort[i]
            k_vals.append(k_val)
            mask[k_val] = digit_idx
            probs_copy[digit_idx] = min_prob
        return mask
    else:
        return np.arange(opts['nmixtures'])

def relabelling_mask_from_entropy(opts, mean_probs, entropies):
    k_vals = []
    max_entropy_state = np.ones(len(entropies))/len(entropies)
    max_entropy = scistats.entropy(max_entropy_state)
    mask = np.arange(opts['nmixtures'])
    while np.amin(entropies) < max_entropy:
        digit_idx = np.argmin(entropies)
        k_val_sort = np.argsort(mean_probs[digit_idx])
        i = -1
        k_val = k_val_sort[i]
        while k_val in k_vals:
            i -= 1
            k_val = k_val_sort[i]
        k_vals.append(k_val)
        mask[k_val] = digit_idx
        entropies[digit_idx] = max_entropy
    return mask

def calculate_row_entropy(mean_probs):
    entropies = []
    for i in range(np.shape(mean_probs)[0]):
        entropies.append(scistats.entropy(mean_probs[i]))
    entropies = np.asarray(entropies)
    return entropies

def one_hot(labels,depth=10):
    one_hot = np.zeros((labels.size, 10))
    one_hot[np.arange(labels.size),labels] = 1
    return one_hot
