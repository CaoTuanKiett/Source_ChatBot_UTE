<script lang="ts" setup>
import FeedbackDetail from '@/components/feedback/FeedbackDetail.vue'
import type { Feedback } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'

import { listFeedbackType } from '@/utils/constants'
import { CheckOutlined, EditOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { Button, Modal, Table, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { createVNode, onMounted, reactive, ref, watchEffect } from 'vue'

const listFeedback = ref<Feedback[]>([])
const isCreate = ref<boolean>(false)
const scrollContainer = ref<HTMLDivElement | null>(null)

const auth = useAuthStore()
const VITE_API_URL = import.meta.env.VITE_API_URL
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION

const feedbackDetail = reactive({
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

const feedbackStatus = ['Chưa xử lý', 'Đã xử lý']

const openPannel = ref<boolean>(false)
const searchValue = ref<string>('')

onMounted(async () => {
    await fetchDataFeedback()

    console.log('listFeedback', listFeedback.value)
})

const feedbackFilters = ref<{ text: string; value: string }[]>([])

watchEffect(() => {
    feedbackFilters.value = Array.from(
        new Set(listFeedback.value.map((item) => item.chatbotName || 'N/A'))
    ).map((name) => ({ text: name, value: name }))
})

const listColumn = [
    {
        title: 'ID',
        dataIndex: 'idFeedback',
        width: '20px'
    },
    {
        title: 'Họ và tên',
        dataIndex: 'fullName',
        width: '140px',
        sorter: (a: any, b: any) => a.username.localeCompare(b.username)
    },
    // {
    //     title: 'Email',
    //     dataIndex: 'email',
    //     width: '188px'
    // },
    {
        title: 'Góp ý',
        dataIndex: 'content',
        width: '400px'
    },
    {
        title: 'Loại góp ý',
        dataIndex: 'feedbackType',
        width: '120px',
        filters: listFeedbackType.map((item) => ({ text: item.label, value: item.value })),
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: string, record: any) => record.feedbackType.indexOf(value) === 0
    },
    {
        title: 'Ngày tạo',
        dataIndex: 'createdTime',
        width: '90px'
    },
    {
        title: 'Trạng thái',
        dataIndex: 'status',
        width: '140px',
        filters: feedbackStatus.map((item) => ({ text: item, value: item })),
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: string, record: any) => record.status.indexOf(value) === 0
    },
    {
        title: 'Chatbot',
        dataIndex: 'chatbotName',
        width: '120px',
        filters: feedbackFilters.value,
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: string, record: any) => record.chatbotName.indexOf(value) === 0
    },

    {
        title: 'Cài đặt',
        dataIndex: 'operation'
    }
]

const fetchDataFeedback = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/${VITE_API_VERSION}/feedbacks`)
        if (response.status === 200) {
            listFeedback.value = response.data
        }
    } catch (error) {
        console.error('error', error)
    }
}

const handleopenPannel = (open: boolean) => {
    openPannel.value = open
}

const handleOpenPanel = (feedback: any) => {
    console.log('handleOpenPanel', feedback)
    if (feedback === null) {
        isCreate.value = true
    }
    Object.assign(feedbackDetail, feedback)
    openPannel.value = true
}

const showDeleteConfirm = (item: Feedback) => {
    Modal.confirm({
        title: 'Xác nhận xử lý',
        icon: createVNode(ExclamationCircleOutlined),
        content: `Xác nhận xử lý góp ý ${item.idFeedback}?`,
        okText: 'Yes',
        okType: 'danger',
        cancelText: 'No',
        async onOk() {
            console.log('OK delete', item.idFeedback)
            await handleConfirmFeedback(item.idFeedback)
        },
        onCancel() {
            console.log('Cancel')
        }
    })
}

const onSearch = async () => {
    if (searchValue.value === '') {
        fetchDataFeedback()
    } else {
        try {
            const response = await axios.get(
                `${VITE_API_URL}/${VITE_API_VERSION}/feedback/search/${searchValue.value}`
            )
            if (response.status === 200) {
                listFeedback.value = response.data
            }
        } catch (error) {
            console.error('error', error)
        }
    }
}

const handleResetSearch = () => {
    searchValue.value = ''
    fetchDataFeedback()
}

const handleConfirmFeedback = async (idFeedback: number) => {
    try {
        const res = await axios.put(`${VITE_API_URL}/${VITE_API_VERSION}/feedback/${idFeedback}`, {
            processedBy: auth.payload?.username || 'Admin'
        })
        if (res.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Xác nhận xử lý thành công góp ý <span class="font-semibold">${idFeedback}</span></p>`,
                true
            )
            fetchDataFeedback()
        } else {
            alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
        }
    } catch (error) {
        console.log('handleSave error', error)
        alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
    }
}
</script>

<template>
    <div class="management-feedback relative w-full overflow-x-auto px-8">
        <div :class="`flex flex-col bg-white right-0 z-10 px-6 pt-4 pb-5 mt-8`">
            <div class="flex justify-end items-center">
                <div class="relative flex items-center">
                    <button class="absolute left-4" @click="onSearch()">
                        <img
                            src="/icons/magnifying-glass-solid.svg"
                            alt="magnifying-glass-solid.svg"
                            class="w-5 h-5 opacity-65"
                        />
                    </button>
                    <input
                        class="input-search w-96 rounded-full px-11 py-3 border-2 border-transparent focus:outline-none focus:border-blue-500 placeholder-gray-400 transition-all duration-300 border-gray-300 shadow-lg"
                        placeholder="Tìm kiếm..."
                        required="true"
                        type="text"
                        v-model="searchValue"
                        @keydown.enter="onSearch()"
                    />
                    <button type="reset" class="absolute right-3 p-1" @click="handleResetSearch()">
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
        <div class="" ref="scrollContainer">
            <Table
                :columns="listColumn"
                :data-source="listFeedback"
                :pagination="{ pageSize: 6 }"
                bordered
            >
                <template #bodyCell="{ column, record }">
                    <template v-if="column.dataIndex === 'idFeedback'">
                        <div class="truncate max-w-[20px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.idFeedback }}</span>
                                </template>
                                <span>{{ record.idFeedback }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'fullName'">
                        <div class="truncate max-w-[140px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.fullName }}</span>
                                </template>
                                <span>{{ record.fullName }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <!-- <template v-if="column.dataIndex === 'email'">
                        <div class="truncate max-w-[160px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.email }}</span>
                                </template>
                                <span>{{ record.email }}</span>
                            </Tooltip>
                        </div>
                    </template> -->
                    <template v-if="column.dataIndex === 'content'">
                        <div class="truncate max-w-[400px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.content }}</span>
                                </template>
                                <span>{{ record.content }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'createdTime'">
                        <div class="truncate max-w-[90px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.createdTime }}</span>
                                </template>
                                <span>{{ record.createdTime }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'status'">
                        <div class="truncate max-w-[140px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.status }}</span>
                                </template>
                                <span>{{ record.status }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'chatbotName'">
                        <div class="truncate max-w-[120px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.chatbotName }}</span>
                                </template>
                                <span>{{ record.chatbotName }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'feedbackType'">
                        <div class="truncate max-w-[120px]">
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">{{
                                        record.feedbackType
                                    }}</span>
                                </template>
                                <span>{{ record.feedbackType }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'operation'">
                        <div class="flex">
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">Xem chi tiết</span>
                                </template>
                                <div
                                    class="w-fit mr-3 px-2 pt-1 pb-[2px] border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                    @click="handleOpenPanel(record)"
                                >
                                    <EditOutlined style="font-size: 16px" />
                                </div>
                            </Tooltip>
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">Xác nhận xử lý góp ý</span>
                                </template>
                                <Button
                                    :disabled="record.status == feedbackStatus[1]"
                                    class="flex items-center px-2 pt-1 pb-[2px] border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                    @click="showDeleteConfirm(record as Feedback)"
                                >
                                    <CheckOutlined style="font-size: 16px" />
                                </Button>
                            </Tooltip>
                        </div>
                    </template>
                </template>
            </Table>
        </div>
        <FeedbackDetail
            v-if="openPannel"
            :openPannel="openPannel"
            :feedbackDetail="feedbackDetail"
            :handleopenPannel="handleopenPannel"
            :fetchDataFeedback="fetchDataFeedback"
        />
    </div>
</template>

<style scoped>
.management-feedback .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}
</style>
