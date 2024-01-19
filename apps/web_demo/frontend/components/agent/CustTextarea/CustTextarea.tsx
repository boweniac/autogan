import { addAgentConversationAPI } from "@/api/add_conversation";
import { streamTestAPI } from "@/api/test";
import { addAgentConversationState } from "@/stores/LocalStoreActions";
import { Container, Flex, MantineStyleProp, rem, Text, Textarea } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { syncMessages } from "../AgentFrameUtil";
import RecordButton from "./AudioToText/AudioToText";

type CustTextareaProps = {
    conversationID: string | undefined;
    isLoading: boolean;
    callback: (value: string) => void;
}

export default function CustTextarea(props: CustTextareaProps) {
    const [value, setValue] = useState<string | undefined>();
    const [popoverOpened, setPopoverOpened] = useState(false);


    const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        event.stopPropagation();
        if (event.keyCode === 13 && !event.shiftKey) {
          if (event.nativeEvent.isComposing) {
            // 处于输入法选词状态，不做处理
          } else {
            event.preventDefault();
            if (value) {
              setValue("")
              props.callback(value);
            }
          }
        }
      };

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {setValue(event.target.value)};

    useEffect(() => {
      if (popoverOpened && props.conversationID) {
        syncMessages(props.conversationID)
      }
  }, [popoverOpened]);

    return (
      <div
            onFocusCapture={() => setPopoverOpened(true)}
            onBlurCapture={() => setPopoverOpened(false)}
        >
          <RecordButton></RecordButton>
          <Textarea
              maw="100%"
              radius="md"
              placeholder="Input placeholder"
              autosize
              minRows={2}
              maxRows={7}
              onKeyDown={handleKeyDown}
              onKeyUp={(e) => e.stopPropagation()}
              disabled={props.isLoading}
              onChange={handleChange}
              value={value}
          />
        </div>
    );
}