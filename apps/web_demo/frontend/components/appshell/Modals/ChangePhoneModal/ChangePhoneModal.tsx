import { upperFirst, useDisclosure, useToggle } from '@mantine/hooks';
import { Modal, Button, Paper, Stack, TextInput, PasswordInput, Checkbox, Group, Anchor, Flex, rem, ActionIcon } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useEffect, useRef, useState } from 'react';
import { sendSmsAPI } from '@/api/user_send_sms';
import { IconSend } from '@tabler/icons-react';
import { notifications } from '@mantine/notifications';
import { loginAPI } from '@/api/user_login';
import { signupAPI } from '@/api/user_signup';
import { forgetPasswordAPI } from '@/api/user_forget_password';
import { changePhoneAPI } from '@/api/user_change_phone';

type ChangePhoneModalProps = {
    opened: boolean;
    close: ()=>void;
  }

export function ChangePhoneModal(props: ChangePhoneModalProps) {
    const [isSendDisabled, { open: sendDisabledOn, close: sendDisabledOff }] = useDisclosure(true); 
    const [isSending, { open: sendingStart, close: sendingEnd }] = useDisclosure(false); 
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);  // 注册过程loading
    const [countdown, setCountdown] = useState(60); // 发送验证码倒计时

    const form = useForm({
      initialValues: {
        phone: '',
        code: '',
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
    <Modal opened={props.opened} onClose={props.close} title="修改手机">
        <form onSubmit={form.onSubmit(async (values) => {
          loadingStart()
          await changePhoneAPI(values.phone, values.code).then((r)=>{
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