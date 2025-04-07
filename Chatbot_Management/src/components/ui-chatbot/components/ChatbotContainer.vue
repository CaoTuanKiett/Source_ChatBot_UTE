<script setup lang="ts">
import { alertNotification } from '@/utils/notification'
import axios from 'axios'
import { nextTick, onMounted, ref } from 'vue'

import Footer from '@/components/ui-chatbot/components/chatbot/Footer.vue'
import Header from '@/components/ui-chatbot/components/chatbot/Header.vue'
import ItemMessage from '@/components/ui-chatbot/components/chatbot/ItemMessage.vue'
import AppLoading from '@/components/ui-chatbot/components/common/AppLoading.vue'
import type { CustomJwtPayload } from '@/utils/config'
import { decodeToken } from '@/utils/config'
// import dataFake from '../api/dataFake.json';

import type { Message } from '@/interfaceConfig'
import FormFeedback from './chatbot/FormFeedback.vue'
import FormQuestion from './chatbot/FormQuestion.vue'

const props = defineProps<{
    apiEndpoint: string
    chatbotToken: string
    textShowForm: string
    textShowFormFeedback: string
}>()

const isLoading = ref<boolean>(false)
const isLoadResponse = ref<boolean>(false)

const data = ref<Message[]>([])
const scrollToEnd = ref<HTMLElement | null>(null)
const isShowFormQuestion = ref<boolean>(false)
const isShowFeedback = ref<boolean>(false)
const isButtonVisible = ref(false)
const chatContainer = ref<HTMLElement | null>(null)
const threadId = ref<number>(0)

const dataMess = ref<Message[]>([])
const chatbotInfor = ref<CustomJwtPayload>({
    created_at: '',
    description: '',
    folder_id: '',
    id: 0,
    name: '',
    school_id: 0
})

const fetchMessages = async (idChatBot: number) => {
    isLoading.value = true
    try {
        const response = await axios.get(
            `${props.apiEndpoint}/messages/${threadId.value}/${idChatBot}`
        )
        if (response.status !== 200) {
            console.error('Error', response.status)
            return
        }

        data.value = response.data

        // data.value = await response.data;

        await nextTick()

        setTimeout(() => {
            scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
        }, 10)
    } catch (error) {
        console.error(error)
    } finally {
        isLoading.value = false
    }
}

onMounted(async () => {
    const decodedToken = decodeToken(props.chatbotToken)
    if (decodedToken) {
        chatbotInfor.value = decodedToken
    }

    threadId.value =
        JSON.parse(localStorage.getItem('inForThread') || '[]').find(
            (item: any) => item.chatbotId === chatbotInfor.value.id
        )?.threadId || 0

    console.log('threadId', threadId.value)

    await fetchMessages(chatbotInfor.value.id)
    localStorage.setItem('dataMess', JSON.stringify(data.value))

    dataMess.value = data.value
    // console.log('dataMess', dataMess.value);

    if (dataMess.value.length === 0) {
        handleSendOneMessage({
            id: Math.random().toString(36).substr(2, 9),
            content: 'Xin chào, tôi có thể giúp gì cho bạn?',
            sender: 'Chatbot',
            sentTime: new Date().toISOString()
        })
    }

    if (chatContainer.value) {
        chatContainer.value.addEventListener('scroll', handleScroll)
    }
})

const handleResponseChat = async (valueInput: string) => {
    if (!valueInput.trim()) {
        console.log('Không được để trống')
        return
    }

    handleCancelFeedback()
    handleCancelQuestion()

    // Hiển thị trạng thái loading
    isLoadResponse.value = true

    // Cuộn đến cuối màn hình chat
    setTimeout(() => {
        scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
    }, 10)

    // Tạo message của người dùng
    const userMessage: Message = {
        id: Math.random().toString(36).substr(2, 9),
        content: valueInput.trim(),
        sender: 'user',
        sentTime: new Date().toISOString()
    }

    // Lấy danh sách đoạn chat từ localStorage
    let chatHistory: Message[] = JSON.parse(localStorage.getItem('dataMess') || '[]')

    // Thêm message người dùng vào lịch sử
    chatHistory.push(userMessage)
    localStorage.setItem('dataMess', JSON.stringify(chatHistory))

    // Cập nhật giao diện
    dataMess.value = chatHistory

    try {
        // Gửi yêu cầu đến API
        const response = await axios.post(`${props.apiEndpoint}/chat`, {
            content: valueInput.trim(),
            sender: 'user',
            chatbotId: chatbotInfor.value.id,
            threadId: threadId.value
        })

        if (response.data) {
            // Thêm phản hồi từ chatbot vào lịch sử

            chatHistory.push(response.data)
            localStorage.setItem('dataMess', JSON.stringify(chatHistory))

            // Lưu threadId vào localStorage
            handleSaveInforThread(response.data.threadId)

            // Cập nhật giao diện
            dataMess.value = chatHistory

            if (String(response.data.content).trim().includes(String(props.textShowForm).trim())) {
                isShowFormQuestion.value = true
            }

            if (
                String(response.data.content)
                    .trim()
                    .includes(String(props.textShowFormFeedback).trim())
            ) {
                isShowFeedback.value = true
            }

            // Cuộn xuống cuối màn hình sau khi nhận phản hồi
            setTimeout(() => {
                scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
            }, 10)
        }
    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu đến API:', error)
    } finally {
        // Tắt trạng thái loading
        isLoadResponse.value = false
    }
}

const handleSaveInforThread = (threadId: number) => {
    // Dữ liệu hiện tại trong localStorage
    const currentData = JSON.parse(localStorage.getItem('inForThread') || '[]')

    // Thông tin mới cần lưu
    const newThreadInfo = {
        chatbotId: chatbotInfor.value.id, // ID của chatbot
        threadId: threadId // ID của thread
    }

    // Kiểm tra xem chatbotId đã tồn tại hay chưa
    const existingIndex = currentData.findIndex(
        (item: any) => item.chatbotId === newThreadInfo.chatbotId
    )
    if (existingIndex !== -1) {
        // Nếu tồn tại, cập nhật threadId
        currentData[existingIndex].threadId = newThreadInfo.threadId
    } else {
        // Nếu chưa tồn tại, thêm mới
        currentData.push(newThreadInfo)
    }

    // Lưu lại dữ liệu vào localStorage
    localStorage.setItem('inForThread', JSON.stringify(currentData))
}

const handleSendQuestion = async (name: string, email: string, question: string) => {
    try {
        const res = await axios.post(`${props.apiEndpoint}/question`, {
            fullName: name,
            email: email,
            question: question,
            chatBotID: chatbotInfor.value.id
        })

        if (res.status === 200) {
            alertNotification(
                'Gửi câu hỏi thành công',
                `<p>Cảm ơn bạn đã gửi câu hỏi, chúng tôi sẽ trả lời bạn sớm nhất có thể!</p>`,
                true
            )
            handleCancelQuestion()
            handleSendOneMessage({
                id: Math.random().toString(36).substr(2, 9),
                content: 'Bạn cần hỗ trợ thêm thông tin gì nữa không?',
                sender: 'Chatbot',
                sentTime: new Date().toISOString()
            })
        } else {
            alertNotification('Gửi câu hỏi thất bại', `<p>Vui lòng thử lại!</p>`, false)
        }
    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu đến API:', error)
        alertNotification('Gửi câu hỏi thất bại', `<p>Vui lòng thử lại!</p>`, false)
    }
}

const handleOpenQuestion = () => {
    isShowFormQuestion.value = true
    setTimeout(() => {
        scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
    }, 10)
}

const handleCancelQuestion = () => {
    isShowFormQuestion.value = false
    console.log('handleCancelQuestion')
}

const handleSendFeedback = async (feedbackDetail: any) => {
    console.log(
        'handleSendFeedback',
        feedbackDetail.fullName,
        feedbackDetail.email,
        feedbackDetail.content,
        feedbackDetail.feedbackType
    )
    try {
        const res = await axios.post(`${props.apiEndpoint}/feedback`, {
            fullName: feedbackDetail.fullName,
            email: feedbackDetail.email,
            content: feedbackDetail.content,
            feedbackType: feedbackDetail.feedbackType,
            chatBotID: chatbotInfor.value.id
        })

        if (res.status === 200) {
            alertNotification(
                'Gửi góp ý thành công',
                `<p>Cảm ơn bạn đã gửi góp ý, chúng tôi sẽ cải thiện dịch vụ tốt hơn</p>`,
                true
            )
            handleCancelFeedback()
            handleSendOneMessage({
                id: Math.random().toString(36).substr(2, 9),
                content: 'Nếu không còn câu hỏi nào thì tạm biệt và hẹn gặp lại bạn sau!',
                sender: 'Chatbot',
                sentTime: new Date().toISOString()
            })
        } else {
            alertNotification('Gửi góp ý thất bại', `<p>Vui lòng thử lại!</p>`, false)
        }
    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu đến API:', error)
        alertNotification('Gửi góp ý thất bại', `<p>Vui lòng thử lại!</p>`, false)
    }
}

const handleOpenFeedback = () => {
    isShowFeedback.value = true
    setTimeout(() => {
        scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
    }, 10)
}

const handleCancelFeedback = () => {
    isShowFeedback.value = false
    console.log('handleCancelFeedback')
}

const handleSendOneMessage = async (message: Message) => {
    try {
        const response = await axios.post(`${props.apiEndpoint}/message`, {
            content: message.content,
            sender: message.sender,
            chatbotId: chatbotInfor.value.id,
            threadId: threadId.value
        })

        if (response.status === 200) {
            const chatHistory: Message[] = JSON.parse(localStorage.getItem('dataMess') || '[]')
            chatHistory.push(response.data)
            localStorage.setItem('dataMess', JSON.stringify(chatHistory))
            dataMess.value = chatHistory

            handleSaveInforThread(response.data.threadId)

            setTimeout(() => {
                scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
            }, 10)
        }
    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu đến API:', error)
    }
}

const handleScroll = () => {
    if (chatContainer.value) {
        const isAtBottom =
            chatContainer.value.scrollHeight - chatContainer.value.scrollTop >=
            chatContainer.value.clientHeight + 200
        isButtonVisible.value = isAtBottom
    }
}

const scrollToBottom = () => {
    scrollToEnd.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
    <div
        class="chatbot-container bg-white w-[420px] h-[600px] rounded-lg overflow-hidden flex flex-col justify-between text-black"
    >
        <Header
            :handleOpenQuestion="handleOpenQuestion"
            :handleOpenFeedback="handleOpenFeedback"
            :apiEndpoint="props.apiEndpoint"
            :chatbotToken="props.chatbotToken"
        />
        <div v-if="isLoading" class="flex justify-center items-center">
            <img src="/icons/loading.svg" alt="loading" class="w-28 h-28" />
        </div>
        <div
            v-else
            ref="chatContainer"
            class="chatbot-content relative h-full p-3 pr-4 pl-5 overflow-y-scroll"
        >
            <ItemMessage
                v-for="message in dataMess"
                :key="message.id"
                :sender="message.sender"
                :message="message"
            />
            <div
                v-if="isLoadResponse"
                class="w-fit relative max-w-96 bg-gray-300 p-2 pr-3 rounded-lg mt-[6px]"
            >
                <AppLoading />
                <span class="after-message-bot"></span>
            </div>

            <div v-if="isShowFormQuestion" class="w-full flex justify-center items-center my-5">
                <FormQuestion
                    :handleSendQuestion="handleSendQuestion"
                    :handleCancelQuestion="handleCancelQuestion"
                />
            </div>
            <div v-if="isShowFeedback" class="w-full flex justify-center items-center my-5">
                <FormFeedback
                    :handleSendFeedback="handleSendFeedback"
                    :handleCancelFeedback="handleCancelFeedback"
                />
            </div>
            <div ref="scrollToEnd" class="relative"></div>
        </div>
        <button
            v-if="isButtonVisible"
            @click="scrollToBottom"
            class="absolute bottom-[90px] left-1/2 transition-all transform -translate-x-1/2 bg-blue-400 shadow-lg text-white p-2 rounded-full hover:bg-blue-300 border-[1px] border-blue-400 hover:border-blue-700"
        >
            <img src="/icons/chevron-down-solid.svg" alt="chevron-down-solid.svg" class="w-5 h-5" />
        </button>
        <Footer :handleResponseChat="handleResponseChat" :isLoadResponse="isLoadResponse" />
    </div>
</template>

<style scoped>
.chatbot-container {
    /* box-shadow: rgba(0, 0, 0, 0.2) 0px 0px 45px, rgba(0, 0, 0, 0.1) 0px 0px 34px; */
    box-shadow: rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px;
}

.chatbot-content {
    --sb-track-color: #ffffff;
    --sb-thumb-color: #151377;
    --sb-size: 6px;
    position: relative !important;
}

.chatbot-content::-webkit-scrollbar {
    width: var(--sb-size);
}

.chatbot-content::-webkit-scrollbar-track {
    background: var(--sb-track-color);
    border-radius: 12px;
}

.chatbot-content::-webkit-scrollbar-thumb {
    background: var(--sb-thumb-color);
    border-radius: 12px;
}

@supports not selector(::-webkit-scrollbar) {
    .chatbot-content {
        scrollbar-color: var(--sb-thumb-color) var(--sb-track-color);
    }
}

.chatbot-container .form-question {
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
}

.after-message-bot {
    position: absolute;
    left: -7px;
    bottom: 0;
    border-bottom: 17px solid rgb(209 213 219 / var(--tw-bg-opacity));
    border-left: 13px solid transparent;
    /* border-end-start-radius: 0px;
  border-start-start-radius: 18px; */
}
</style>
