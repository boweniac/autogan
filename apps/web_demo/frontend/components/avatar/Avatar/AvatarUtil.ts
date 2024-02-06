import { MouthCues } from "@/stores/TypeAudioAndLip"

export const animateMorphTargets = (startTime: number, callback: (ratio: number)=>void) => {
    const duration = 200; // 持续时间（毫秒）
    const animate = (time: number) => {
        const elapsed = time - startTime;
        if (elapsed < duration) {
            const ratio = elapsed / duration;
            callback(ratio);
            requestAnimationFrame(animate);
        } else {
            callback(1);
        }
    };
    requestAnimationFrame(animate);
}

export interface Position {
    x: string | number;
    y: string | number;
    z: string | number;
    rotation: string | number;
}