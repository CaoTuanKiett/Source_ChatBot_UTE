<script lang="ts" setup>
import UserDetail from '@/components/user/UserDetail.vue'
import type { Role, User } from '@/interfaceConfig'
import { alertNotification } from '@/utils/notification'
import {
    DeleteOutlined,
    EditOutlined,
    ExclamationCircleOutlined,
    PlusOutlined
} from '@ant-design/icons-vue'
import { Button, Modal, Skeleton, Table, Tooltip } from 'ant-design-vue'
import axios from 'axios'

import { computed, createVNode, onMounted, reactive, ref, watch } from 'vue'

const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const current = ref<number>(1)
const pageSize = ref<number>(10)
const listUser = ref<User[]>([])
const isCreate = ref<boolean>(false)
const listRole = ref<Role[]>([])
const scrollContainer = ref<HTMLDivElement | null>(null)
const isLoadingData = ref<boolean>(false)
const searchValue = ref<string>('')
// const filtersForRoles = ref<{ text: string; value: number }[]>([])

const userDetail = reactive<User>({
    idUser: 0,
    username: '',
    avatarUrl: '',
    phone: '',
    email: '',
    birthday: '',
    gender: '',
    address: '',
    password: '',
    role: '',
    status: '',
    createdTime: '',
    updatedTime: '',
    createdBy: '',
    roleID: 0,
    schoolID: 0
})

const openPannel = ref<boolean>(false)

const onSearch = async () => {
    console.log('use value', searchValue.value)
    if (searchValue.value === '') {
        fetchDataUsers()
    } else {
        try {
            const response = await axios.get(`${VITE_API_URL}/users/search/${searchValue.value}`)

            if (response.status === 200) {
                listUser.value = response.data
            }
        } catch (error) {
            console.error('error', error)
        }
    }
}

const handleResetSearch = () => {
    searchValue.value = ''
    fetchDataUsers()
}

onMounted(async () => {
    await fetchDataRoles()

    await fetchDataUsers()
    console.log('listUser', listUser.value)
    console.log('listRole', listRole.value)
    console.log('filtersForRoles', filtersForRoles.value)
})

const fetchDataRoles = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/roles`)

        if (response.status === 200) {
            listRole.value = response.data
        }
    } catch (error) {
        console.error('error', error)
    }
}

const fetchDataUsers = async () => {
    isLoadingData.value = true
    try {
        const response = await axios.get(`${VITE_API_URL}/users/school/${VITE_ID_SCHOOL}`)

        if (response.status === 200) {
            listUser.value = response.data
        }
    } catch (error) {
        console.error('error', error)
    } finally {
        isLoadingData.value = false
    }
}

const convertRole = (roleID: number) => {
    const role = listRole.value.find((role) => role.idRole === roleID)
    return role ? role.roleName : ''
}

const filtersForRoles = computed(() =>
    listRole.value.map((role) => ({
        text: role.roleName,
        value: role.idRole
    }))
)

const listColumn = [
    {
        title: 'ID',
        dataIndex: 'idUser',
        width: '60px',
        sorter: (a: any, b: any) => a.idUser - b.idUser
    },
    {
        title: 'Họ và tên',
        dataIndex: 'username',
        width: '208px',
        sorter: (a: any, b: any) => a.username.localeCompare(b.username)
    },
    {
        title: 'Email',
        dataIndex: 'email',
        width: '260px'
    },
    {
        title: 'Số điện thoại',
        dataIndex: 'phone',
        width: '188px'
    },
    {
        title: 'Vai trò',
        dataIndex: 'roleID',
        width: '148px',
        filters: filtersForRoles.value,
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: any, record: any) => record.roleID === value
    },
    {
        title: 'Trạng thái',
        dataIndex: 'status',
        width: '148px',
        filters: [
            { text: 'Hoạt động', value: 1 },
            { text: 'Vô hiệu hóa', value: 0 }
        ],
        filterMode: 'tree',
        filterSearch: true,
        onFilter: (value: any, record: any) => record.status === value
    },
    {
        title: 'Cài đặt',
        dataIndex: 'operation',
        width: '100px'
    }
]

const handleopenPannel = (open: boolean) => {
    openPannel.value = open
}

watch(pageSize, () => {
    console.log('pageSize', pageSize.value)
})
watch(current, () => {
    console.log('current', current.value)
})

const handleOpenPanel = (user: any) => {
    console.log('handleOpenPanel', user)
    if (user === null) {
        isCreate.value = true
        resetUser()
    } else {
        isCreate.value = false
    }
    Object.assign(userDetail, user)
    openPannel.value = true
}

//reser user
const resetUser = () => {
    userDetail.idUser = 0
    userDetail.username = ''
    userDetail.avatarUrl = ''
    userDetail.phone = ''
    userDetail.email = ''
    userDetail.birthday = ''
    userDetail.address = ''
    userDetail.password = ''
    userDetail.role = ''
    userDetail.status = ''
    userDetail.createdTime = ''
    userDetail.updatedTime = ''
    userDetail.createdBy = ''
    userDetail.roleID = 0
    userDetail.schoolID = 0
}

const showDeleteConfirm = async (id: string, name: string) => {
    Modal.confirm({
        title: `Bạn có chắc chắn muốn xóa ?`,
        icon: createVNode(ExclamationCircleOutlined),
        content: `Người dùng ${name}`,
        okText: 'Yes',
        okType: 'danger',
        cancelText: 'No',
        async onOk() {
            try {
                const response = await axios.delete(`${VITE_API_URL}/user/${id}`)
                if (response.status === 200) {
                    alertNotification(
                        'Thành công',
                        `<p>Xóa thành công chatbot <span class="font-semibold">${name}</span></p>`,
                        true
                    )
                    fetchDataUsers()
                } else {
                    alertNotification('Thất bại', 'Xóa không thành công', false)
                }
            } catch (error) {
                console.error('error', error)
                alertNotification('Thất bại', 'Xóa không thành công', false)
            }
        },
        onCancel() {
            console.log('Cancel')
        }
    })
}
</script>

<template>
    <div class="management-users relative w-full overflow-x-auto px-8">
        <div :class="`flex flex-col bg-white right-0 z-10 px-6 pt-4 pb-5 mt-8`">
            <!-- <h1 class="font-semibold uppercase text-lg mb-3">Quản lý tài khoản</h1> -->
            <div class="flex justify-between items-center">
                <Button
                    class="flex items-center h-10 border-black hover:shadow-lg transition-all duration-300"
                    @click="handleOpenPanel(null)"
                    ><PlusOutlined /> Thêm mới</Button
                >
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

        <Skeleton :loading="isLoadingData" :active="true">
            <div class="" ref="scrollContainer">
                <Table
                    v-if="filtersForRoles.length > 0"
                    :columns="listColumn"
                    :data-source="listUser"
                    :pagination="{ pageSize: 8 }"
                    bordered
                >
                    <template #bodyCell="{ column, record }">
                        <template v-if="column.dataIndex === 'status'">
                            <div class="truncate">
                                {{ record.status === 1 ? 'Hoạt động' : 'Vô hiệu hóa' }}
                            </div>
                        </template>
                        <template v-if="column.dataIndex === 'roleID'">
                            <div class="truncate">
                                {{ convertRole(record.roleID) }}
                            </div>
                        </template>
                        <template v-if="column.dataIndex === 'operation'">
                            <div class="pl-3 flex">
                                <Tooltip color="#ccc">
                                    <template #title>
                                        <span class="text-xs text-black">Chỉnh sửa</span>
                                    </template>
                                    <div
                                        class="mr-3 px-2 py-1 border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                        @click="handleOpenPanel(record)"
                                    >
                                        <EditOutlined />
                                    </div>
                                </Tooltip>
                                <Tooltip color="#ccc">
                                    <template #title>
                                        <span class="text-xs text-black">Xóa</span>
                                    </template>
                                    <div
                                        class="px-2 py-1 border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                        @click="showDeleteConfirm(record.idUser, record.username)"
                                    >
                                        <DeleteOutlined />
                                    </div>
                                </Tooltip>
                            </div>
                        </template>
                    </template>
                </Table>
            </div>
        </Skeleton>
        <UserDetail
            v-if="openPannel"
            :openPannel="openPannel"
            :userDetail="userDetail"
            :handleopenPannel="handleopenPannel"
            :isCreate="isCreate"
            :listRole="listRole"
            :fetchDataUsers="fetchDataUsers"
        />
    </div>
</template>

<style>
.management-users .ant-table-cell {
    padding: 12px 16px !important;
}

.management-users .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}
</style>
