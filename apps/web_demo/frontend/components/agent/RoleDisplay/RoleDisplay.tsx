import { Button, Stack } from "@mantine/core";
import GLBViewer from "../avatar/DefaultAvatar/DefaultAvatar";
import DefaultAvatar from "../avatar/DefaultAvatar/DefaultAvatar2";

export default function RoleDisplay() {
    return (
        <Stack
            h={1000}
            w={1000}
            bg="var(--mantine-color-body)"
            justify="space-between"
        >
            <DefaultAvatar />
        </Stack>
    );
}