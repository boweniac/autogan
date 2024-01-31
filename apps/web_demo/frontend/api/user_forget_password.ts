import { updateUserPhoneState, updateUserTokenState } from "@/stores/LocalStoreActions"
import { postOpenRequestAPI } from "./request_open"

export const forgetPasswordAPI = async (phone: string, code: string, password: string) =>  {
    const res = await postOpenRequestAPI("/open/user/forget-password", {phone: phone, code: code, password: password})
    if (res) {
      updateUserPhoneState(phone)
      updateUserTokenState(res.token)
      return true
    }
    return false
  }