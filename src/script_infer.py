import argparse
from pathlib import Path
import os
import subprocess
from typing import Literal
from logging import getLogger
import torch
from mix import mix_audio

from so_vits_svc_fork.utils import get_optimal_device

LOG = getLogger(__name__)

def infer(
    # paths
    input_path: Path,
    output_path: Path,
    model_path: Path,
    config_path: Path,
    recursive: bool,
    # svc config
    speaker: str,
    cluster_model_path: Path | None = None,
    transpose: int = 0,
    auto_predict_f0: bool = False,
    cluster_infer_ratio: float = 0,
    noise_scale: float = 0.4,
    f0_method: Literal["crepe", "crepe-tiny", "parselmouth", "dio", "harvest"] = "dio",
    # slice config
    db_thresh: int = -40,
    pad_seconds: float = 0.5,
    chunk_seconds: float = 0.5,
    absolute_thresh: bool = False,
    max_chunk_seconds: float = 40,
    device: str | torch.device = get_optimal_device(),
):
    """Inference"""
    from so_vits_svc_fork.inference.main import infer

    if not auto_predict_f0:
        LOG.warning(
            f"auto_predict_f0 = False, transpose = {transpose}. If you want to change the pitch, please set transpose."
            "Generally transpose = 0 does not work because your voice pitch and target voice pitch are different."
        )

    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}.out{input_path.suffix}"
    output_path = Path(output_path)
    if input_path.is_dir() and not recursive:
        raise ValueError(
            "input_path is a directory. Use 0re or --recursive to infer recursively."
        )
    model_path = Path(model_path)
    if model_path.is_dir():
        model_path = list(
            sorted(model_path.glob("G_*.pth"), key=lambda x: x.stat().st_mtime)
        )[-1]
        LOG.info(f"Since model_path is a directory, use {model_path}")
    config_path = Path(config_path)
    if cluster_model_path is not None:
        cluster_model_path = Path(cluster_model_path)
    infer(
        # paths
        input_path=input_path,
        output_path=output_path,
        model_path=model_path,
        config_path=config_path,
        recursive=recursive,
        # svc config
        speaker=speaker,
        cluster_model_path=cluster_model_path,
        transpose=transpose,
        auto_predict_f0=auto_predict_f0,
        cluster_infer_ratio=cluster_infer_ratio,
        noise_scale=noise_scale,
        f0_method=f0_method,
        # slice config
        db_thresh=db_thresh,
        pad_seconds=pad_seconds,
        chunk_seconds=chunk_seconds,
        absolute_thresh=absolute_thresh,
        max_chunk_seconds=max_chunk_seconds,
        device=device,
    )


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='/home/shreyan/Downloads/shreyan_voice_1min.wav', help='Path to the audio file')
parser.add_argument('-m', '--model', type=str, default='', help='Model path')
parser.add_argument('-s', '--speaker', type=str, default='shreyan', help='Speaker name')
parser.add_argument('-o', '--output', type=str, default='../files', help='output file name')

args = parser.parse_args()

infer(
    input_path=args.input,
    output_path=args.output,
    speaker=args.speaker,
    model_path=args.model,
    config_path="runs/configs/44k/config.json",
    cluster_model_path=None,
    recursive=False,
    transpose=0,
    db_thresh=-20,
    f0_method="crepe",
    auto_predict_f0=True,
    cluster_infer_ratio=0,
    noise_scale=0.4,
    pad_seconds=0.5,
    device=get_optimal_device(),
    chunk_seconds=0.5,
    absolute_thresh=False,
    max_chunk_seconds=40,
)


output_filename = Path(args.output).stem
output_filepath = args.output
song_id = '_'.join(output_filename.split('_')[1:-1])
instrumental_filename = '../TestSongs/'+f"{song_id}_ins.wav"
mix_audio(vocal_filepath=output_filepath, instrumental_filepath=instrumental_filename, output_filepath='../Converted/'+f'{output_filename}.wav')

# output_filename = 'A2B0EFE9-70F2-4D22-ACEC-42D255925547_oops_i_did_it_again_converted.wav'
# output_filepath = 'Converted/'+output_filename
# song_id = '_'.join(output_filename.split('_')[1:-1])
# instrumental_filename = 'TestSongs/'+f"{song_id}_ins.wav"
# mix_audio(vocal_filepath=output_filepath, instrumental_filepath=instrumental_filename, output_filepath='Converted/'+f'{output_filename}_mixed.wav')
