<script setup lang="ts">
import type { CustomJwtPayload } from '@/utils/config'
import { decodeToken } from '@/utils/config'
import axios from 'axios'
import { onMounted, ref } from 'vue'

import { alertNotification } from '@/utils/notification'
import { Tooltip } from 'ant-design-vue'

const props = defineProps<{
    handleOpenQuestion: () => void
    handleOpenFeedback: () => void
    apiEndpoint: string
    chatbotToken: string
}>()

const nameChatbot = ref('')

const inForSchool = ref({
    schoolName: '',
    schoolCode: '',
    description: '',
    avatarUrl: '',
    dateEstablished: '',
    address: '',
    phone: '',
    email: '',
    website: '',
    createdTime: '',
    logo: ''
})

const getInForSchool = async (idSchool: number) => {
    try {
        const res = await axios.get(`${props.apiEndpoint}/school/${idSchool}`)
        if (res.status === 200) {
            inForSchool.value = res.data
        }
    } catch (error: any) {
        console.log(error)
        alertNotification('Thất bại', `${error.response.data.detail}`, false)
    }
}

const getInForChatbot = async (idChatBot: number) => {
    try {
        const res = await axios.get(`${props.apiEndpoint}/chatbot/${idChatBot}`)
        if (res.status === 200) {
            console.log('getInForChatbot', res.data)
            nameChatbot.value = res.data.chatBotName
        }
    } catch (error: any) {
        console.log(error)
        alertNotification('Thất bại', `${error.response.data.detail}`, false)
    }
}

onMounted(() => {
    const dataInfor: CustomJwtPayload | null = decodeToken(props.chatbotToken)

    if (dataInfor && dataInfor.school_id !== undefined) {
        getInForSchool(dataInfor.school_id)
        getInForChatbot(dataInfor.id)
    } else {
        console.error('ID Trường không tồn tại')
    }
})
</script>

<template>
    <div class="header-chatbot bg-white flex items-center justify-between p-3 px-4">
        <div class="flex">
            <img
                :src="inForSchool?.avatarUrl || '/images/logo-truong-250.png'"
                alt="avt"
                class="w-[52px] h-[52px] rounded-full mr-3 object-cover"
            />
            <div class="text-black flex flex-col justify-center items-start">
                <Tooltip color="#ccc">
                    <template #title>
                        <span class="text-xs text-black">{{ inForSchool?.schoolName }}</span>
                    </template>
                    <h2 class="font-bold text-base truncate max-w-[254px]">
                        {{ inForSchool?.schoolName }}
                    </h2>
                </Tooltip>
                <p class="text-xs pt-[2px]">{{ nameChatbot }}</p>
            </div>
        </div>
        <div class="flex items-center gap-3">
            <Tooltip color="#ccc">
                <template #title>
                    <span class="text-xs text-black">Đặt câu hỏi</span>
                </template>
                <button
                    class="flex items-center hover:opacity-60 hover:border-slate-500 transition-all duration-300"
                    @click="props.handleOpenQuestion"
                >
                    <img
                        src="/icons/circle-question-regular.svg"
                        alt="help"
                        class="w-6 h-6 cursor-pointer hover:opacity-50"
                    />
                </button>
            </Tooltip>

            <Tooltip color="#ccc">
                <template #title>
                    <span class="text-xs text-black">Góp ý</span>
                </template>
                <button
                    class="flex items-center hover:opacity-60 hover:border-slate-500 transition-all duration-300"
                    @click="props.handleOpenFeedback"
                >
                    <img
                        src="/icons/message-regular.svg"
                        alt="feedback"
                        class="w-6 h-6 cursor-pointer hover:opacity-50"
                    />
                </button>
            </Tooltip>
            <!-- <el-tooltip placement="top-start" content="Hỗ trợ 24/7" effect="light">
                <button @click="props.handleOpenFeedback">
                    <img
                        src="/icons/headset-solid.svg"
                        alt="support"
                        class="w-6 h-6 cursor-pointer hover:opacity-50"
                    />
                </button>
            </el-tooltip> -->
        </div>
    </div>
</template>

<style scoped>
.header-chatbot {
    box-shadow: rgba(0, 0, 0, 0.04) 0px 1px 1px, rgba(0, 0, 0, 0.04) 0px 2px 2px,
        rgba(0, 0, 0, 0.04) 0px 4px 4px, rgba(0, 0, 0, 0.04) 0px 8px 8px,
        rgba(0, 0, 0, 0.04) 0px 16px 16px;
}
</style>
