import { useRef, useState } from 'react';
import { Button } from '@mantine/core';
import { audioToTextAPI } from '@/api/audio_to_text';

const RecordButton = () => {
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorder = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);
    const streamRef = useRef<MediaStream | null>(null);
  
    const startRecording = async () => {
      const constraints = {
        audio: {
          sampleRate: 16000  // 设置音频采样率为 16000 Hz
        }
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;
      mediaRecorder.current = new MediaRecorder(stream);
      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };
      mediaRecorder.current.onstop = () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/mp4' });
        audioChunks.current = [];
  
        // 发送音频到后端
        const formData = new FormData();
        formData.append('file', audioBlob);
  
        audioToTextAPI(formData)
      };
      mediaRecorder.current.start();
      setIsRecording(true);
    };
  
    const stopRecording = () => {
      mediaRecorder.current?.stop();
      setIsRecording(false);

      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop()); // 关闭所有轨道
        streamRef.current = null; // 清空stream引用
      }
    };
  

  return (
    <Button 
      onClick={isRecording ? stopRecording : startRecording} 
      color={isRecording ? 'red' : 'blue'}
    >
      {isRecording ? 'Stop Recording' : 'Start Recording'}
    </Button>
  );
};

export default RecordButton;
