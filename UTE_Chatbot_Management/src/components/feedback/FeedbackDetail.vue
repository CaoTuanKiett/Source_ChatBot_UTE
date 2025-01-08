<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'
import { Button, Drawer, Input, Textarea } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, reactive, ref } from 'vue'

const props = defineProps({
    feedbackDetail: Object,
    openPannel: Boolean,
    handleopenPannel: Function,
    fetchDataFeedback: Function
})

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const localOpen = ref(props.openPannel)
const feedbackStatus = ['Chưa xử lý', 'Đã xử lý']

const feedback = reactive({
    idFeedback: 0,
    fullName: '',
    email: '',
    content: '',
    feedbackType: '',
    status: '',
    createdTime: '',
    processedBy: '',
    processedTime: '',
    chatBotID: 0,
    chatbotName: ''
})

onMounted(() => {
    console.log('feedbackDetail', props.feedbackDetail)
    converntDataFeedback()
})

const converntDataFeedback = () => {
    if (props.feedbackDetail) {
        feedback.idFeedback = props.feedbackDetail.idFeedback
        feedback.fullName = props.feedbackDetail.fullName
        feedback.email = props.feedbackDetail.email
        feedback.content = props.feedbackDetail.content
        feedback.feedbackType = props.feedbackDetail.feedbackType
        feedback.status = props.feedbackDetail.status
        feedback.createdTime = props.feedbackDetail.createdTime
        feedback.processedBy = props.feedbackDetail.processedBy
        feedback.processedTime = props.feedbackDetail.processedTime
        feedback.chatBotID = props.feedbackDetail.chatBotID
        feedback.chatbotName = props.feedbackDetail.chatbotName
    }
}

// Handle Drawer open/close changes
const afterOpenChange = (bool: boolean) => {
    console.log('afterOpenChange', bool)
}

const handleClose = () => {
    localOpen.value = false
    props.handleopenPannel && props.handleopenPannel(false)

    //Reser feedback
    resetFeedback()
}

const handleSave = async () => {
    try {
        console.log('handleSave', feedback)

        const res = await axios.put(
            `${VITE_API_URL}/${VITE_API_VERSION}/feedback/${feedback.idFeedback}`,
            {
                processedBy: auth.payload?.username || 'Admin'
            }
        )
        if (res.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Xác nhận xử lý thành công góp ý <span class="font-semibold">${feedback.idFeedback}</span></p>`,
                true
            )
            props.fetchDataFeedback && props.fetchDataFeedback()
            handleClose()
        } else {
            alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
        }
    } catch (error) {
        console.log('handleSave error', error)
        alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
    }
}

// Reset feedback
const resetFeedback = () => {
    feedback.idFeedback = 0
    feedback.fullName = ''
    feedback.email = ''
    feedback.content = ''
    feedback.feedbackType = ''
    feedback.status = ''
    feedback.createdTime = ''
    feedback.processedBy = ''
    feedback.processedTime = ''
    feedback.chatBotID = 0
    feedback.chatbotName = ''
}
</script>

<template>
    <div>
        <Drawer
            title="Chi tiết góp ý"
            placement="right"
            v-model:open="localOpen"
            width="700"
            @afterOpenChange="afterOpenChange"
            @close="handleClose"
            :footer-style="{ textAlign: 'right' }"
            autofocus:false
            :maskClosable="false"
            class="feedback-detail"
        >
            <div>
                <div class="flex flex-col mb-4">
                    <label for="name" class="pb-2 font-medium">Họ và tên:</label>
                    <Input
                        readonly
                        v-model:value="feedback.fullName"
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
                        v-model:value="feedback.email"
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
                    <label for="feedbackType" class="pb-2 font-medium">Loại góp ý:</label>
                    <Input
                        readonly
                        v-model:value="feedback.feedbackType"
                        placeholder="Basic usage"
                        id="feedbackType"
                        class="h-10 input-readonly"
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
                    <label for="time" class="pb-2 font-medium">Thời gian:</label>
                    <Input
                        readonly
                        v-model:value="feedback.createdTime"
                        placeholder="Basic usage"
                        id="time"
                        class="h-10 input-readonly"
                    >
                        <template #prefix>
                            <img
                                src="/icons/calendar-days-solid.svg"
                                alt="calendar-days-solid.svg"
                                class="w-[14px] mr-2"
                            />
                        </template>
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="role" class="pb-2 font-medium">Góp ý:</label>
                    <Textarea
                        readonly
                        v-model:value="feedback.content"
                        placeholder="Góp ý"
                        :auto-size="{ minRows: 4, maxRows: 5 }"
                        class="input-readonly"
                    />
                </div>
                <div v-if="feedback.processedBy">
                    <p class="text-sm italic">
                        Người xử lý:
                        <span class="text-base font-semibold not-italic pl-1">{{
                            feedback.processedBy
                        }}</span>
                    </p>
                    <p class="text-sm italic">
                        Thời gian:
                        <span class="text-base font-semibold not-italic pl-1">{{
                            feedback.processedTime
                        }}</span>
                    </p>
                </div>
            </div>
            <template #footer>
                <Button
                    v-if="feedback.status == feedbackStatus[1]"
                    type="default"
                    @click="handleClose"
                    class="mr-3 h-10 font-semibold"
                    >Cancel</Button
                >
                <Button v-else type="default" @click="handleClose" class="mr-3 h-10 font-semibold">
                    Hủy
                </Button>
                <Button
                    :disabled="feedback.status == feedbackStatus[1]"
                    type="primary"
                    @click="handleSave"
                    class="w-44 h-10 font-semibold"
                >
                    Xác nhận xử lý
                </Button>
            </template>
        </Drawer>
    </div>
</template>

<style>
.select-role .ant-select-selector {
    border: none !important;
}

.feedback-detail .ant-input {
    cursor: not-allowed !important;
}
</style>
