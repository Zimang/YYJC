import pyttsx3

# 诗歌文本
text = """
Tyger Tyger, burning bright,
In the forests of the night;
What immortal hand or eye,
Could frame thy fearful symmetry?
"""

# 初始化TTS引擎
engine = pyttsx3.init()

# 设置语速
engine.setProperty('rate', 150)

# 设置音量
engine.setProperty('volume', 0.9)

# 保存音频到文件
output_path = "./the_tyger.wav"
engine.save_to_file(text, output_path)

# 运行TTS引擎
engine.runAndWait()

output_path
