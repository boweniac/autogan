import { addAgentConversationAPI } from "@/api/add_conversation";
import { streamTestAPI } from "@/api/request_open";
import { addAgentConversationMessageBlockState, addAgentConversationMessageState, addAgentConversationState, updateAgentConversationMessageBlockState } from "@/stores/LocalStoreActions";
import { ActionIcon, Container, FileButton, Flex, MantineStyleProp, rem, Text, Textarea } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { syncMessages } from "../AgentFrameUtil";
import RecordButton from "./AudioToText/AudioToText";
import { IconFile, IconMicrophone, IconPlayerStop } from "@tabler/icons-react";
import { uploadFileStreamAPI } from "@/api/upload_file_stream";
import { v4 as uuidv4 } from "uuid";

type CustTextareaProps = {
    conversationID: string | undefined;
    isLoading: boolean;
    callback: (value: string) => void;
    stopCallback: () => void;
    // stopTalking: () => void;
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
          {/* <RecordButton></RecordButton> */}
          <Textarea
              maw="100%"
              radius="md"
              placeholder="Talk to agent"
              autosize
              minRows={1}
              maxRows={7}
              onKeyDown={handleKeyDown}
              onKeyUp={(e) => e.stopPropagation()}
              // disabled={props.isLoading}
              onChange={handleChange}
              value={value}
              leftSection={
                <FileButton disabled={props.conversationID == undefined} onChange={(v)=>{
                  const messageLocalID = uuidv4()
                  const messageBlockLocalID = uuidv4()
                  uploadFileStreamAPI([v], "chat", "", props.conversationID, (res)=>{
                    if (props.conversationID != undefined && res != undefined) {
                      const p = res.index/res.length*100
                      console.log(`res.index/res.length:`+p);
                      if (res.step == "add_chat_file") {
                        updateAgentConversationMessageBlockState(props.conversationID, messageLocalID, messageBlockLocalID, {add_document_progress: p})
                      } else if (res.step == "text_to_vectors") {
                        updateAgentConversationMessageBlockState(props.conversationID, messageLocalID, messageBlockLocalID, {text_to_vectors_progress: p})
                      } else {
                        addAgentConversationMessageState(props.conversationID, {
                            task_id: props.conversationID,
                            localID: messageLocalID,
                            msg_id:res.msg_id,
                            agent_name: res.agent_name,
                            message_blocks: []
                        })
                        addAgentConversationMessageBlockState(props.conversationID, messageLocalID, {
                            task_id: props.conversationID,
                            localID: messageBlockLocalID,
                            msg_id: res.msg_id,
                            agent_name: res.agent_name,
                            content_type: "file",
                            content_tag: res.file_name,
                            content: "",
                            tokens: 0
                        })
                      }
                    }
                  })
                  }} accept=".pdf">
                  {(p) => {
                  return <ActionIcon disabled={props.conversationID == undefined} variant="subtle" aria-label="Settings" {...p}>
                      <IconFile style={{ width: '70%', height: '70%' }} stroke={1.5} />
                    </ActionIcon>}}
                </FileButton>
              }
              rightSection={props.isLoading ? <ActionIcon variant="subtle" aria-label="Settings" onClick={props.stopCallback}>
              <IconPlayerStop style={{ width: '70%', height: '70%' }} stroke={1.5} />
            </ActionIcon> : <RecordButton callback={(value)=>{
              if (value) {
                setValue("")
                props.callback(value);
              }
            }}></RecordButton>}
          />
        </div>
    );
}