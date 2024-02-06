import { updateUserPhoneState, updateUserTokenState } from "@/stores/LocalStoreActions"
import { postOpenRequestAPI } from "../request_open"
import { postRequestAPI } from "../request"

export const changePhoneAPI = async (phone: string, code: string) =>  {
    const res = await postRequestAPI("/user/change-phone", {phone: phone, code: code})
    if (res) {
      updateUserPhoneState(phone)
      updateUserTokenState(res.token)
      return true
    }
    return false
  }