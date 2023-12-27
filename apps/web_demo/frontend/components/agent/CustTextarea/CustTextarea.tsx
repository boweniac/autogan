import { streamTestAPI } from "@/api/test";
import { Container, Flex, MantineStyleProp, rem, Text, Textarea } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useState } from "react";

type CustTextareaProps = {
    setTest: React.Dispatch<React.SetStateAction<string | undefined>>;
}

export default function CustTextarea(props: CustTextareaProps) {
    const [value, setValue] = useState<string | undefined>();
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);  // 注册过程loading

    const doSubmit = async () => {
        if (!isLoading) {
          loadingStart()
          // 并非新对话
          if (value != undefined) {
            let text = ""
            await streamTestAPI(
                value,
                undefined,
                (res) => {
                    console.log(`res:`+JSON.stringify(res));
                    console.log(`res.text:`+JSON.stringify(res.text));
                    text += res.text
                    props.setTest(text)
                },
                undefined
              ).then();
          }
          setValue("");
          loadingEnd()
        }
      };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        event.stopPropagation();
        if (event.keyCode === 13 && !event.shiftKey) {
          if (event.nativeEvent.isComposing) {
            // 处于输入法选词状态，不做处理
          } else {
            event.preventDefault();
            doSubmit();
          }
        }
      };
      const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {setValue(event.target.value)};

    return (
        <Textarea
            maw="100%"
            radius="md"
            placeholder="Input placeholder"
            autosize
            minRows={2}
            maxRows={4}
            style={{ margin: rem(50) }}
            onKeyDown={handleKeyDown}
            onKeyUp={(e) => e.stopPropagation()}
            onChange={handleChange}
            value={value}
        />
    );
}