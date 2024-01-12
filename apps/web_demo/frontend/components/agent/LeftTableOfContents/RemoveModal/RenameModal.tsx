import { Button, Modal, TextInput } from "@mantine/core";
import { IconAbc } from "@tabler/icons-react";
import {useForm} from "@mantine/form";
import { updateConversationTitleAPI } from "@/api/update_conversation_title";
import { useDisclosure } from "@mantine/hooks";
import { updateAgentConversationState } from "@/stores/LocalStoreActions";
import { useEffect, useState } from "react";

type RenameModalProps = {
    conversation_id: string
    title: string | undefined
    opened: boolean;
    onClose: () => void;
  }
  
  export default function RenameModal(props: RenameModalProps) {
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);

    const form = useForm({
        initialValues: {
            title: "",
        },
    });

    useEffect(() => {
        form.setFieldValue('title', props.title || '');
      }, [props.title]);

    return (
        <Modal opened={props.opened} onClose={props.onClose} title="Rename">
            <form onSubmit={form.onSubmit((values) => updateConversationTitleAPI(props.conversation_id, values.title).then((res)=>{
                updateAgentConversationState(props.conversation_id, {"title": values.title})
                props.onClose()
            }))}>
                <TextInput
                    leftSection={<IconAbc size="1rem" />}
                    placeholder="Title"
                    {...form.getInputProps('title')}
                />
                <Button loading={isLoading} mt="md" fullWidth={true} type="submit">Submit</Button>
            </form>
        </Modal>
    );
  }
