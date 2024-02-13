import { useEffect, useState } from 'react';
import { Center, Tooltip, UnstyledButton, Stack, rem, Divider, Space, Box } from '@mantine/core';
import {
  IconHome2,
  IconRobot,
  IconDeviceDesktopAnalytics,
  IconFingerprint,
  IconCalendarStats,
  IconUser,
  IconSettings,
  IconLogout,
  IconSwitchHorizontal,
  IconBurger,
} from '@tabler/icons-react';
import { MantineLogo } from '@mantinex/mantine-logo';
import classes from './NavbarMinimal.module.css';
import { useRouter } from 'next/router';
import { LocalState, localStore } from '@/stores/LocalStore';
import UserMenu from './UserMenu/UserMenu';

interface NavbarLinkProps {
  icon: typeof IconHome2;
  label: string;
  active?: boolean;
  onClick?(): void;
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
    return (
        <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
        <UnstyledButton onClick={onClick} className={classes.link} data-active={active || undefined}>
            <Icon style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
        </UnstyledButton>
        </Tooltip>
    );
}

const mockdata = [
  { icon: IconHome2, label: 'Home', page: '/' },
  { icon: IconRobot, label: 'Agent', page: '/agent' },
];

export function NavbarMinimal() {
  const [active, setActive] = useState(2);
  const router = useRouter();
  const activePage = localStore((state: LocalState) => state.activePage);
  const userToken = localStore((state: LocalState) => state.userToken);

  const [viewportHeight, setViewportHeight] = useState(0); 

  useEffect(() => {
    // 这确保了window.innerHeight只在客户端获取
    setViewportHeight(window.innerHeight);

    const handleResize = () => {
      setViewportHeight(window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // const viewportHeight = window.innerHeight;
//   useEffect(() => {
//     if (router.isReady) {
//       notifications.show({
//         message: "请求失败：",
//         color: "red",
//     });
//     }
// }, [router.isReady]);

  const links = mockdata.map((link, index) => {
    return (
    <NavbarLink
      icon={link.icon}
      label={link.label}
      key={link.label}
      active={link.page == activePage}
      onClick={() => {
        router.push(link.page)
      }}
    />
  )});

  return (
    <nav style={{ height: `${viewportHeight}px`}} className={classes.navbar}>
      <Box>
      <Space h="xs" />
      <Center>
        <IconBurger type="mark" size={30} />
      </Center>
      <Space h="xs" />
      <Divider />
      <div className={classes.navbarMain}>
        <Stack justify="center" align="center" gap="sm">
          {links}
        </Stack>
      </div>
      </Box>

      <Stack align="center" justify="center" gap={0}>
        <UserMenu></UserMenu>
        {/* <NavbarLink icon={IconSwitchHorizontal} label="Change account" active={true} />
        <NavbarLink icon={IconLogout} label="Logout" /> */}
      </Stack>
    </nav>
  );
}