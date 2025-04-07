<script setup lang="ts">
import { listFeedbackType } from '@/utils/constants'
import { defineProps, reactive } from 'vue'

const props = defineProps<{
    handleSendFeedback: Function
    handleCancelFeedback: Function
}>()

const feedbackDetail = reactive({
    fullName: '',
    email: '',
    content: '',
    feedbackType: ''
})

const handleSendQuestion = () => {
    props.handleSendFeedback(feedbackDetail)

    resetValue()
}

const handleCancelQuestion = () => {
    props.handleCancelFeedback()
    resetValue()
}

const resetValue = (): void => {
    feedbackDetail.fullName = ''
    feedbackDetail.email = ''
    feedbackDetail.content = ''
    feedbackDetail.feedbackType = ''
}
</script>

<template>
    <div
        class="form-feedback w-[95%] border-[1px] rounded-xl px-4 py-6 shadow-xl transition-all duration-300 ease-in-out delay-75"
    >
        <h1 class="text-center font-semibold uppercase mb-3">Form góp ý</h1>
        <div class="w-full flex flex-col items-center">
            <div class="w-full flex flex-col mb-3">
                <label for="" class="font-medium ml-1 text-sm">Họ tên:</label>
                <input
                    type="text"
                    v-model="feedbackDetail.fullName"
                    class="border-2 p-2 px-3 rounded-md shadow-sm text-sm"
                />
            </div>
            <div class="w-full flex flex-col mb-3">
                <label for="" class="font-medium ml-1 text-sm">Email:</label>
                <input
                    type="email"
                    v-model="feedbackDetail.email"
                    class="border-2 p-2 px-3 rounded-md shadow-sm text-sm"
                />
            </div>
            <div class="w-full flex flex-col mb-3">
                <label for="" class="font-medium ml-1 text-sm">Chọn loại góp ý:</label>
                <el-select
                    v-model="feedbackDetail.feedbackType"
                    placeholder="Loại góp ý"
                    class="placeholder:text-base rounded-md shadow-sm text-sm"
                    size="large"
                >
                    <el-option
                        v-for="item in listFeedbackType"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        class="text-sm"
                    />
                </el-select>
            </div>
            <div class="w-full flex flex-col mb-1 text-sm">
                <label for="" class="font-medium ml-1">Nhập góp ý:</label>
                <textarea
                    rows="3"
                    v-model="feedbackDetail.content"
                    class="border-2 p-2 px-3 rounded-md shadow-sm text-sm"
                />
            </div>
        </div>
        <div class="flex justify-center">
            <button
                @click="handleCancelQuestion"
                class="py-3 px-7 rounded-lg mt-2 font-semibold text-sm border-[1px] mr-2 shadow-md hover:opacity-75"
            >
                Hủy
            </button>
            <button
                @click="handleSendQuestion"
                class="bg-blue-500 text-white py-3 px-7 rounded-lg mt-2 font-semibold text-sm shadow-md hover:opacity-75"
            >
                Gửi góp ý
            </button>
        </div>
    </div>
</template>

<style>
.form-feedback .el-select__wrapper {
    height: 44px;
    border-radius: 12px;
}

.form-feedback .el-select__selected-item {
    font-size: 14px;
    color: black;
}
</style>