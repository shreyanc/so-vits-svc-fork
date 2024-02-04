import librosa
import soundfile as sf
import numpy as np
import pydub
import pyloudnorm as pyln


# def compress(audio_filepath, output_filepath, threshold=-20, ratio=4, attack=10, release=100):
#     # Load the audio track
#     audio = pydub.AudioSegment.from_file(audio_filepath)

#     # Apply compression
#     compressed = audio.compress_threshold(threshold, ratio, attack, release)

#     # Export the compressed audio to the output filepath
#     compressed.export(output_filepath, format="wav")


def mix_audio(vocal_filepath, instrumental_filepath, output_filepath):
    vocal, sr_vocal = librosa.load(vocal_filepath, sr=None)
    try:
        # Try loading instrumental track as .wav files
        instrumental, sr_instrumental = librosa.load(instrumental_filepath, sr=None)
    except:
        # If loading as .wav fails, try loading as .mp3 files
        instrumental, sr_instrumental = librosa.load(instrumental_filepath.replace('.wav', '.mp3'), sr=None)

    # Calculate the average loudness of the vocal and instrumental tracks using pyloudnorm
    meter = pyln.Meter(sr_vocal)  # Create a meter object
    loudness_vocal = meter.integrated_loudness(vocal)  # Calculate the integrated loudness of the vocal track
    loudness_instrumental = meter.integrated_loudness(instrumental)  # Calculate the integrated loudness of the instrumental track

    # Adjust the gain of the vocal track based on the average loudnesses
    gain = loudness_instrumental - loudness_vocal
    vocal_adjusted = vocal * 10**(gain / 20)

    # Mix the vocal and instrumental tracks
    mixed = vocal_adjusted + instrumental

    # Save the mixed track to the output filepath as an MP3 file
    sf.write(output_filepath, mixed, sr_vocal, format='mp3')

