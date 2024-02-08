import { useRef, useState } from 'react';
import { ActionIcon, Button, Loader, MantineProvider, rem } from '@mantine/core';
import { audioToTextAPI } from '@/api/audio/audio_to_text';
import { IconMicrophone, IconPlayerStop } from '@tabler/icons-react';
import { useDisclosure } from '@mantine/hooks';
// import { RingLoader } from './RingLoader';
import classes from './SpeakToText.module.css';
import { LocalState, localStore } from '@/stores/LocalStore';

type SpeakButtonProps = {
  callback: (value: string) => void;
}

const SpeakButton = (props: SpeakButtonProps) => {
    const [isRecording, { open: recordStart, close: recordEnd }] = useDisclosure(false);
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);
    const mediaRecorder = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);
    const streamRef = useRef<MediaStream | null>(null);

    const avatarState = localStore((state: LocalState) => state.avatarState);
    const classSpeakButton = avatarState ? classes.speakButtonAvatarOn : classes.speakButtonAvatarOff;
  
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
      if (isRecording) {
        mediaRecorder.current?.stop();
        recordEnd();
        loadingStart()
  
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop()); // 关闭所有轨道
          streamRef.current = null; // 清空stream引用
        }
      }
    };
  

  return (
    // <Button 
    //   onClick={isRecording ? stopRecording : startRecording} 
    //   color={isRecording ? 'red' : 'blue'}
    // >
    //   {isRecording ? 'Stop Recording' : 'Start Recording'}
    // </Button>
    <ActionIcon className={classSpeakButton} size={rem(100)} variant="filled" radius="xl" aria-label="Record" 
    mb={rem(50)}
    onClick={isRecording ? stopRecording : startRecording}
    // onMouseDown={startRecording} 
    // onMouseUp={stopRecording} 
    // onMouseLeave={stopRecording} 
    // onTouchStart={startRecording} 
    // onTouchEnd={stopRecording} 
    // onTouchCancel={stopRecording} 
    loading={isLoading}>
    {isRecording ? <Loader size={rem(100)} type="bars"/> : <IconMicrophone size={rem(100)} style={{ width: '70%', height: '70%' }} stroke={1.5} />}
    {/* {isRecording ? <Loader size="xs" type="bars"/> : <IconMicrophone style={{ width: '70%', height: '70%' }} stroke={1.5} />} */}
  </ActionIcon>
  );
};

export default SpeakButton;
