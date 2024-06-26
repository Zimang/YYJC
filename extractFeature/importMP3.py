import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

# 加载MP3音频文件
audio_path = '../sample.mp3'
y, sr = librosa.load(audio_path, sr=None)

# 打印音频信息
print(f"Sample rate: {sr}")
print(f"Audio shape: {y.shape}")

# 提取MFCC特征
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# 打印MFCC特征的形状
print(f"MFCC shape: {mfccs.shape}")

# 对MFCC特征进行标准化处理
mfccs = (mfccs - np.mean(mfccs, axis=1, keepdims=True)) / np.std(mfccs, axis=1, keepdims=True)

# 可视化MFCC特征
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, sr=sr, x_axis='time', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('MFCC')
plt.tight_layout()
plt.show()
