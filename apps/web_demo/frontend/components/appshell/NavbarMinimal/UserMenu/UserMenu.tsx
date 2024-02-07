import { LocalState, localStore } from "@/stores/LocalStore";
import { Menu, UnstyledButton, rem, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconClockRecord, IconCoinYen, IconCrown, IconDeviceMobile, IconKey, IconLogin, IconLogout, IconTrash, IconUser, IconUserPlus } from "@tabler/icons-react";
import { useRef, useState } from "react";
import { LoginModal } from "../../Modals/LoginModal/LoginModal";
import { closeLogInModal, openLogInModal, resetAgentConversationListState, resetAgentConversationMessageState, updateAgentAvatarMappingState, updateAvatarStateState, updateMuteStateState, updateUserPhoneState, updateUserStateState, updateUserTokenState } from "@/stores/LocalStoreActions";
import { notifications } from "@mantine/notifications";
import { useRouter } from "next/router";
import { getUserInfoAPI } from "@/api/user/user_get_user_info";
import { subscribeListAPI } from "@/api/user/user_subscribe_list";
import { unixTimestamp } from "./UserMenuUtil";
import { ChangePhoneModal } from "../../Modals/ChangePhoneModal/ChangePhoneModal";
import { ChangePasswordModal } from "../../Modals/ChangePasswordModal/ChangePasswordModal";

export default function UserMenu() {
    const userToken = localStore((state: LocalState) => state.userToken);
    const userPhone = localStore((state: LocalState) => state.userPhone);
    const openedLogInModal = localStore((state: LocalState) => state.openedLogInModal);
    // const [openedLogInModal, { open: openLogInModal, close: closeLogInModal }] = useDisclosure(false);
    const [openedChangePhoneModal, { open: openChangePhoneModal, close: closeChangePhoneModal }] = useDisclosure(false);
    const [openedChangePasswordModal, { open: openChangePasswordModal, close: closeChangePasswordModal }] = useDisclosure(false);
    const typeLogInModal = useRef("登录");
    const router = useRouter();
    const activePage = localStore((state: LocalState) => state.activePage);
    const [subscribe, setSubscribe] = useState([]);

    const sub = subscribe.length>0 ? subscribe.map((s: any) => {
      const ut = unixTimestamp(s.valid)
      return s.serviceId == "1" && <Menu.Label>会员到期时间: {ut}</Menu.Label>
  }) : (
      <Menu.Item leftSection={<IconCoinYen size="0.9rem" stroke={1.5} />} onClick={() => {router.push('/subscriber').then()}}>
          购买会员
      </Menu.Item>
  );

    return (
        <>
        <LoginModal type={typeLogInModal.current} opened={openedLogInModal} close={closeLogInModal}></LoginModal>
        <ChangePhoneModal opened={openedChangePhoneModal} close={closeChangePhoneModal}></ChangePhoneModal>
        <ChangePasswordModal opened={openedChangePhoneModal} close={closeChangePhoneModal}></ChangePasswordModal>
        <Menu 
          trigger="click" 
          openDelay={100} 
          closeDelay={400} 
          position="right-end"
          onOpen={() => {
            // onOpen()
            if (userToken) {
                getUserInfoAPI().then()
                subscribeListAPI().then((res) => {
                    setSubscribe(res ? res : [])
                })
            }
        }}
          >
        <Menu.Target>
            <UnstyledButton>
                <IconUser size="1.4rem" stroke={1.5} />
            </UnstyledButton>
        </Menu.Target>
        
        {userToken ? <Menu.Dropdown>
          <Menu.Label>{userPhone}</Menu.Label>
          {/* {sub}
          <Menu.Item leftSection={<IconClockRecord style={{ width: rem(14), height: rem(14) }} />}>
            历史订单
          </Menu.Item>
          <Menu.Label>账户</Menu.Label> */}
          <Menu.Item leftSection={<IconDeviceMobile style={{ width: rem(14), height: rem(14) }} />} onClick={()=>{
            openChangePhoneModal()
          }}>
            修改手机
          </Menu.Item>
          <Menu.Item leftSection={<IconKey style={{ width: rem(14), height: rem(14) }} />} onClick={()=>{
            openChangePasswordModal()
          }}>
            修改密码
          </Menu.Item>
          <Menu.Divider />
          <Menu.Item
            color="red"
            leftSection={<IconLogout style={{ width: rem(14), height: rem(14) }} />} onClick={()=>{
              updateUserTokenState("")
              updateUserPhoneState("")
              updateUserStateState(0)
              updateAvatarStateState(true)
              updateMuteStateState(false)
              updateAgentAvatarMappingState({"CustomerManager": "customerManagerGirl"})
              resetAgentConversationListState()
              resetAgentConversationMessageState()
              router.push(activePage).then(()=>{
                notifications.show({
                  message: "已成功退出登录",
                  color: "green",
                });
              })
            }}
          >
            退出登录
          </Menu.Item>
        </Menu.Dropdown> : <Menu.Dropdown>
          {/* <Menu.Label>登录/注册</Menu.Label> */}
          <Menu.Item leftSection={<IconLogin style={{ width: rem(14), height: rem(14) }} />} onClick={()=>{
            typeLogInModal.current = "登录"
            openLogInModal()
          }}>
            登录
          </Menu.Item>
          <Menu.Item leftSection={<IconUserPlus style={{ width: rem(14), height: rem(14) }} />} onClick={()=>{
            typeLogInModal.current = "注册"
            openLogInModal()
          }}>
            注册
          </Menu.Item>
        </Menu.Dropdown>}
      </Menu>
        </>
        
    );
  }