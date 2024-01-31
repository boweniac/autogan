import { updateUserPhoneState, updateUserTokenState } from "@/stores/LocalStoreActions"
import { postOpenRequestAPI } from "./request_open"
import { postRequestAPI } from "./request"

export const changePasswordAPI = async (phone: string, code: string, password: string) =>  {
    const res = await postRequestAPI("/user/change-password", {phone: phone, code: code, password: password})
    if (res) {
      updateUserTokenState(res.token)
      return true
    }
    return false
  }