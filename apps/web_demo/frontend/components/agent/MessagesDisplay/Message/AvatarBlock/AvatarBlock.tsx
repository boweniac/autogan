import { Avatar } from "@mantine/core";

type AvatarBlockProps = {
    role: string | undefined;
}

export default function AvatarBlock(props: AvatarBlockProps) {
    return (
        <Avatar
            src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-2.png"
            alt={props.role}
            radius="xl"
            size="md"
        />
    );
  };