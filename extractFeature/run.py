import subprocess
import librosa
import numpy as np
import matplotlib.pyplot as plt
from vosk import Model, KaldiRecognizer
import wave
import json

# 将MP3文件转换为WAV格式
def convert_mp3_to_wav(mp3_path, wav_path):
    subprocess.call(['ffmpeg', '-i', mp3_path, wav_path])

# 提取MFCC特征并可视化
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # 检查音频文件是否加载正确
    if len(y) == 0:
        print("Error: Audio file is empty or corrupted.")
        return None

    # 提取MFCC特征
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=int(sr*0.01), n_fft=int(sr*0.02))

    # 打印和可视化MFCC特征
    print("MFCC Features Shape:", mfccs.shape)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()

    return mfccs

# 加载Vosk模型
model = Model('vosk-model-en-us-0.22')

# 将音频文件转换为文本并打印中间结果
def speech_to_text(wav_path):
    # 打开WAV文件
    wf = wave.open(wav_path, 'rb')
    
    # 提取特征
    features = extract_features(wav_path)
    if features is None:
        return "Failed to extract features from audio."
    
    # 初始化识别器
    rec = KaldiRecognizer(model, wf.getframerate())
    
    # 识别音频
    result = []
    acoustic_model_output = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            partial_result = rec.PartialResult()
            acoustic_model_output.append(partial_result)
            print("Partial Result (Acoustic Model Output):")
            print(partial_result)
            result.append(json.loads(rec.Result()))
    
    # 拼接结果文本
    final_result = rec.FinalResult()
    print("Final Result (Decoded Text):")
    print(final_result)
    result.append(json.loads(final_result))
    
    # 解析声学模型输出
    phonemes = []
    for res in result:
        if 'text' in res:
            phonemes.extend(res['text'].split())
    
    print("Phonemes (after acoustic model):")
    print(phonemes)
    
    # 示例字典（音素到单词的映射）
    phoneme_to_word = {
        'tyger': 'Tyger',
        'burning': 'burning',
        'bright': 'bright',
        'in': 'in',
        'the': 'the',
        'forests': 'forests',
        'of': 'of',
        'night': 'night',
        'what': 'what',
        'immortal': 'immortal',
        'hand': 'hand',
        'or': 'or',
        'eye': 'eye',
        'could': 'could',
        'frame': 'frame',
        'thy': 'thy',
        'fearful': 'fearful',
        'symmetry': 'symmetry'
    }
    
    # 转换音素到单词
    words = [phoneme_to_word.get(phoneme, phoneme) for phoneme in phonemes]
    print("Words (after dictionary lookup):")
    print(words)
    
    # 拼接成最终文本
    text = ' '.join(words)
    return text

# 示例：将MP3文件转换为WAV格式并识别
audio_path = '../sample3.mp3'
wav_path = audio_path.replace('.mp3', '.wav')
convert_mp3_to_wav(audio_path, wav_path)

# 获取最终文本并打印
transcript = speech_to_text(wav_path)
print("Final Transcript:")
print(transcript)
