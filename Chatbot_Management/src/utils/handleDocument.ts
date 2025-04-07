import axios from 'axios'
import { alertNotification } from './notification'

export const removeDocument = async (
    idDocument: number,
    isLoadingDelete: any,
    fetchData: Function
) => {
    const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
    const baseURL = import.meta.env.VITE_API_URL

    const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`
    isLoadingDelete.value = true
    try {
        const response = await axios.delete(`${VITE_API_URL}/document/${idDocument}`)
        console.log('response', response)
        if (response.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Xóa thành công tài liệu <span class="font-semibold">${idDocument}</span></p>`,
                true
            )
        } else {
            alertNotification(
                'Thất bại',
                `<p>Xóa tài liệu <span class="font-semibold">${idDocument}</span> thất bại</p>`,
                false
            )
        }
        fetchData()
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingDelete.value = false
    }
}
