import { Message } from "@/stores/TypeAgentChat";
import { Avatar, Group, Text } from "@mantine/core";

type UserMessageBlockProps = {
    message: Message;
}

export default function UserMessageBlock(props: UserMessageBlockProps) {
    const message = props.message

    return <div>
        <Group justify="flex-end">
            <Text fz="sm">{message.name}</Text>
            <Avatar
                src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png"
                alt={message.name}
                radius="xl"
            />
        </Group>
        <Group justify="flex-end">
            <Text fz="sm">{message.content}</Text>
        </Group>
    </div>
}