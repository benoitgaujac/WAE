import os
from datetime import datetime
import logging
import argparse
import configs
from train import Run
from datahandler import DataHandler
import utils

import tensorflow as tf
tf.compat.v1.disable_eager_execution()
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
import pdb

parser = argparse.ArgumentParser()
# Dir setup
parser.add_argument("--data_dir", type=str,
                    help='directory in which data is stored')
parser.add_argument("--out_dir", type=str, default='code_outputs',
                    help='root_directory in which outputs are saved')
parser.add_argument("--res_dir", type=str, default='res',
                    help='directory in which exp. res are saved')
# Exp setup
parser.add_argument("--dataset", default='mnist',
                    help='dataset')
parser.add_argument("--mode", default='train',
                    help='mode to run [train/test/vizu]')
parser.add_argument("--num_it", type=int, default=300000,
                    help='iteration number')
parser.add_argument("--lr", type=float,
                    help='learning rate size')
# Model setup
parser.add_argument("--model", default='WAE',
                    help='model to train [WAE/BetaVAE/...]')
parser.add_argument("--cost", default='l2sq',
                    help='wae ground cost [l2/l2sq/l1]')
parser.add_argument("--id", type=int,
                    help='id exp')
parser.add_argument("--decoder", default='bernoulli',
                    help='decoder type for VAE [gauss/bernoulli]')
parser.add_argument("--net_archi", default='mlp',
                    help='networks architecture [mlp/conv]')
# Savings
parser.add_argument('--save_model', action='store_false', default=True,
                    help='save final model weights [True/False]')
parser.add_argument("--save_data", action='store_false', default=True,
                    help='save training data')
parser.add_argument("--weights_file")


FLAGS = parser.parse_args()


def main():

    # dataset config
    if FLAGS.dataset == 'mnist':
        opts = configs.config_mnist
    elif FLAGS.dataset == 'svhn':
        opts = configs.config_svhn
    else:
        assert False, 'Unknown dataset'
    if FLAGS.data_dir:
        opts['data_dir'] = FLAGS.data_dir
    else:
        raise Exception('You must provide a data_dir')

    # Model set up
    opts['model'] = FLAGS.model
    opts['cost'] = FLAGS.cost
    betas = [0,1,5,10,15,25,50,75,100]
    coef_id = (FLAGS.id-1) % len(betas)
    opts['beta'] = betas[coef_id]
    opts['decoder'] = FLAGS.decoder
    opts['net_archi'] = FLAGS.net_archi

    # Create directories
    results_dir = 'results'
    if not tf.io.gfile.isdir(results_dir):
        utils.create_dir(results_dir)
    opts['out_dir'] = os.path.join(results_dir,FLAGS.out_dir)
    if not tf.io.gfile.isdir(opts['out_dir']):
        utils.create_dir(opts['out_dir'])
    out_subdir = os.path.join(opts['out_dir'], opts['model'])
    if not tf.io.gfile.isdir(out_subdir):
        utils.create_dir(out_subdir)
    exp_dir = os.path.join(out_subdir,
                           '{}_{}_{:%Y_%m_%d_%H_%M}'.format(
                                FLAGS.res_dir,
                                opts['beta'],
                                datetime.now()), )
    opts['exp_dir'] = exp_dir
    if not tf.io.gfile.isdir(exp_dir):
        utils.create_dir(exp_dir)
        utils.create_dir(os.path.join(exp_dir, 'checkpoints'))

    # Verbose
    logging.basicConfig(filename=os.path.join(opts['exp_dir'],'outputs.log'),
        level=logging.INFO, format='%(asctime)s - %(message)s')

    # Experiemnts set up
    opts['lr'] = FLAGS.lr
    opts['it_num'] = FLAGS.num_it
    opts['print_every'] = int(opts['it_num'] / 2.)
    opts['evaluate_every'] = int(opts['it_num'] / 4.)
    opts['save_every'] = 10000000000
    opts['save_final'] = FLAGS.save_model
    opts['save_train_data'] = FLAGS.save_data

    #Reset tf graph
    tf.reset_default_graph()

    # Loading the dataset
    data = DataHandler(opts)
    assert data.train_size >= opts['batch_size'], 'Training set too small'

    # inti method
    run = Run(opts, data)

    # Training/testing/vizu
    if FLAGS.mode=="train":
        # Dumping all the configs to the text file
        with utils.o_gfile((exp_dir, 'params.txt'), 'w') as text:
            text.write('Parameters:\n')
            for key in opts:
                text.write('%s : %s\n' % (key, opts[key]))
        run.train()
    else:
        assert False, 'Unknown mode %s' % FLAGS.mode


main()