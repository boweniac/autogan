import { Anchor, Progress, rem } from "@mantine/core";
import { IconFileTypeDoc, IconFileTypeDocx, IconFileTypePdf, IconFileUnknown } from "@tabler/icons-react";
import { getFileExtension } from "./FileBlockUtil";


type FileBlockProps = {
    content_tag: string | undefined;
  }
  
  export default function FileBlock(props: FileBlockProps) {
    const file_type = getFileExtension(props.content_tag)
    return (
      <Anchor href={`https://aibowen-base.boweniac.top/${props.content_tag}`} target="_blank" underline="always">
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
      </Anchor>
      // <div>
      //   {file_type == "pdf" || file_type == "PDF" ? (
      //       <IconFileTypePdf
      //           style={{ width: rem(80), height: rem(80) }}
      //           stroke={1.5}
      //           // color="var(--mantine-color-blue-filled)"
      //     />
      //   ) : file_type == "docx" ? (
      //       <IconFileTypeDocx
      //           style={{ width: rem(80), height: rem(80) }}
      //           stroke={1.5}
      //     />
      //   ) : file_type == "doc" ? (
      //       <IconFileTypeDoc
      //           style={{ width: rem(80), height: rem(80) }}
      //           stroke={1.5}
      //     />
      //   ) : (
      //       <IconFileUnknown
      //           style={{ width: rem(80), height: rem(80) }}
      //           stroke={1.5}
      //     />
      //   )}
      // </div>
    );
  }