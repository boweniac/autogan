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

type LoginModalProps = {
    type: string;
    opened: boolean;
    close: ()=>void;
  }

export function LoginModal(props: LoginModalProps) {
    const [type, setType] = useState<string>("");
    const [isSendDisabled, { open: sendDisabledOn, close: sendDisabledOff }] = useDisclosure(true); 
    const [isSending, { open: sendingStart, close: sendingEnd }] = useDisclosure(false); 
    const [isLoading, { open: loadingStart, close: loadingEnd }] = useDisclosure(false);  // 注册过程loading
    const [countdown, setCountdown] = useState(60); // 发送验证码倒计时
    const codeType = useRef(0);

    useEffect(() => {
      setType(props.type)
  }, [props.type]);

    const form = useForm({
      initialValues: {
        phone: '',
        code: '',
        password: '',
        terms: true,
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
        message: type + "成功🎉",
        color: "green",
      });
      props.close()
    }

  return (
    <Modal opened={props.opened} onClose={props.close} title={type}>
        <form onSubmit={form.onSubmit(async (values) => {
          loadingStart()
          if (type == '登录') {
            await loginAPI(values.phone, values.password).then((r)=>{
              if (r) {
                successClose()
              }
            })
          } else if (type == '注册') {
            await signupAPI(values.phone, values.code, values.password).then((r)=>{
              if (r) {
                successClose()
              }
            })
          } else {
            await forgetPasswordAPI(values.phone, values.code, values.password).then((r)=>{
              if (r) {
                successClose()
              }
            })
          }
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

          {type != '登录' && (
            <TextInput
            required={type != '登录'}
            label="验证码"
            placeholder="请输入"
            value={form.values.code}
            onChange={(event) => form.setFieldValue('code', event.currentTarget.value)}
            error={form.errors.code}
            radius="md"
            style={{ flex: 1 }}
            rightSection={
              <ActionIcon disabled={isSendDisabled || isSending} onClick={() => {
                if (type === "注册") {
                  codeType.current =  0
                } else {
                  codeType.current =  2
                }
                sendingStart()
                sendSmsAPI(form.values.phone, codeType.current)
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
          )}
          
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

          {type === '注册' && (
            <Checkbox
              label="同意用户协议"
              checked={form.values.terms}
              onChange={(event) => form.setFieldValue('terms', event.currentTarget.checked)}
            />
          )}
          {type === '登录' && (
            <Group justify="flex-end">
<Anchor component="button" type="button" c="dimmed" onClick={() => setType("重置密码")} size="xs">
            忘记密码？
          </Anchor>
            </Group>
          )}
        </Stack>

        <Group justify="space-between" mt="xl">
        {type === '注册'
              ? <Anchor component="button" type="button" c="dimmed" onClick={() => setType("登录")} size="xs">
              已经有账户了? 现在登录
            </Anchor>
              : <Anchor component="button" type="button" c="dimmed" onClick={() => setType("注册")} size="xs">
              还没有账户? 现在注册
            </Anchor>}
          <Button loading={isLoading} type="submit" radius="xl">
            {type}
          </Button>
        </Group>
      </form>
      </Modal>
  );
}