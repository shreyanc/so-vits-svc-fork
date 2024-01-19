import argparse
from pathlib import Path
import os
import subprocess
from typing import Literal
from logging import getLogger


def split_audio(input_file: str, speaker_name: str, output_dir: str, segment_length: int) -> None:
    """
    Split an input audio file into multiple segments of length t and save them to the specified output directory.
    
    Args:
        input_file (str): Path to the input audio file.
        output_dir (str): Path to the output directory where the segments will be saved.
        segment_length (int): Length of each segment in seconds.
    """
    print("Splitting audio")
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        '-f', 'segment',
        '-segment_time', str(segment_length),
        '-c', 'copy',
        '-map', '0',
        '-reset_timestamps', '1',
        f'{output_dir}/{speaker_name}_%03d.wav'
    ])



def pre_resample(
    input_dir: Path,
    output_dir: Path,
    sampling_rate: int,
    n_jobs: int,
    top_db: int,
    frame_seconds: float,
    hop_seconds: float,
) -> None:
    """Preprocessing part 1: resample"""
    from so_vits_svc_fork.preprocessing.preprocess_resample import preprocess_resample

    print("Preprocessing part 1: resample")

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    preprocess_resample(
        input_dir=input_dir,
        output_dir=output_dir,
        sampling_rate=sampling_rate,
        n_jobs=n_jobs,
        top_db=top_db,
        frame_seconds=frame_seconds,
        hop_seconds=hop_seconds,
    )


def pre_config(
    input_dir: Path,
    speaker: str,
    filelist_path: Path,
    config_path: Path,
    config_type: str,
):
    """Preprocessing part 2: config"""
    from so_vits_svc_fork.preprocessing.preprocess_flist_config import preprocess_config

    print("Preprocessing part 2: config")
    input_dir = Path(input_dir)
    filelist_path = Path(filelist_path)
    config_path = Path(config_path)
    preprocess_config(
        input_dir=input_dir,
        selected_speaker=speaker,
        train_list_path=filelist_path / "train.txt",
        val_list_path=filelist_path / "val.txt",
        test_list_path=filelist_path / "test.txt",
        config_path=config_path,
        config_name=config_type,
    )


def pre_hubert(
    input_dir: Path,
    speaker: str,
    config_path: Path,
    n_jobs: bool,
    force_rebuild: bool,
    f0_method: Literal["crepe", "crepe-tiny", "parselmouth", "dio", "harvest"],
) -> None:
    """Preprocessing part 3: hubert
    If the HuBERT model is not found, it will be downloaded automatically."""
    from so_vits_svc_fork.preprocessing.preprocess_hubert_f0 import preprocess_hubert_f0
    print("Preprocessing part 3: hubert")
    input_dir = Path(input_dir)
    config_path = Path(config_path)
    preprocess_hubert_f0(
        input_dir=input_dir,
        selected_speaker=speaker,
        config_path=config_path,
        n_jobs=n_jobs,
        force_rebuild=force_rebuild,
        f0_method=f0_method,
    )


def train(
    config_path: Path,
    model_path: Path,
    tensorboard: bool = False,
    reset_optimizer: bool = False,
):
    """Train model
    If D_0.pth or G_0.pth not found, automatically download from hub."""
    from so_vits_svc_fork.train import train

    print("Training")
    config_path = Path(config_path)
    model_path = Path(model_path)

    if tensorboard:
        import webbrowser

        from tensorboard import program

        getLogger("tensorboard").setLevel(30)
        tb = program.TensorBoard()
        tb.configure(argv=[None, "--logdir", model_path.as_posix()])
        url = tb.launch()
        webbrowser.open(url)

    train(
        config_path=config_path, model_path=model_path, reset_optimizer=reset_optimizer
    )

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='/home/shreyan/Downloads/shreyan_voice_1min.wav', help='Path to the audio file')
parser.add_argument('-s', '--speaker', type=str, default='shreyan', help='Speaker name')

args = parser.parse_args()

audio_file_path = args.input
speaker_name = args.speaker

dataset_raw_dir = 'dataset_raw'
speaker_dataset_dir = f'{dataset_raw_dir}/{speaker_name}' 

os.makedirs(speaker_dataset_dir, exist_ok=True)

# Split audio
split_audio(input_file=audio_file_path, speaker_name=speaker_name, output_dir=speaker_dataset_dir, segment_length=5)

# Preprocess
pre_resample(input_dir=dataset_raw_dir,             
             output_dir="so_vits_svc_fork/dataset/44k",
             sampling_rate=44100,
             n_jobs=-1,
             top_db=30,
             frame_seconds=1,
             hop_seconds=0.3
)

pre_config(input_dir="so_vits_svc_fork/dataset/44k",
           speaker=speaker_name,
           filelist_path="so_vits_svc_fork/filelists/44k",
           config_path="so_vits_svc_fork/configs/44k/config.json",
           config_type="so-vits-svc-4.0v1"
)    

pre_hubert(input_dir="so_vits_svc_fork/dataset/44k",
           speaker=speaker_name,
           config_path="so_vits_svc_fork/configs/44k/config.json",
           n_jobs=None,
           force_rebuild=True,
           f0_method="crepe",
)

# Train
train(config_path="so_vits_svc_fork/configs/44k/config.json",
      model_path=f"so_vits_svc_fork/logs/44k/{args.speaker}",
      tensorboard=False,
      reset_optimizer=False
)
