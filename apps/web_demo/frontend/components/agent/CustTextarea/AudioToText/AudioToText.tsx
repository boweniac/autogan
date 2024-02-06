import { useRef, useState } from 'react';
import { ActionIcon, Button, Loader, MantineProvider } from '@mantine/core';
import { audioToTextAPI } from '@/api/audio/audio_to_text';
import { IconMicrophone, IconPlayerStop } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';
// import { RingLoader } from './RingLoader';

type AppProps = {
  callback: (value: string) => void;
}

const RecordButton = (props: AppProps) => {
    const [isRecording, { open: recordStart, close: recordEnd }] = useDisclosure(false);
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);
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
        audioToTextAPI(formData).then((value)=>{
          loadingEnd()
          props.callback(value)
        })
      };
      mediaRecorder.current.start();
      recordStart();
    };
  
    const stopRecording = () => {
      mediaRecorder.current?.stop();
      recordEnd();
      loadingStart()

      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop()); // 关闭所有轨道
        streamRef.current = null; // 清空stream引用
      }
    };
  

  return (
    // <Button 
    //   onClick={isRecording ? stopRecording : startRecording} 
    //   color={isRecording ? 'red' : 'blue'}
    // >
    //   {isRecording ? 'Stop Recording' : 'Start Recording'}
    // </Button>
    <ActionIcon variant="subtle" radius="xl" aria-label="Record" onClick={isRecording ? stopRecording : startRecording} loading={isLoading}>
    {isRecording ? <Loader size="xs" type="bars"/> : <IconMicrophone style={{ width: '70%', height: '70%' }} stroke={1.5} />}
    {/* {isRecording ? <Loader size="xs" type="bars"/> : <IconMicrophone style={{ width: '70%', height: '70%' }} stroke={1.5} />} */}
  </ActionIcon>
  );
};

export default RecordButton;
