import {
    HoverCard,
    Group,
    Button,
    UnstyledButton,
    Text,
    SimpleGrid,
    ThemeIcon,
    Anchor,
    Divider,
    Center,
    Box,
    Burger,
    Drawer,
    Collapse,
    ScrollArea,
    NativeSelect,
    rem,
    useMantineTheme,
    Switch,
} from '@mantine/core';
import { MantineLogo } from '@mantinex/mantine-logo';
import { useDisclosure } from '@mantine/hooks';
import {
    IconNotification,
    IconCode,
    IconBook,
    IconChartPie3,
    IconFingerprint,
    IconCoin,
    IconChevronDown,
    IconSun,
    IconVolume3,
    IconVolume,
} from '@tabler/icons-react';
import classes from './HeaderMegaMenu.module.css';
import AvatarMenu from './AvatarMenu/AvatarMenu';
import { LocalState, localStore } from '@/stores/LocalStore';
import { updateMuteStateState } from '@/stores/LocalStoreActions';

type HeaderMegaMenuProps = {
    muteCallback: (value: boolean) => void;
    selectAvatarCallback: (value: string) => void;
  }

export function HeaderMegaMenu(props: HeaderMegaMenuProps) {
    const muteState = localStore((state: LocalState) => state.muteState);
    const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);
    const [linksOpened, { toggle: toggleLinks }] = useDisclosure(false);
    const theme = useMantineTheme();

    return (
        <Box>
            <header className={classes.header}>
                <Group justify="flex-end" h="100%">
                    <Switch size="lg" checked={muteState} onChange={(v)=>{updateMuteStateState(v.currentTarget.checked)}} style={{marginRight: rem(32)}} color="dark.4" onLabel={<IconVolume
                        style={{ width: rem(16), height: rem(16) }}
                        stroke={2.5}
                        />} offLabel={<IconVolume3
                            style={{ width: rem(16), height: rem(16) }}
                            stroke={2.5}
                        />} />
                    <AvatarMenu ></AvatarMenu>

                    <Burger opened={drawerOpened} onClick={toggleDrawer} hiddenFrom="sm" />
                </Group>
            </header>
        </Box>
    );
}