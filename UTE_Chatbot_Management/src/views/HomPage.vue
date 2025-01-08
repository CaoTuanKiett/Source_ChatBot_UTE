<script setup lang="ts">
import ChatbotUI from '@/components/ui-chatbot/Chatbot.vue'
const VITE_CHATBOT_TOKEN = import.meta.env.VITE_CHATBOT_TOKEN
</script>
<template>
    <div class="w-full mt-[100px]">
        <img src="/images/homePage.png" alt="homePage.png" />
        <img src="/images/homePage2.png" alt="homePage.png" />
        <ChatbotUI :chatbotToken="VITE_CHATBOT_TOKEN" />
    </div>
</template>


