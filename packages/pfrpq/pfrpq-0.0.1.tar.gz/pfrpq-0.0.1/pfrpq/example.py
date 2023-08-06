
import warnings
import argparse
from lib import get_model, get_score

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

parser = argparse.ArgumentParser(
    description='Pairwise FR IQA Metric')


parser.add_argument('input_path', type=str,
                    help=(
                        'Path to input image'
                    )
                    )
parser.add_argument('reference_path', type=str,
        help=(
            'Path to reference image'
        )
        )
parser.add_argument('gt_path', type=str,
        help=(
            'Path to Groud Truth image'
        )
        )

parser.add_argument('--ckpt_path', type=str, default='epoch=43-step=21296.ckpt',
                    help='Path to ckpt with weights.'
                    )

args=parser.parse_args()

model=get_model(args.ckpt_path)

print('Metric value:', get_score(args.input_path, args.reference_path, args.gt_path, model))
