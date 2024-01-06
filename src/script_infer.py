import argparse
from pathlib import Path
import os
import subprocess
from typing import Literal
from logging import getLogger
import torch

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


infer(
    input_path="path_to_input_file",
    output_path=None,
    speaker='mark_cuban_5min',
    model_path="so_vits_svc_fork/configs/44k/",
    config_path="so_vits_svc_fork/configs/44k/config.json",
    cluster_model_path=None,
    recursive=False,
    transpose=0,
    db_thresh=-20,
    f0_method="dio",
    auto_predict_f0=True,
    cluster_infer_ratio=0,
    noise_scale=0.4,
    pad_seconds=0.5,
    device=get_optimal_device(),
    chunk_seconds=0.5,
    absolute_thresh=False,
    max_chunk_seconds=40,
)