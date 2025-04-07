<script lang="ts" setup>
// import {formatDataConfig} from '@/utils/index'
import ModalCreate from '@/components/chatbot/ModalCreate.vue'
import ChatbotItem from '@/components/common/ChatbotItem.vue'

import ChatbotUI from '@/components/ui-chatbot/Chatbot.vue'
// import { AutoComplete, InputSearch } from 'ant-design-vue'
import type { DataChatbot } from '@/types/chatbot'
import { alertNotification } from '@/utils/notification'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Button, Skeleton } from 'ant-design-vue'
import axios from 'axios'
import { onBeforeUnmount, onMounted, ref } from 'vue'

interface Option {
    query: string
    category: string
    value: string
    count: number
}

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL

const dataChatbot = ref<DataChatbot[]>([])
const dataChatbotDetail = ref<DataChatbot>(null)
const valueSearch = ref<string>('')
const isOpenModal = ref(false)
const activeScroll = ref(false)
const scrollContainer = ref<HTMLDivElement | null>(null)
const isCreate = ref(false)
const isLoadingData = ref(false)
const searchValue = ref<string>('')
const isShowChatbot = ref<boolean>(false)
const tokenChatbot = ref<string>('')

onMounted(async () => {
    console.log('onMounted ManagementChatbot')

    await getDataChatbot()
    if (scrollContainer.value) {
        scrollContainer?.value.addEventListener('scroll', handleScroll)
    }
})

onBeforeUnmount(() => {
    if (scrollContainer.value) {
        scrollContainer.value.removeEventListener('scroll', handleScroll)
    }
})

const handleShowChatbot = (show: boolean, token: string) => {
    isShowChatbot.value = show
    tokenChatbot.value = token
}

const getDataChatbot = async () => {
    isLoadingData.value = true
    try {
        const apiUrl = `${VITE_API_URL}/chatbots/school/${VITE_ID_SCHOOL}`

        const response = await axios.get(apiUrl)
        if (response.status === 200) {
            dataChatbot.value = response.data
        }

        isLoadingData.value = false
    } catch (error) {
        isLoadingData.value = false
        console.log('error', error)
    }
}

const handleScroll = () => {
    if (scrollContainer.value) {
        // console.log('scrollContainer.value.scrollTop', scrollContainer.value.scrollTop)
        activeScroll.value = scrollContainer.value.scrollTop > 50
    }
}

const toggleCheckbox = (item: any) => {
    item.status = !item.status
    // isChecked.value = !isChecked.value
}

const handleSetting = (item: any) => {
    if (item) {
        dataChatbotDetail.value = item
        handleOpenPanel(false)
    }
}

const onSearch = async () => {
    console.log('use value', valueSearch.value)
    try {
        isLoadingData.value = true
        const res = await axios.post(`${VITE_API_URL}/chatbot/search`, {
            searchValue: valueSearch.value,
            schoolId: VITE_ID_SCHOOL
        })

        if (res.status === 200) {
            dataChatbot.value = res.data
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingData.value = false
    }
}

const handleRemoveSearch = async () => {
    valueSearch.value = ''
    await getDataChatbot()
}

const handleDelete = async (item: any) => {
    try {
        const apiUrl = `${VITE_API_URL}/chatbot/${item.idChatBot}`
        const response = await axios.delete(apiUrl)
        if (response.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Xóa thành công chatbot <span class="font-semibold">${item.chatBotName}</span></p>`,
                true
            )
            isShowChatbot.value = false
            getDataChatbot()
        }
    } catch (error) {
        console.log('error', error)
    }
}

const handleOpenPanel = (value: boolean) => {
    // router.push({ path: `/chatbot/detail/${item?.id}` })
    isOpenModal.value = true
    isCreate.value = value
}

const handleCloseModal = async () => {
    await getDataChatbot()
    isOpenModal.value = false
    dataChatbotDetail.value = null
}
</script>

<template>
    <div class="managemnt-chatbot w-full relative">
        <ChatbotUI v-if="isShowChatbot" :chatbotToken="tokenChatbot" />
        <div
            :class="`flex flex-col bg-white right-0 w-full z-10 px-14 pt-3 pb-5 mt-8 ${
                activeScroll ? 'activeScroll' : ''
            }`"
        >
            <div class="flex justify-between">
                <Button
                    class="flex items-center h-10 border-black hover:shadow-lg transition-all duration-300"
                    @click="handleOpenPanel(true)"
                    ><PlusOutlined /> Thêm mới</Button
                >
                <div class="relative flex items-center">
                    <button class="absolute left-4" @click="onSearch()">
                        <img
                            src="/icons/magnifying-glass-solid.svg"
                            alt="magnifying-glass-solid.svg"
                            class="w-5 h-5"
                        />
                    </button>
                    <input
                        class="input-search w-96 rounded-full px-11 py-3 border-2 border-transparent focus:outline-none focus:border-blue-500 placeholder-gray-400 transition-all duration-300 border-gray-400 shadow-lg"
                        placeholder="Search..."
                        required="true"
                        type="text"
                        v-model="valueSearch"
                        @keydown.enter="onSearch()"
                    />
                    <button @click="handleRemoveSearch()" type="reset" class="absolute right-3 p-1">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="w-5 h-5 text-gray-700"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M6 18L18 6M6 6l12 12"
                            ></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <div
            v-if="dataChatbot.length > 0"
            ref="scrollContainer"
            class="h-5/6 pt-4 overflow-y-auto flex flex-col items-center"
        >
            <ChatbotItem
                v-for="(item, index) in dataChatbot"
                :key="index"
                :item="item"
                :toggleCheckbox="toggleCheckbox"
                :handleSetting="handleSetting"
                :handleDelete="handleDelete"
                :handleShowChatbot="handleShowChatbot"
            />
        </div>
        <Skeleton
            :loading="isLoadingData"
            v-else
            v-for="i in 3"
            :key="i"
            active
            :paragraph="{ rows: 4 }"
            class="py-4 px-32"
        ></Skeleton>
        <div v-if="isOpenModal">
            <ModalCreate
                :openModal="isOpenModal"
                :isCreateNew="isCreate"
                :handleCloseModal="handleCloseModal"
                :dataChatbotDetail="dataChatbotDetail"
            />
        </div>
    </div>
</template>

<style>
.managemnt-chatbot {
    /* padding: 148px 190px;
    box-shadow:
        rgba(0, 0, 0, 0.2) 0px 12px 28px 0px,
        rgba(0, 0, 0, 0.1) 0px 2px 4px 0px,
        rgba(255, 255, 255, 0.05) 0px 0px 0px 1px inset; */
}

.activeScroll {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.managemnt-chatbot .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}

.checkbox-wrapper-22 {
    display: inline-block;
    height: 25px;
    position: relative;
    width: 48px;
    margin-left: 4px;
}

.checkbox-wrapper-22 .switch {
    display: inline-block;
    height: 25px;
    position: relative;
    width: 48px;
}

.checkbox-wrapper-22 .switch input {
    display: none;
}

.checkbox-wrapper-22 .slider {
    background-color: #ccc;
    bottom: 0;
    cursor: pointer;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    transition: 0.4s;
}

.checkbox-wrapper-22 .slider:before {
    background-color: #fff;
    bottom: 4px;
    content: '';
    height: 18px;
    left: 4px;
    position: absolute;
    transition: 0.4s;
    width: 18px;
}

.checkbox-wrapper-22 input:checked + .slider {
    background-color: #66bb6a;
}

.checkbox-wrapper-22 input:checked + .slider:before {
    transform: translateX(22px);
}

.checkbox-wrapper-22 .slider.round {
    border-radius: 34px;
}

.checkbox-wrapper-22 .slider.round:before {
    border-radius: 50%;
}
</style>
