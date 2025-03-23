from fastapi import Request, FastAPI, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from utils import *
import os
from scipy.io import wavfile
import io

app = FastAPI()
template = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def root(request: Request):
    return template.TemplateResponse('index.html', {"request": request})

@app.post('/transform')
async def transform_audio(file: UploadFile = File(...), type: str = Form(...)):
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        if type == 'waveform':
            return JSONResponse(content={"status": "successfully", "photo": plot_waveform(rate, audio, "Waveform")})
        else:
            return JSONResponse(content={"status": "successfully", "photo":  plot_frequency_spectrum(rate, audio, "frequency_spectrum")})
    except Exception as e:
        return JSONResponse(content={"status": "falied", "message": f"{e}"})
    
@app.post('/compare')
async def compare_audio(file: UploadFile = File(...), type: str = Form(...)):
    try: 
        print(file)
        binary_data1, binary_data2 = await file.read() 
        wav_io1, wav_io2 = io.BytesIO(binary_data1), io.BytesIO(binary_data2)

        _, audio1= wavfile.read(wav_io1)
        _, audio2= wavfile.read(wav_io2)
        if type == 'data':
            l = ['0% ~ 0%\nRisk-free', '20% ~ 40%\nSecure', '40% ~ 60%\nModerate', '60% ~ 80%\nDangerous', '80% ~ 100%\nHazardous']
            rate_check = [[0, 0], [20, 40], [40, 60], [60, 80], [80, 101]]
            final = compare_audio(audio1, audio2)
            for i in range(5):
                if rate_check[i][1] > final >= rate_check[i][0]:
                    return JSONResponse(content={"status": "successfully", "messsage": l[i]})
        elif type == 'wavefrom':
            return JSONResponse(content={"status": "successfully", "photo": plot_waveform_compare(audio1, audio2)})

        else:
            return JSONResponse(content={"status": "successfully", "photo": plot_spectrogram_compare(audio1, audio2)})
        
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

@app.post('/encode')
async def encode_audio(file: UploadFile = File(...)):
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        _, audio = wavfile.read(wav_io)
        encryption_id = generate_encryption_id()
        accelerated_audio = speed_up_audio(audio, 2.0)
        encoded_audio = embed_watermark(accelerated_audio, encryption_id)
        return JSONResponse(content={"status": "successfully", "photo": save_audio(encode_audio)})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

@app.post('/decode')
async def decode_audio(file: UploadFile = File(...)):
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        _, audio = wavfile.read(wav_io)
        extracted_id = extract_watermark(audio)
        psw = input("請輸入密鑰進行驗證: ")

        if psw == extracted_id:
            remove = input("是否移除水印並生成解密後音檔？(y/n): ").lower() == 'y'
            if remove:
                return JSONResponse(content={"status": "successfully", "photo": save_audio(encode_audio)})
               
        else:
             return JSONResponse(content={"status": "failed", "message": 'input format error'})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})
