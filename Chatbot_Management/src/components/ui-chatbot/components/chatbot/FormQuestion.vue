<script setup lang="ts">
import { defineProps, ref } from 'vue'

const props = defineProps<{
    handleSendQuestion: Function
    handleCancelQuestion: Function
}>()

const name = ref<string>('')
const email = ref<string>('')
const question = ref<string>('')

const handleSendQuestion = () => {
    props.handleSendQuestion(name.value, email.value, question.value)
    resetValue()
}

const handleCancelQuestion = () => {
    props.handleCancelQuestion()
    resetValue()
}

const resetValue = () => {
    name.value = ''
    email.value = ''
    question.value = ''
}
</script>

<template>
    <div
        class="form-question w-[90%] border-[1px] rounded-xl px-4 py-6 shadow-xl transition-all duration-300 ease-in-out delay-75"
    >
        <h1 class="text-center font-semibold uppercase mb-3">Form hỏi đáp</h1>
        <div class="w-full flex flex-col items-center">
            <div class="w-full flex flex-col mb-2">
                <label for="" class="font-medium text-sm ml-1">Họ tên:</label>
                <input type="text" v-model="name" class="border-2 p-2 rounded-md text-sm" />
            </div>
            <div class="w-full flex flex-col mb-2">
                <label for="" class="font-medium text-sm ml-1">Email:</label>
                <input type="email" v-model="email" class="border-2 p-2 rounded-md text-sm" />
            </div>
            <div class="w-full flex flex-col mb-2">
                <label for="" class="font-medium ml-1 text-sm">Nhập câu hỏi:</label>
                <textarea rows="3" v-model="question" class="border-2 p-2 rounded-md text-sm" />
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
                class="bg-blue-500 text-white py-3 px-7 rounded-lg mt-2 font-semibold text-sm border-[1px] mr-2 shadow-md hover:opacity-75"
            >
                Gửi câu hỏi
            </button>
        </div>
    </div>
</template>