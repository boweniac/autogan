import { addAgentConversationAPI } from "@/api/conversation/add_conversation";
import { addAgentConversationMessageBlockState, addAgentMessageState, addAgentConversationListState, updateAgentConversationMessageBlockState } from "@/stores/LocalStoreActions";
import { ActionIcon, Box, Center, Container, FileButton, Flex, Loader, LoadingOverlay, MantineStyleProp, Modal, Popover, Progress, rem, Space, Text, Textarea } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import RecordButton from "./AudioToText/AudioToText";
import { IconFile, IconMicrophone, IconPlayerStop } from "@tabler/icons-react";
import { uploadFileStreamAPI } from "@/api/file/upload_file_stream";
import { v4 as uuidv4 } from "uuid";
import UploadFile from "./UploadFile/UploadFile";

type CustTextareaProps = {
    conversationID: string | undefined;
    isLoading: boolean;
    callback: (value: string) => void;
    stopCallback: () => void;
    syncMessagesCallback: () => void;
    // stopTalking: () => void;
}

export default function CustTextarea(props: CustTextareaProps) {
    const [value, setValue] = useState<string | undefined>();
    const [popoverOpened, setPopoverOpened] = useState(false);
    const [uploadPopoverOpened, setUploadPopoverOpened] = useState(false);
    // const [uploadPopoverOpened, { openUploadPopoverOpened, closeUploadPopoverOpened }] = useDisclosure(false);
    const [analyticalProgress, setAnalyticalProgress] = useState(0);
    const [storageProgress, setStorageProgress] = useState(0);

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
        props.syncMessagesCallback()
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
              placeholder="按住 shift 可以换行"
              autosize
              minRows={1}
              maxRows={7}
              onKeyDown={handleKeyDown}
              onKeyUp={(e) => e.stopPropagation()}
              // disabled={props.isLoading}
              onChange={handleChange}
              value={value}
              leftSection={
                <UploadFile syncMessagesCallback={()=>props.syncMessagesCallback()} conversationID={props.conversationID} startCallback={()=>{
                  setAnalyticalProgress(0)
                  setStorageProgress(0)
                  setUploadPopoverOpened(true)
                }} addCallback={(v)=>{
                  setStorageProgress(v)
                  if (v == 100) {
                    setUploadPopoverOpened(false)
                  }
                }
                } vectorCallback={(v)=>{
                  setAnalyticalProgress(v)
                }}></UploadFile>
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
          <Modal title="文件上传" opened={uploadPopoverOpened} onClose={()=>{}} withCloseButton={false}>
          <LoadingOverlay visible={analyticalProgress == 0} loaderProps={{ children: 'Uploading...' }} />
            <Text>解析进度</Text>
            <Progress value={analyticalProgress} />
            <Space h="md"></Space>
            <Text>存储进度</Text>
            <Progress value={storageProgress} />
      </Modal>
        </div>
    );
}