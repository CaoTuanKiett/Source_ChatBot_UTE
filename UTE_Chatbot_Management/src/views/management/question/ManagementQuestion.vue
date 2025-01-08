<script lang="ts" setup>
import QuestionDetail from '@/components/question/QuestionDetail.vue'
import type { Question } from '@/interfaceConfig'
import { CommentOutlined } from '@ant-design/icons-vue'
import { Table, Tooltip } from 'ant-design-vue'
import axios from 'axios'

import { onMounted, reactive, ref } from 'vue'

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const listQuestion = ref<Question[]>([])
const isCreate = ref<boolean>(false)
const scrollContainer = ref<HTMLDivElement | null>(null)
const searchValue = ref<string>('')

const questionStatus = ['Chưa xử lý', 'Đã xử lý']

const questionDetail = reactive<Question>({
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

const openPannel = ref<boolean>(false)

const listColumn = [
    {
        title: 'ID',
        dataIndex: 'idQuestion',
        // width: '10px',
        sorter: (a: any, b: any) => a.idUser - b.idUser
    },
    {
        title: 'Họ và tên',
        dataIndex: 'fullName',
        width: '200px',
        sorter: (a: any, b: any) => a.username.localeCompare(b.username)
    },
    {
        title: 'Email',
        dataIndex: 'email',
        width: '220px'
    },
    {
        title: 'Câu hỏi',
        dataIndex: 'question',
        width: '300px'
    },
    {
        title: 'Ngày tạo',
        dataIndex: 'sentTime',
        width: '150px'
    },
    {
        title: 'Trạng thái',
        dataIndex: 'status',
        width: '200px',
        filters: questionStatus.map((item) => ({ text: item, value: item })),
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: string, record: any) => record.status.indexOf(value) === 0
    },
    {
        title: 'Chatbot',
        dataIndex: 'chatbotName'
        // width: '10%'
    },
    {
        title: 'Chức năng',
        dataIndex: 'operation',
        width: '100px'
    }
]

onMounted(async () => {
    await fetchDataQuestion()
})

const fetchDataQuestion = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/questions`)
        if (response.status === 200) {
            listQuestion.value = response.data
        }
    } catch (error) {
        console.error('error', error)
    }
}

const onSearch = async () => {
    if (searchValue.value === '') {
        fetchDataQuestion()
    } else {
        try {
            const response = await axios.get(`${VITE_API_URL}/question/search/${searchValue.value}`)
            if (response.status === 200) {
                listQuestion.value = response.data
            }
        } catch (error) {
            console.error('error', error)
        }
    }
}

const handleResetSearch = () => {
    searchValue.value = ''
    fetchDataQuestion()
}

const handleopenPannel = (open: boolean) => {
    openPannel.value = open
}

const handleOpenPanel = (question: any) => {
    console.log('handleOpenPanel', question)
    if (question === null) {
        isCreate.value = true
    }
    Object.assign(questionDetail, question)
    openPannel.value = true
    console.log('handleOpenPanel1111', questionDetail)
}

// const showDeleteConfirm = (id: string) => {
//     Modal.confirm({
//         title: 'Are you sure delete this task?',
//         icon: createVNode(ExclamationCircleOutlined),
//         content: 'Some descriptions',
//         okText: 'Yes',
//         okType: 'danger',
//         cancelText: 'No',
//         onOk() {
//             console.log('OK delete', id)
//         },
//         onCancel() {
//             console.log('Cancel')
//         }
//     })
// }
</script>

<template>
    <div class="management-question relative w-full overflow-x-auto px-8">
        <div :class="`flex flex-col bg-white right-0 z-10 px-6 pt-4 pb-5 mt-8`">
            <!-- <h1 class="font-semibold uppercase text-lg mb-3">Quản lý tài khoản</h1> -->
            <div class="flex justify-end items-center">
                <!-- <Button
                    class="flex items-center h-10 border-black hover:shadow-lg transition-all duration-300"
                    @click="handleOpenPanel(null)"
                    ><PlusOutlined /> Thêm mới</Button
                > -->
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
                :data-source="listQuestion"
                :pagination="{ pageSize: 6 }"
                bordered
            >
                <template #bodyCell="{ column, record }">
                    <template v-if="column.dataIndex === 'idQuestion'">
                        <div class="truncate max-w-[20px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.idQuestion }}</span>
                                </template>
                                <span>{{ record.idQuestion }}</span>
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
                    <template v-if="column.dataIndex === 'email'">
                        <div class="truncate max-w-[160px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.email }}</span>
                                </template>
                                <span>{{ record.email }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'question'">
                        <div class="truncate max-w-[300px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.question }}</span>
                                </template>
                                <span>{{ record.question }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'sentTime'">
                        <div class="truncate max-w-[80px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.sentTime }}</span>
                                </template>
                                <span>{{ record.sentTime }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'status'">
                        <div class="truncate max-w-[160px]">
                            <Tooltip color="#ccc" placement="topLeft">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.status }}</span>
                                </template>
                                <span>{{ record.status }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'chatbotName'">
                        <div class="truncate max-w-[110px]">
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">{{ record.chatbotName }}</span>
                                </template>
                                <span>{{ record.chatbotName }}</span>
                            </Tooltip>
                        </div>
                    </template>
                    <template v-if="column.dataIndex === 'operation'">
                        <div class="flex">
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">Trả lời</span>
                                </template>
                                <div
                                    class="w-fit mr-3 px-2 pt-1 pb-[2px] border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                    @click="handleOpenPanel(record)"
                                >
                                    <CommentOutlined style="font-size: 16px" />
                                </div>
                            </Tooltip>
                            <!-- <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">Xóa</span>
                                </template>
                                <div
                                    class="px-2 pt-1 pb-[2px] border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                    @click="showDeleteConfirm(record.id)"
                                >
                                    <DeleteOutlined style="font-size: 16px" />
                                </div>
                            </Tooltip> -->
                        </div>
                        <!-- <div class="w-[70px] flex">
                            <div
                                class="mr-3 p-2 bg-slate-300 cursor-pointer"
                                @click="handleOpenPanel(record)"
                            >
                                <EditOutlined />
                            </div>
                            <div
                                class="p-2 bg-slate-300 cursor-pointer"
                                @click="showDeleteConfirm(record.id)"
                            >
                                <DeleteOutlined />
                            </div>
                        </div> -->
                    </template>
                </template>
            </Table>
        </div>
        <div v-if="openPannel">
            <QuestionDetail
                :openPannel="openPannel"
                :questionDetail="questionDetail"
                :handleopenPannel="handleopenPannel"
                :fetchDataQuestion="fetchDataQuestion"
            />
        </div>
    </div>
</template>

<style scoped>
.management-question .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}
</style>
