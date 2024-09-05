import { Group, Button } from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';

export function BottomNavbar() {
    return (
        <Group justify="center" >
            <a href="https://beian.miit.gov.cn/" target="_blank">备案号：京ICP备2023021208号-1</a>
        </Group>
    );
}