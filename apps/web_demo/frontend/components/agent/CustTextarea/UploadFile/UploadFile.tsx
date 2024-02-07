import { addAgentConversationAPI } from "@/api/conversation/add_conversation";
import { uploadFileStreamAPI } from "@/api/file/upload_file_stream";
import { ActionIcon, FileButton } from "@mantine/core";
import { IconFile } from "@tabler/icons-react";
import { useRouter } from "next/router";
import { v4 as uuidv4 } from "uuid";

type UploadFileProps = {
    conversationID: string | undefined;
    startCallback: () => void;
    addCallback: (value: number) => void;
    vectorCallback: (value: number) => void;
    syncMessagesCallback: () => void;
  }
  
  export default function UploadFile(props: UploadFileProps) {
    const router = useRouter();
    const uploadFile = (payload: File | null, conversationID: string, endCallback?: ()=>void)=>{
        uploadFileStreamAPI([payload], "chat", "", conversationID, (res)=>{
            if (res != undefined) {
              const p = res.index/res.length*100
              if (res.step == "add_chat_file") {
                if (endCallback && p == 100) {
                    endCallback()
                }
                props.addCallback(p)
                // updateAgentConversationMessageBlockState(props.conversationID, messageLocalID, messageBlockLocalID, {add_document_progress: p})
              } else if (res.step == "text_to_vectors") {
                props.vectorCallback(p)
                // updateAgentConversationMessageBlockState(props.conversationID, messageLocalID, messageBlockLocalID, {text_to_vectors_progress: p})
              }
            }
          })
    }
    return (
        <FileButton 
        // disabled={props.conversationID == undefined} 
        onChange={(v)=>{
            if (v) {
                props.startCallback()
                if (props.conversationID) {
                    uploadFile(v, props.conversationID, ()=>{props.syncMessagesCallback()})
                } else {
                    addAgentConversationAPI().then((conversationID)=>{
                        uploadFile(v, conversationID, ()=>{router.push(`/agent/${conversationID}`).then()})
                    })
                }
            }
          }} accept=".pdf">
          {(p) => {
          return <ActionIcon 
          // disabled={props.conversationID == undefined} 
          variant="subtle" aria-label="Settings" {...p}>
              <IconFile style={{ width: '70%', height: '70%' }} stroke={1.5} />
            </ActionIcon>}}
        </FileButton>
    );
  }