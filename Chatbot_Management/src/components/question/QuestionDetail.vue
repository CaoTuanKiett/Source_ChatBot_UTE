<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'
import { Button, Drawer, Input, Textarea } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, reactive, ref } from 'vue'

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL
const VITE_LOGO_SCHOOL_URL = import.meta.env.VITE_LOGO_SCHOOL_URL

const props = defineProps({
    questionDetail: Object,
    openPannel: Boolean,
    handleopenPannel: Function,
    fetchDataQuestion: Function
})

const question = reactive({
    idQuestion: 0,
    fullName: '',
    question: '',
    answer: '',
    email: '',
    status: '',
    sentTime: '',
    answeredBy: '',
    answeredTime: '',
    chatBotID: 0,
    chatbotName: ''
})

const questionStatus = ['Chưa xử lý', 'Đã xử lý']
const localOpen = ref<boolean>(props.openPannel)
const isLoadingUpdate = ref<boolean>(false)

onMounted(() => {
    convertDataQuestion()
    console.log('auth', auth.payload)
})

const convertDataQuestion = () => {
    if (props.questionDetail) {
        question.idQuestion = props.questionDetail.idQuestion
        question.fullName = props.questionDetail.fullName
        question.question = props.questionDetail.question
        question.answer = props.questionDetail.answer
        question.email = props.questionDetail.email
        question.status = props.questionDetail.status
        question.sentTime = props.questionDetail.sentTime
        question.answeredBy = props.questionDetail.answeredBy
        question.answeredTime = props.questionDetail.answeredTime
        question.chatBotID = props.questionDetail.chatBotID
        question.chatbotName = props.questionDetail.chatbotName
    }
}

// Handle Drawer open/close changes
const afterOpenChange = (bool: boolean) => {
    console.log('afterOpenChange', bool)
}

const handleClose = () => {
    localOpen.value = false
    props.handleopenPannel && props.handleopenPannel(false)

    //Reser user
    resetQuestion()
}

const handleSave = async () => {
    console.log('handleSave', question)
    try {
        isLoadingUpdate.value = true

        const bodyTemplateEmail = `
        <div>
            <p style="margin-bottom: 12px">
                Chào bạn
                <span style="font-weight: 600">${question.fullName}</span>,
            </p>
            <p>Cảm ơn bạn đã gửi câu hỏi đến chúng tôi.</p>
            <p style="margin-bottom: 4px">Dưới đây là câu trả lời cho câu hỏi của bạn:</p>
            <p style="font-weight: 600">Câu hỏi:</p>
            <p style="margin-bottom: 4px">${question.question}</p>
            <p style="font-weight: 600">Trả lời:</p>
            <p style="margin-bottom: 12px">${question.answer}</p>
            <p style="font-weight: 500; font-style: italic">Chúc bạn một ngày tốt lành!</p>

            <div
                style="
                    display: flex;
                    align-items: center;
                    margin-top: 16px;
                    border-top-width: 1px;
                    border-color: #214180;
                    padding-top: 16px;
                "
            >
                <img
                    src="https://res.cloudinary.com/dqo8ven0y/image/upload/v1735548137/chatbot/logo-truong-250_zlm4ys.png"
                    alt="logo-truong-250.png"
                    style="width: 54px; height: 54px; object-fit: cover; margin-right: 16px"
                />
                <div>
                    <h1 style="font-size: 14px; font-weight: 500">
                        Trường Đại học Sư phạm Kỹ thuật - Đại học Đà Nẵng
                    </h1>
                    <div style="display: flex; align-items: center; gap: 4px">
                        <p style="font-size: 12px">
                            <span style="font-weight: 500">Trụ sở:</span> 48 Cao Thắng - Hải Châu -
                            Đà Nẵng.
                        </p>
                        <p style="font-size: 12px">
                            <span style="font-weight: 500">Điện thoại:</span> 0236.3530103 -
                            0236.3835705
                        </p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 4px">
                        <p style="font-size: 12px">
                            <span style="font-weight: 500">Email:</span> tuyensinh@ute.udn.vn
                        </p>
                        <p style="font-size: 12px">
                            <span style="font-weight: 500">Website::</span>
                            <a href="https://ute.udn.vn/default.aspx"
                                >https://ute.udn.vn/default.aspx</a
                            >
                        </p>
                    </div>
                </div>
            </div>
        </div>
        `

        const subjectEmail = `[UTE-DN] Câu trả lời cho câu hỏi của bạn`

        const sendMail = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/send-email`, {
            email: question.email,
            subject: subjectEmail,
            body: bodyTemplateEmail
        })

        if (sendMail.status === 200) {
            console.log('sendMail', sendMail.data.message)
        }

        const response = await axios.put(
            `${VITE_API_URL}/${VITE_API_VERSION}/question/${question.idQuestion}`,
            {
                answer: question.answer,
                answeredBy: auth.payload?.username || 'Admin'
            }
        )

        if (response.status === 200) {
            console.log('response', response.data)
            props.fetchDataQuestion && props.fetchDataQuestion()
            alertNotification(
                'Thành công',
                `<p>Trả lời thành công câu hỏi <span class="font-semibold">${question.idQuestion}</span></p>`,
                true
            )
            handleClose()
        } else {
            alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
        }
    } catch (error) {
        console.log('handleSave error', error)
        alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
    } finally {
        isLoadingUpdate.value = false
    }
}

// Reset question
const resetQuestion = () => {
    question.idQuestion = 0
    question.fullName = ''
    question.question = ''
    question.answer = ''
    question.email = ''
    question.status = ''
    question.sentTime = ''
    question.answeredBy = ''
    question.answeredTime = ''
    question.chatBotID = 0
    question.chatbotName = ''
}
</script>

<template>
    <Drawer
        title="Chi tiết câu hỏi"
        placement="right"
        v-model:open="localOpen"
        width="700"
        @afterOpenChange="afterOpenChange"
        @close="handleClose"
        :footer-style="{ textAlign: 'right' }"
        autofocus:false
        :maskClosable="false"
        class="question-detail"
    >
        <div>
            <div class="flex flex-col mb-4">
                <label for="name" class="pb-2 font-medium">Họ và tên:</label>
                <Input
                    readonly
                    v-model:value="question.fullName"
                    placeholder="Basic usage"
                    id="name"
                    class="h-10 input-readonly"
                >
                    <template #prefix>
                        <img
                            src="/icons/user-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-[14px] mr-2"
                        />
                    </template>
                </Input>
            </div>
            <div class="flex flex-col mb-4">
                <label for="email" class="pb-2 font-medium">Email:</label>
                <Input
                    readonly
                    v-model:value="question.email"
                    placeholder="Basic usage"
                    id="email"
                    class="h-10 input-readonly"
                    type="email"
                >
                    <template #prefix>
                        <img
                            src="/icons/envelope-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-[15px] mr-2"
                        />
                    </template>
                </Input>
            </div>

            <div class="flex flex-col mb-4">
                <label for="role" class="pb-2 font-medium">Câu hỏi:</label>
                <Textarea
                    readonly
                    v-model:value="question.question"
                    placeholder="Câu hỏi"
                    :auto-size="{ minRows: 4, maxRows: 5 }"
                    class="input-readonly"
                />
            </div>
            <div class="flex flex-col mb-4">
                <label for="role" class="pb-2 font-medium">Câu trả lời:</label>
                <Textarea
                    :disabled="question.status == questionStatus[1]"
                    v-model:value="question.answer"
                    placeholder="Câu trả lời"
                    :auto-size="{ minRows: 7, maxRows: 5 }"
                />
            </div>
            <div v-if="question.answeredBy">
                <p class="text-sm italic">
                    Người trả lời:
                    <span class="text-base font-medium not-italic pl-1">{{
                        question.answeredBy
                    }}</span>
                </p>
                <p class="text-sm italic">
                    Thời gian:
                    <span class="text-base font-medium not-italic pl-1">{{
                        question.sentTime
                    }}</span>
                </p>
            </div>
        </div>
        <template #footer>
            <Button
                v-if="question.status == questionStatus[1]"
                type="default"
                @click="handleClose"
                class="mr-3 h-10 font-semibold"
                >Cancel</Button
            >
            <Button v-else type="default" @click="handleClose" class="mr-3 h-10 font-semibold">
                Hủy
            </Button>
            <Button
                :loading="isLoadingUpdate"
                :disabled="question.status == questionStatus[1]"
                type="primary"
                @click="handleSave"
                class="w-44 h-10 font-semibold"
            >
                Gửi câu trả lời
            </Button>
        </template>
    </Drawer>
</template>

<style>
.question-detail .input-readonly {
    cursor: not-allowed !important;
}

.question-detail .ant-input-disabled {
    color: black !important;
}
</style>
