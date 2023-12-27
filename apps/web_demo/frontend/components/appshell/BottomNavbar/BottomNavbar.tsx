import { Group, Button } from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';

export function BottomNavbar() {
    return (
        <Group justify="space-between" grow hiddenFrom="sm">
            <Button variant="default">First</Button>
            <Button variant="default">Second</Button>
            <Button variant="default">Third</Button>
        </Group>
    );
}