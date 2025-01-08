import iconSuccess from '@/assets/icons/circle-check-solid.svg'
import iconError from '@/assets/icons/circle-xmark-solid.svg'
import { notification } from 'ant-design-vue'
import { h } from 'vue'

export const alertNotification = (message: string, description: string | any, status: boolean) => {
    notification.open({
        message: message,
        description: h('div', { innerHTML: description }),
        icon: h('img', {
            src: status ? iconSuccess : iconError,
            style: 'width: 24px; height: 24px;'
        }),
        duration: 3
    })

    // Example
    // alertNotification(
    //     'Thành công',
    //     `<p>Xóa thành công tài liệu <span class="font-semibold">${idDocument}</span></p>`,
    //     true
    // )
}
