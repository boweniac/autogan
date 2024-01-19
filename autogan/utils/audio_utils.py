import os
from typing import Optional
import subprocess
from pydub import AudioSegment


def audio_to_lip(work_dir: str, file_name: str, response_format: Optional[str] = "mp3") -> Optional[str]:
    try:
        if response_format == "mp3":
            audio = AudioSegment.from_mp3(f"{work_dir}{file_name}.mp3")
        elif response_format == "ogg":
            audio = AudioSegment.from_ogg(f"{work_dir}{file_name}.ogg")
        else:
            return None
        audio.export(f"{work_dir}{file_name}.wav", format="wav")

        result = subprocess.run(f"/root/agent/Rhubarb-Lip-Sync-1.13.0-Linux/rhubarb -o {work_dir}{file_name}.txt {work_dir}{file_name}.wav -f json -r phonetic", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        returncode = result.returncode

        if returncode == 0:
            with open(f'{work_dir}{file_name}.txt', 'r') as file:
                # 读取文件内容
                file_content = file.read()

                # 将 JSON 字符串转换为字典
            os.remove(f"{work_dir}{file_name}.wav")
            return file_content
        else:
            return None
    except subprocess.CalledProcessError as e:
        return None
