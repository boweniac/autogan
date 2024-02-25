import cx from 'clsx';
import { Box, Text, Group, rem, ScrollArea, Stack, Button, Flex, Menu, ActionIcon } from '@mantine/core';
import { IconDots, IconListSearch, IconPencil, IconPlus, IconTrash } from '@tabler/icons-react';
import classes from './LeftTableOfContents.module.css';
import { LocalState, localStore } from '@/stores/LocalStore';
import { AgentConversationMessage } from '@/stores/TypeAgentChat';
import { useRouter } from 'next/router';
import RenameModal from './RemoveModal/RenameModal';
import { useDisclosure } from '@mantine/hooks';
import { useEffect, useState } from 'react';
import DeleteModal from './DeleteModal/DeleteModal';

const links = [
  { label: 'Usage', link: '#usage', order: 1 },
  { label: 'Position and placement', link: '#position', order: 1 },
  { label: 'With other overlays', link: '#overlays', order: 1 },
  { label: 'Manage focus', link: '#focus', order: 1 },
  { label: 'Examples', link: '#1', order: 1 },
  { label: 'Show on focus', link: '#2', order: 2 },
  { label: 'Show on hover', link: '#3', order: 2 },
  { label: 'With form', link: '#4', order: 2 },
];

type LeftTableOfContentsProps = {
  conversationID: string | undefined;
}

export function LeftTableOfContents(props: LeftTableOfContentsProps) {
  const router = useRouter();
  const agentConversations = localStore((state: LocalState) => state.agentConversationList);
  const [openedRenameModal, { open: openRenameModal, close: closeRenameModal }] = useDisclosure(false);
  const [openedDeleteModal, { open: openDeleteModal, close: closeDeleteModal }] = useDisclosure(false);
  const [conversationID, setConversationID] = useState<string>("");
  const [title, setTitle] = useState<string | undefined>("");

  const [viewportHeight, setViewportHeight] = useState(0); // 初始值设置为0或合理的默认值

  useEffect(() => {
    // 这确保了window.innerHeight只在客户端获取
    setViewportHeight(window.innerHeight);

    const handleResize = () => {
      setViewportHeight(window.innerHeight);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const deleteConversation = () => {
    closeDeleteModal()
    router.push(`/agent`)
  }
  
  const items = agentConversations?.map((item) => {
    return (
    <Flex
      // gap="0"
      justify="space-between"
      align="center"
      direction="row"
      wrap="nowrap"
      key={item.id}
      className={cx(classes.link, { [classes.linkActive]: props.conversationID == item.id })}
    >
      <Box<'a'>
        component="a"
        // href={item.id}
        onClick={(event) => {
          event.preventDefault()
          router.push(`/agent/${item.id}`).then()
        }}
        // key={item.id}
        // className={cx(classes.link, { [classes.linkActive]: props.conversationID === item.id })}
        style={{ paddingLeft: "var(--mantine-spacing-md)", flexGrow: 1, cursor: 'pointer' }}
      >
        <Text 
        style={{ maxWidth: rem(170), overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
        size={rem(14)}
        >
        {item.title ? item.title : "New Chat"}
      </Text>
      </Box>
      {
        props.conversationID == item.id ? <Menu shadow="md" width={200}>
        <Menu.Target>
          {/* <Button>Toggle menu</Button> */}
          <ActionIcon variant="default" aria-label="Settings" style={{ border: 'none', background: 'transparent' }}>
            <IconDots style={{ width: '70%', height: '70%' }} stroke={1.5} />
          </ActionIcon>
        </Menu.Target>
  
        <Menu.Dropdown>
          <Menu.Item
            leftSection={<IconPencil style={{ width: rem(14), height: rem(14) }} />}
            onClick={() => {
              setConversationID(item.id)
              setTitle(item.title)
              openRenameModal()
            }}
          >
            Rename
          </Menu.Item>
          <Menu.Item
            color="red"
            leftSection={<IconTrash style={{ width: rem(14), height: rem(14) }} />}
            onClick={() => {
              setConversationID(item.id)
              setTitle(item.title)
              openDeleteModal()
            }}
          >
            Delete chat
          </Menu.Item>
        </Menu.Dropdown>
      </Menu> : <></>
      }
    </Flex>
  )});

  return (
            <Stack
                h={`calc(${viewportHeight}px)`}
                w={`${rem(220)})`}
            >
                <Button
                  variant="gradient"
                  gradient={{ from: 'blue', to: 'cyan', deg: 90 }}
                  rightSection={<IconPlus size={14} />}
                  style={{marginLeft: rem(15), marginRight: rem(15), marginTop: rem(10), marginBottom: rem(10)}}
                  onClick={()=>router.push("/agent").then()}
                >
                  New Chat
                </Button>
                <ScrollArea className={classes.scrollArea} w={rem(220)} type="never" scrollbars="y">
                {items}
              </ScrollArea>
              <RenameModal conversation_id={conversationID} title={title} opened={openedRenameModal} onClose={closeRenameModal}></RenameModal>
              <DeleteModal conversation_id={conversationID} title={title} opened={openedDeleteModal} onClose={closeDeleteModal} onDelete={deleteConversation}></DeleteModal>
            </Stack>

  );
}