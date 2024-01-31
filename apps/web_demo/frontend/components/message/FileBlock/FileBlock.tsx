import { Progress, rem } from "@mantine/core";
import { IconFileTypeDoc, IconFileTypeDocx, IconFileTypePdf, IconFileUnknown } from "@tabler/icons-react";
import { getFileExtension } from "./FileBlockUtil";


type FileBlockProps = {
    content_tag: string | undefined;
    text_to_vectors_progress: number | undefined;
    add_document_progress: number | undefined;
  }
  
  export default function FileBlock(props: FileBlockProps) {
    const file_type = getFileExtension(props.content_tag)
    return (
      <div>
        {file_type == "pdf" || file_type == "PDF" ? (
            <IconFileTypePdf
                style={{ width: rem(80), height: rem(80) }}
                stroke={1.5}
                // color="var(--mantine-color-blue-filled)"
          />
        ) : file_type == "docx" ? (
            <IconFileTypeDocx
                style={{ width: rem(80), height: rem(80) }}
                stroke={1.5}
          />
        ) : file_type == "doc" ? (
            <IconFileTypeDoc
                style={{ width: rem(80), height: rem(80) }}
                stroke={1.5}
          />
        ) : (
            <IconFileUnknown
                style={{ width: rem(80), height: rem(80) }}
                stroke={1.5}
          />
        )}
        <p>{props.content_tag}</p>
        {props.text_to_vectors_progress ? <Progress.Root size="xl">
      <Progress.Section value={props.text_to_vectors_progress}>
        <Progress.Label>Analytical progress</Progress.Label>
      </Progress.Section>
    </Progress.Root> : <></>}
    {props.add_document_progress ? <Progress.Root size="xl">
      <Progress.Section value={props.add_document_progress}>
        <Progress.Label>Storage progress</Progress.Label>
      </Progress.Section>
    </Progress.Root> : <></>}
      </div>
    );
  }