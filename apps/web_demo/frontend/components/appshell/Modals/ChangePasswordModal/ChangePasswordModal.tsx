import { upperFirst, useDisclosure, useToggle } from '@mantine/hooks';
import { Modal, Button, Paper, Stack, TextInput, PasswordInput, Checkbox, Group, Anchor, Flex, rem, ActionIcon } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useEffect, useRef, useState } from 'react';
import { sendSmsAPI } from '@/api/user/user_send_sms';
import { IconSend } from '@tabler/icons-react';
import { notifications } from '@mantine/notifications';
import { loginAPI } from '@/api/user/user_login';
import { signupAPI } from '@/api/user/user_signup';
import { forgetPasswordAPI } from '@/api/user/user_forget_password';
import { changePhoneAPI } from '@/api/user/user_change_phone';
import { changePasswordAPI } from '@/api/user/user_change_password';

type ChangePhoneModalProps = {
    opened: boolean;
    close: ()=>void;
  }

export function ChangePasswordModal(props: ChangePhoneModalProps) {
    const [isSendDisabled, { open: sendDisabledOn, close: sendDisabledOff }] = useDisclosure(true); 
    const [isSending, { open: sendingStart, close: sendingEnd }] = useDisclosure(false); 
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);  // 注册过程loading
    const [countdown, setCountdown] = useState(60); // 发送验证码倒计时

    const form = useForm({
      initialValues: {
        phone: '',
        code: '',
        password: '',
      },
  
      validate: {
        phone: (val) => (/^1[3-9]\d{9}$/.test(val) ? null : '手机号格式错误'),
        code: (value) => {
          if (!value) {
            return null
          } else if (!/^[0-9]{6}$/.test(value)) {
            return '验证码格式错误'
          } else {
              return null
          }
        },
        password: (value) => {
          if (value.length < 8) {
              return '密码必须大于8位';
          } else if (!/\d/.test(value) || !/[a-zA-Z]/.test(value)) {
              return '密码必须为数字字母混合';
          } else {
              return null;
          }
        },
      },
    });

    const successClose = () => {
      notifications.show({
        message: "修改成功🎉",
        color: "green",
      });
      props.close()
    }

  return (
    <Modal opened={props.opened} onClose={props.close} title="修改密码">
        <form onSubmit={form.onSubmit(async (values) => {
          loadingStart()
          await changePasswordAPI(values.phone, values.code, values.password).then((r)=>{
            if (r) {
              successClose()
            }
          })
          loadingEnd()
        })}>
        <Stack>
          <TextInput
            required
            label="手机号"
            placeholder="请输入"
            value={form.values.phone}
            onChange={(event) => {
              const value = event.currentTarget.value
              if (/^1[3-9]\d{9}$/.test(value)) {
                sendDisabledOff()
              } else {
                sendDisabledOn()
              }

              form.setFieldValue('phone', value)}
            }
            error={form.errors.phone}
            radius="md"
          />

          <TextInput
            required
            label="验证码"
            placeholder="请输入"
            value={form.values.code}
            onChange={(event) => form.setFieldValue('code', event.currentTarget.value)}
            error={form.errors.code}
            radius="md"
            style={{ flex: 1 }}
            rightSection={
              <ActionIcon disabled={isSendDisabled || isSending} onClick={() => {
                sendingStart()
                sendSmsAPI(form.values.phone, 3)
                // 开始倒计时
                const intervalId = setInterval(() => {
                  setCountdown((prevCountdown) => prevCountdown - 1);
                  }, 1000);
                  // 倒计时结束后启用发送验证码按钮
                  setTimeout(() => {
                      clearInterval(intervalId);
                      sendingEnd()
                      setCountdown(60);
                  }, 60000);
                }}>{isSending ? `${countdown}` : <IconSend style={{ width: '70%', height: '70%' }} stroke={1.5} />}</ActionIcon>
            }
          />

          <PasswordInput
            required
            label="密码"
            description="密码必须大于 8 位，且为数字、字母混合"
            placeholder="请输入"
            value={form.values.password}
            onChange={(event) => form.setFieldValue('password', event.currentTarget.value)}
            error={form.errors.password && form.errors.password}
            radius="md"
          />
          
        </Stack>

        <Group justify="flex-end" mt="xl">
          <Button loading={isLoading} type="submit" radius="xl">
            提交
          </Button>
        </Group>
      </form>
      </Modal>
  );
}