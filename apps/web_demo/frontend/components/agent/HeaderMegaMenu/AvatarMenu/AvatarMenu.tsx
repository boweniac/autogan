import { LocalState, localStore } from "@/stores/LocalStore";
import { Avatar, Center, Group, Menu, UnstyledButton, rem, Text } from "@mantine/core";
import { IconChevronDown, IconRobot, IconRobotOff, IconVolume3 } from "@tabler/icons-react";
import { useState } from "react";
import classes from './AvatarMenu.module.css';
import { updateAgentAvatarMappingState, updateAvatarStateState } from "@/stores/LocalStoreActions";

// type AvatarMenuProps = {
//     callback: (value: string) => void;
//   }
  
  export default function AvatarMenu() {
    const avatarState = localStore((state: LocalState) => state.avatarState);
    return (
        <Menu shadow="md" width={200}>
        <Menu.Target>
            <Center style={{ marginRight: rem(50)}}>
                <span className={classes.linkLabel}>选择客户经理</span>
                <IconChevronDown size="0.9rem" stroke={1.5} />
            </Center>
        </Menu.Target>
  
        <Menu.Dropdown>
          <Menu.Item leftSection={<Avatar src="/avatars/customerManagerGirl.png" radius="xl" />}>
          <UnstyledButton
            // ref={ref}
            style={{
                padding: 'var(--mantine-spacing-md)',
                color: 'var(--mantine-color-text)',
                borderRadius: 'var(--mantine-radius-sm)',
            }}
            onClick={()=>{
              updateAgentAvatarMappingState({"CustomerManager": "customerManagerGirl"})
              updateAvatarStateState(true)
            }}
            >
            <Group>
                <div style={{ flex: 1 }}>
                <Text size="sm" fw={500}>
                    爱美丽
                </Text>

                <Text c="dimmed" size="xs">
                    客户经理
                </Text>
                </div>
            </Group>
        </UnstyledButton>
          </Menu.Item>
          <Menu.Item leftSection={<Avatar src="/avatars/customerManagerBoy.png" radius="xl" />}>
          <UnstyledButton
            // ref={ref}
            style={{
                padding: 'var(--mantine-spacing-md)',
                color: 'var(--mantine-color-text)',
                borderRadius: 'var(--mantine-radius-sm)',
            }}
            onClick={()=>{
              updateAgentAvatarMappingState({"CustomerManager": "customerManagerBoy"})
              updateAvatarStateState(true)
            }}
            >
            <Group>
                <div style={{ flex: 1 }}>
                <Text size="sm" fw={500}>
                    爱耍帅
                </Text>

                <Text c="dimmed" size="xs">
                    客户经理
                </Text>
                </div>
            </Group>
        </UnstyledButton>
          </Menu.Item>
          {avatarState && <Menu.Divider />}
          {avatarState && <Menu.Item
          color="red"
          leftSection={<IconRobotOff style={{ width: rem(14), height: rem(14) }} />}
          onClick={()=>{updateAvatarStateState(false)}}
        >
          关闭数字化身
        </Menu.Item>}
        </Menu.Dropdown>
      </Menu>
    );
  }