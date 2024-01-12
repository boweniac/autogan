import { Button, Group, Modal, TextInput, Text } from "@mantine/core";
import { IconAbc } from "@tabler/icons-react";
import {useForm} from "@mantine/form";
import { updateConversationTitleAPI } from "@/api/update_conversation_title";
import { useDisclosure } from "@mantine/hooks";
import { deleteAgentConversationState, updateAgentConversationState } from "@/stores/LocalStoreActions";
import { deleteConversationAPI } from "@/api/delete_conversation";

type DeleteModalProps = {
    conversation_id: string
    title: string | undefined
    opened: boolean;
    onClose: () => void;
    onDelete: () => void;
  }
  
  export default function DeleteModal(props: DeleteModalProps) {
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);


    return (
        <Modal size="xs" opened={props.opened} onClose={props.onClose} title="Delete">
            <Text>This will delete {props.title || ""}</Text>
            <Group justify="space-between" mt="xl">
                <Button variant="default" color="gray" onClick={()=>props.onClose()}>Cancel</Button>
                <Button color="red" onClick={()=>{deleteConversationAPI(props.conversation_id).then(()=>{
                    deleteAgentConversationState(props.conversation_id)
                    props.onDelete()
                    })}}>Delete</Button>
            </Group>
        </Modal>
    );
  }
