import { Avatar, rem } from "@mantine/core";

type AvatarBlockProps = {
    avatarName: string | undefined;
}

export default function AvatarBlock(props: AvatarBlockProps) {
    let avatarName = "customer"
    if (props.avatarName) {
        avatarName = props.avatarName
    }
    return (
        <Avatar
            src={`/avatars/${avatarName}.png`}
            alt={avatarName}
            radius="xl"
            size={rem(38)}
        />
    );
  };