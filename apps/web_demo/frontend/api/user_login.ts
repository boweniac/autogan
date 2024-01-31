import { updateUserPhoneState, updateUserTokenState } from "@/stores/LocalStoreActions"
import { postOpenRequestAPI } from "./request_open"

export const loginAPI = async (phone: string, password: string) =>  {
    const res = await postOpenRequestAPI("/open/user/login-password", {phone: phone, password: password})
    if (res) {
      updateUserPhoneState(phone)
      updateUserTokenState(res.token)
      return true
    }
    return false
  }