import copy
from math import pow, sqrt, cos, sin, pi

### Default common config
config = {}
# Outputs set up
config['verbose'] = False
config['save_every'] = 1000
config['save_final'] = True
config['save_train_data'] = True
config['print_every'] = 100
config['evaluate_every'] = int(config['print_every'] / 2)
config['embedding'] = 'umap' #vizualisation method of the embeddings: pca, umap
config['out_dir'] = 'code_outputs'
config['plot_num_pics'] = 100
config['plot_num_cols'] = 10
# Experiment set up
config['train_dataset_size'] = -1
config['batch_size'] = 100
config['use_trained'] = False #train from pre-trained model
config['e_pretrain'] = False #pretrained the encoder parameters
config['e_pretrain_sample_size'] = 200
# Opt set up
config['optimizer'] = 'adam' # adam, sgd
config['adam_beta1'] = 0.9
config['adam_beta2'] = 0.999
config['lr'] = 0.0001
config['lr_adv'] = 1e-08
config['lr_decay'] = False
config['normalization'] = 'batchnorm' #batchnorm, layernorm, none
config['batch_norm_eps'] = 1e-05
config['batch_norm_momentum'] = 0.99
config['dropout_rate'] = 1.
# Objective set up
config['model'] = 'WAE' #WAE, BetaVAE
config['cost'] = 'l2sq' #l2, l2sq, l2sq_norm, l1, xentropy
config['mmd_kernel'] = 'IMQ' # RBF, IMQ
# Model set up
config['zdim'] = 2
config['nmixtures'] = 10
config['pz_scale'] = 1.
config['decoder'] = 'bernoulli' #bernoulli, gauss
# config['sigma_prior'] = sqrt((1-cos(pi/5.))**2 + sin(pi/5.)**2) / 4. # to check
config['sigma_prior'] = .1
config['pz_scale'] = 1.
# NN set up
config['net_archi'] = 'mlp' #mlp. conv
config['init_std'] = 0.099999
config['init_bias'] = 0.0
config['mlp_init'] = 'glorot_uniform' #normal, he, glorot, glorot_he, glorot_uniform, ('uniform', range)
config['conv_init'] = 'glorot_uniform' #he, glorot, normilized_glorot, truncated_norm

# MNIST config
config_mnist = config.copy()
# Data set up
config_mnist['dataset'] = 'mnist'
config_mnist['data_dir'] = 'mnist'
config_mnist['nclasses'] = 10

# SVHN config
config_SVHN = config.copy()
# Data set up
config_SVHN['dataset'] = 'svhn'
config_SVHN['data_dir'] = 'svhn'
config_SVHN['nclasses'] = 10
