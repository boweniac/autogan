import { useRouter } from "next/router";
import { useEffect, useRef } from "react";

type AudioPlayProps = {
    src: string | undefined;
    onFinishedPlaying: () => void;
    onPlaying: (currentTime: number) => void
  }


export default function AudioPlay(props: AudioPlayProps) {
    const audioRef = useRef<HTMLAudioElement>(null);

    useEffect(() => {
      const audio = audioRef.current;
      if (audio) {
        audio.play()
          .then(() => {
            console.log("Audio is playing");
          })
          .catch(error => {
            console.error("Error playing audio", error);
          });
        
        audio.onended = () => {
          props.onFinishedPlaying();
        };

        audio.ontimeupdate = () => {
          props.onPlaying(audio.currentTime);
      };
      }
    }, [props.src, props.onFinishedPlaying]);

    return <audio ref={audioRef} src={props.src} />;
}