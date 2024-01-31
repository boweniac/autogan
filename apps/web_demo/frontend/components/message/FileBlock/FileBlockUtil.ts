export function getFileExtension(filename: string | undefined): string | undefined {
    if (filename) {
        // 将文件名按照点号分割，获取数组的最后一个元素作为扩展名
        const parts = filename.split('.');
        return parts[parts.length - 1];
    } else {
        return undefined
    }
  }