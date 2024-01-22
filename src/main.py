# import asyncio
# from typing import Union

# from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse, StreamingResponse
# from pydantic import BaseModel
# import shutil
# import uuid
# import os
# # import wiggle_process_starganv2

# app = FastAPI()

# ###
# # Directory to store uploaded audio files
# upload_directory = "../files"

# # ML code to be run asynchronously
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)

#     stdout, stderr = await proc.communicate()

#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')

# ## Wiggle

# @app.post('/upload_audio')
# def upload_file(uploaded_file: UploadFile = File(...)):
#     fileId = str(uuid.uuid4())[:8]
#     path = f"../files/{fileId}.wav"
#     print(fileId)

#     with open(path, 'w+b') as file:
#         shutil.copyfileobj(uploaded_file.file, file)

#     test1 = "../TestSongs/Survivor - Eye Of The Tiger (O_gaudiolab_vocal.mp3"
#     test2 = "../TestSongs/Britney Spears - OopsI Did It _gaudiolab_vocal.mp3"
#     test3 = "../TestSongs/Right Said Fred - Im Too Sexy _gaudiolab_vocal.mp3"
#     test4 = "../TestSongs/Taylor Swift - Shake It Off [vocals].wav"
#     test5 = "../TestSongs/The Weeknd - Blinding Lights (_gaudiolab_vocal.mp3"

#     # wiggle_process_starganv2.main(path, f"../files/{fileId}_converted.wav")
#     # shell_cmd = f'python3 wiggle_process_starganv2.py -i \'{path}\' -o \'../files/{fileId}_converted.wav\''
#     train_cmd = f'python3 script_train.py -i \'{path}\' -s \'{fileId}\''
#     infer_cmd1 = f'python3 script_infer.py -i \'{test1}\' -o \'../Converted/{test1}_{fileId}_converted.wav\''
#     infer_cmd2 = f'python3 script_infer.py -i \'{test2}\' -o \'../Converted/{test2}_{fileId}_converted.wav\''
#     infer_cmd3 = f'python3 script_infer.py -i \'{test3}\' -o \'../Converted/{test3}_{fileId}_converted.wav\''
#     infer_cmd4 = f'python3 script_infer.py -i \'{test4}\' -o \'../Converted/{test4}_{fileId}_converted.wav\''
#     infer_cmd5 = f'python3 script_infer.py -i \'{test5}\' -o \'../Converted/{test5}_{fileId}_converted.wav\''
#     infer_cmd = f'{infer_cmd1} && {infer_cmd2} && {infer_cmd3} && {infer_cmd4} && {infer_cmd5}'
    
#     # shell_cmd = f'{train_cmd} && {infer_cmd}'
    
#     shell_cmd = f'{infer_cmd}'


#     asyncio.run(run(shell_cmd))

#     return {
#         'uploaded_file': uploaded_file.filename,
#         'uploaded_content': uploaded_file.content_type,
#         'file_id': fileId,
#     }

# @app.get("/get_audio/{file_id}")
# async def get_audio(file_id: str):
#     # rel_filepath = f'files/{fileId}_converted.wav'
#     file_path_original = os.path.join("../files", f"{file_id}.wav")
#     file_path_converted = os.path.join("../files", f"{file_id}_converted.wav")

#     if not os.path.exists(file_path_original):
#         raise HTTPException(status_code=404, detail=(f"Original File failed to upload. Path: {file_path_original}"))

#     if not os.path.exists(file_path_converted):
#         raise HTTPException(status_code=404, detail=(f"Converted File not found. Path: {file_path_converted}"))

#     return StreamingResponse(open(file_path_converted, "rb"), media_type="audio/wav")


# import asyncio
# import subprocess
# from typing import Union

# from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse, StreamingResponse
# from pydantic import BaseModel
# import shutil
# import uuid
# import os
# # import wiggle_process_starganv2

# app = FastAPI()

# ## Helper Functions
# # Directory to store uploaded audio files
# upload_directory = '../files'

# # ML code to be run asynchronously
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)

#     # stdout, stderr = await proc.communicate()

#     # print(f'[{cmd!r} exited with {proc.returncode}]')
#     # if stdout:
#     #     print(f'[stdout]\n{stdout.decode()}')
#     # if stderr:
#     #     print(f'[stderr]\n{stderr.decode()}')

# ## Wiggle

# @app.post('/upload_audio')
# def upload_file(song_id: str, uploaded_file: UploadFile = File(...)):
#     def validate_song_id(song_id: str):
#         match song_id:
#             case 'oops_i_did_it_again':
#                 return 'oops_i_did_it_again' # change server-side id to w/e, I just kept them the same
#             case 'im_too_sexy':
#                 return 'im_too_sexy'
#             case 'eye_of_the_tiger':
#                 return 'eye_of_the_tiger'
#             case 'blinding_lights':
#                 return 'blinding_lights'
#             case _:
#                 raise HTTPException(status_code=400, detail='Song ID Not Found.')

#     valid_song_id = validate_song_id(song_id)
#     fileId = str(uuid.uuid4())[:8]
#     path = f'{upload_directory}/{fileId}.wav'

#     with open(path, 'w+b') as file:
#         shutil.copyfileobj(uploaded_file.file, file)

#     print(f'Processing [{fileId}]: song={valid_song_id}')
#     train_cmd = f'echo \'sup\'' # not necessary for starganv
#     infer_cmd = f'python3 wiggle_process_starganv2.py -i \'{path}\' -o \'{upload_directory}/{fileId}_converted.wav\' -s \'{valid_song_id}\'' # update song here
#     shell_cmd = f'{train_cmd} && {infer_cmd}'
#     asyncio.run(run(shell_cmd))

#     return {
#         'uploaded_file': uploaded_file.filename,
#         'uploaded_content': uploaded_file.content_type,
#         'file_id': fileId,
#     }

# @app.get('/get_audio/{file_id}')
# async def get_audio(file_id: str):
#     # rel_filepath = f'files/{fileId}_converted.wav'
#     file_path_original = os.path.join(f'{upload_directory}', f'{file_id}.wav')
#     file_path_converted = os.path.join(f'{upload_directory}', f'{file_id}_converted.wav')

#     if not os.path.exists(file_path_original):
#         raise HTTPException(status_code=405, detail=(f'Original File failed to upload. Path: {file_path_original}'))

#     if not os.path.exists(file_path_converted):
#         raise HTTPException(status_code=404, detail=(f'Converted File not found. Path: {file_path_converted}'))

#     return StreamingResponse(open(file_path_converted, 'rb'), media_type='audio/wav')


import asyncio
import subprocess
from typing import Union

from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import shutil
import uuid
import os
# import wiggle_process_starganv2

app = FastAPI()

## Helper Functions
# Directory to store uploaded audio files
upload_directory = '../VoiceSamples'
converted_directory = '../Converted'
models_directory = 'runs/logs/44k'

# ML code to be run asynchronously
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)

#     stdout, stderr = await proc.communicate()

#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # while True:
    #     line = await proc.stdout.readline()
    #     if not line:
    #         break
    #     print(line.decode().strip())

    await proc.communicate()

## Wiggle

def validate_song_id(song_id: str):
    match song_id:
        case 'oops_i_did_it_again':
            return 'oops_i_did_it_again' # change server-side id to w/e, I just kept them the same
        case 'im_too_sexy':
            return 'im_too_sexy'
        case 'eye_of_the_tiger':
            return 'eye_of_the_tiger'
        case 'blinding_lights':
            return 'blinding_lights'
        case _:
            raise HTTPException(status_code=400, detail='Song ID Not Found.')


@app.post('/upload_audio')
def upload_file(song_id: str, voice_id: str, uploaded_file: UploadFile = File(...)):
    valid_song_id = validate_song_id(song_id)
    song_path = f'../TestSongs/{valid_song_id}.mp3'
    # file_id = str(uuid.uuid4())[:8]
    uploaded_voice_sample = f'{upload_directory}/{voice_id}.wav'
    current_voice_models_dir = f"{models_directory}/{voice_id}"

    with open(uploaded_voice_sample, 'w+b') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    # print(f'Processing [{file_id}]')

    converted_filename = f'{voice_id}_{song_id}_converted.wav'

    if os.path.exists(os.path.join(converted_directory, converted_filename)):
        print(f'{converted_filename} already exists. Skipping conversion.')
    else:
        if os.path.exists(current_voice_models_dir):
            print(f'Voice [{voice_id}] already exists. Skipping training.')
            print(f'Inferring for song [{song_id}] with voice [{voice_id}]')
            infer_cmd = f'python3 script_infer.py -i \'{song_path}\' -m \'{models_directory}/{voice_id}\' -s \'{voice_id}\' -o \'{converted_directory}/{converted_filename}\''
            shell_cmd = f'{infer_cmd}'
            print(shell_cmd)
            asyncio.run(run(shell_cmd))
        else:
            print(f'Training for voice [{voice_id}] and then inferring for song [{song_id}]')
            train_cmd = f'python3 script_train.py -i \'{uploaded_voice_sample}\' -s \'{voice_id}\''
            infer_cmd = f'python3 script_infer.py -i \'{song_path}\' -m \'{models_directory}/{voice_id}\' -s \'{voice_id}\' -o \'{converted_directory}/{converted_filename}\''
            shell_cmd = f'{train_cmd} && {infer_cmd}'
            print(shell_cmd)
            asyncio.run(run(shell_cmd))

    return {
        'uploaded_file': uploaded_file.filename,
        'uploaded_content': uploaded_file.content_type,
        # 'file_id': file_id,
        'file_id': converted_filename,
    }


# @app.get('/infer_audio/{song_id}')
# async def infer_audio(song_id: str, voice_id: str):
#     valid_song_id = validate_song_id(song_id)
#     file_id = str(uuid.uuid4())[:8]
#     song_path = f'../TestSongs/{valid_song_id}.mp3'
#     infer_cmd = f'python3 script_infer.py -i \'{song_path}\' -m \'{models_directory}/{voice_id}\' -s \'{voice_id}\' -o \'{converted_directory}/{file_id}_converted.wav\''
#     print(infer_cmd)
#     shell_cmd = f'{infer_cmd}'
#     task = asyncio.create_task(run(shell_cmd))
#     await task
#     return {
#         'file_id': file_id,
#     }

@app.get('/infer_audio/{song_id}')
def infer_audio(song_id: str, voice_id: str):
    valid_song_id = validate_song_id(song_id)
    converted_filename = f'{voice_id}_{song_id}_converted.wav'
    if os.path.exists(os.path.join(converted_directory, converted_filename)):
        print(f'{converted_filename} already exists. Skipping conversion.')
    else:
        # file_id = str(uuid.uuid4())[:8]
        song_path = f'../TestSongs/{valid_song_id}.mp3'
        infer_cmd = f'python3 script_infer.py -i \'{song_path}\' -m \'{models_directory}/{voice_id}\' -s \'{voice_id}\' -o \'{converted_directory}/{converted_filename}\''
        print(infer_cmd)
        shell_cmd = f'{infer_cmd}'
        asyncio.run(run(shell_cmd))
    
    return {
        'file_id': converted_filename,
    }


@app.get('/get_audio/{file_id}')
async def get_audio(song_id: str, voice_id: str):
    # rel_filepath = f'files/{fileId}_converted.wav'
    # file_path_original = os.path.join(f'{upload_directory}', f'{file_id}.wav')
    converted_filename = f'{voice_id}_{song_id}_converted.wav'
    file_path_converted = os.path.join(f'{converted_directory}', f'{converted_filename}')
    file_path_trained_models = os.path.join(f'{models_directory}/{voice_id}')

    # if not os.path.exists(file_path_original):
    #     raise HTTPException(status_code=404, 
    #                         detail= {
    #                             'reason': 'original_upload_missing',
    #                             'message': 'Original file failed to upload.',
    #                             'debug': (f'Path: {file_path_original}')
    #                         })
    if not os.path.exists(file_path_trained_models):
        raise HTTPException(status_code=404,
                            detail= {
                                'reason': 'trained_model_missing',
                                'message': 'Training incomplete or failed. Please try again later.',
                                'debug': (f'Path: {file_path_trained_models}')
                            })
    if not os.path.exists(file_path_converted):
        raise HTTPException(status_code=404,
                            detail= {
                                'reason': 'converted_file_missing',
                                'message': 'Converted File not found.',
                                'debug': (f'Path: {file_path_converted}')
                            })

    return StreamingResponse(open(file_path_converted, 'rb'), media_type='audio/wav')