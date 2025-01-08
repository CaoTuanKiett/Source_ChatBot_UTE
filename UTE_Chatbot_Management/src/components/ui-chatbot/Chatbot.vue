<script setup lang="ts">
import ChatbotContainer from '@/components/ui-chatbot/components/ChatbotContainer.vue'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps<{
    chatbotToken: string
}>()

const isOpenChatbot = ref(false)
const tokenChatbotNew = ref<string>('')

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_BE_API = import.meta.env.VITE_API_URL
const VITE_CONTENT_SHOW_FORM = import.meta.env.VITE_CONTENT_SHOW_FORM
const VITE_CONTENT_SHOW_FORM_FEEDBACK = import.meta.env.VITE_CONTENT_SHOW_FORM_FEEDBACK

const BE_URL = `${VITE_BE_API}/${VITE_API_VERSION}`

const handleOpenChatbot = () => {
    isOpenChatbot.value = !isOpenChatbot.value

    if (!isOpenChatbot.value) {
        // xóa message ở local storage
        localStorage.removeItem('dataMess')
    }
}

onMounted(() => {
    tokenChatbotNew.value = props.chatbotToken
})

onBeforeUnmount(() => {
    console.log('onBeforeUnmount Chatbot.vue')
})

watch(
    () => props.chatbotToken,
    (newVal) => {
        tokenChatbotNew.value = newVal
    }
)
</script>


<template>
    <div
        class="fixed flex items-end right-10 bottom-9 transition-all duration-500 ease-in-out z-50"
    >
        <transition name="slide-fade">
            <div
                v-if="isOpenChatbot"
                class="relative transition-all duration-500 ease-in-out chatbot-box mb-8"
            >
                <ChatbotContainer
                    :apiEndpoint="BE_URL"
                    :chatbotToken="tokenChatbotNew"
                    :textShowForm="VITE_CONTENT_SHOW_FORM"
                    :textShowFormFeedback="VITE_CONTENT_SHOW_FORM_FEEDBACK"
                />
                <span class="absolute container-after"></span>
            </div>
        </transition>

        <img
            src="/images/icon-bot.png"
            alt="bot"
            :class="{ 'rotate-[360deg] bot-shadow': isOpenChatbot }"
            class="w-20 h-20 cursor-pointer rounded-full icon-bot ml-5 shadow-xl hover:shadow-2xl transition-all duration-700 ease-in-out"
            @click="handleOpenChatbot"
        />
    </div>
</template>

<style scoped>
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.5s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    /* Xuất hiện từ góc */
    transform: translate3d(280px, 280px, 0) scale(0.1);
    opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave-from {
    transform: translate3d(0, 0, 0) scale(1);
    opacity: 1;
}

.bot-shadow {
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
}

.container-after {
    border-left: 23px solid #ffffff;
    border-right: 0px solid transparent;
    border-top: 44px solid transparent;
    border-bottom: 26px solid transparent;
    position: absolute;
    bottom: 0px;
    right: -16px;
}
</style>

