<script setup lang="ts">
import type { Message } from '@/interfaceConfig'
import { useTimeAgo } from '@vueuse/core'
import { marked } from 'marked'
import { computed } from 'vue'
const props = defineProps<{
    sender: string
    message: Message
}>()

const TimeAgo = computed(() => {
    return useTimeAgo(new Date(props.message.sentTime), { updateInterval: 60 }).value
})
</script>

<template>
    <div class="">
        <div v-if="props.sender === 'user'" class="flex justify-end mt-1">
            <div class="flex flex-col items-end max-w-64">
                <time class="text-[10px] font-medium opacity-50 pr-3">{{ TimeAgo }}</time>
                <div class="w-fit relative max-w-64 bg-blue-500 text-white p-2 px-3 rounded-xl">
                    <p
                        class="w-full h-fit text-left text-sm"
                        v-html="marked(props.message?.content)"
                    ></p>
                    <span class="after-message-user"></span>
                </div>
            </div>
        </div>
        <div v-else class="flex justify-start mt-1">
            <div class="flex flex-col items-start max-w-64">
                <time class="text-[10px] font-medium opacity-50 pl-3">{{ TimeAgo }}</time>
                <div class="w-fit relative max-w-64 bg-gray-300 p-2 px-3 rounded-xl">
                    <p
                        class="w-full h-fit text-left text-sm"
                        v-html="marked(props.message?.content)"
                    ></p>
                    <span class="after-message-bot"></span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.after-message-user {
    position: absolute;
    right: -7px;
    bottom: 0;
    border-bottom: 21px solid rgb(59 130 246 / var(--tw-bg-opacity));
    border-right: 18px solid transparent;
    /* border-end-end-radius: 0px;
  border-start-end-radius: 18px; */
}

.after-message-bot {
    position: absolute;
    left: -7px;
    bottom: 0;
    border-bottom: 21px solid rgb(209 213 219 / var(--tw-bg-opacity));
    border-left: 18px solid transparent;
    /* border-end-start-radius: 0px;
  border-start-start-radius: 18px; */
}
</style>
