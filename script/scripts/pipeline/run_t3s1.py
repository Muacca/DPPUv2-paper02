#!/usr/bin/env python3
"""CLI wrapper for T³×S¹ topology."""
import argparse
import os
import sys
from datetime import datetime
sys.path.insert(0, str(__file__).rsplit('scripts', 1)[0])

from dppu.topology import T3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.engine import ComputationLogger, CheckpointManager


def main():
    parser = argparse.ArgumentParser(description="DPPUv2 T³×S¹ Runner")
    parser.add_argument('--mode', required=True, choices=['AX', 'VT', 'MX'])
    parser.add_argument('--ny-variant', required=True, choices=['TT', 'REE', 'FULL'])
    parser.add_argument('--output-dir', default='output',
                        help='Output directory for log file (default: output)')
    parser.add_argument('--checkpoint-dir', default=None,
                        help='Checkpoint directory (enables checkpointing when specified)')
    args = parser.parse_args()

    mode = Mode[args.mode]
    ny_variant = NyVariant[args.ny_variant]

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(args.output_dir, f'run_t3s1_{timestamp}.log')

    logger = ComputationLogger(log_file)
    ckpt = CheckpointManager(
        args.checkpoint_dir or 'checkpoints',
        enabled=args.checkpoint_dir is not None
    )

    engine = T3S1Engine(mode, ny_variant, logger, ckpt)
    engine.run()


if __name__ == "__main__":
    main()
