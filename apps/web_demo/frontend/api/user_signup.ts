import { updateUserPhoneState, updateUserTokenState } from "@/stores/LocalStoreActions"
import { postOpenRequestAPI } from "./request_open"

export const signupAPI = async (phone: string, code: string, password: string) =>  {
    const res = await postOpenRequestAPI("/open/user/signup-phone", {phone: phone, code: code, password: password})
    if (res) {
      updateUserPhoneState(phone)
      updateUserTokenState(res.token)
      return true
    }
    return false
  }