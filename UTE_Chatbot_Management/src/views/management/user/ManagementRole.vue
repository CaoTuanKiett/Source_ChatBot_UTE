<script lang="ts" setup>
import type { Role, RoleManagement } from '@/interfaceConfig'
import {
    DeleteOutlined,
    EditOutlined,
    ExclamationCircleOutlined,
    PlusOutlined
} from '@ant-design/icons-vue'
import { Avatar, AvatarGroup, Button, Modal, Popover, Table, Tooltip } from 'ant-design-vue'
import { createVNode, onMounted, ref } from 'vue'

import RoleDetail from '@/components/user/RoleDetail.vue'
import { alertNotification } from '@/utils/notification'
import axios from 'axios'

const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const searchValue = ref<string>('')
const openPannel = ref<boolean>(false)
const roleDetail = ref<RoleManagement | null>(null)
const listRolesUsers = ref<RoleManagement[]>([])
const listRoles = ref<Role[]>([])
const isCreateRole = ref<boolean>(true)

const columns = [
    {
        title: 'STT',
        dataIndex: 'role.idRole',
        width: '5%'
    },
    {
        title: 'Vai trò',
        dataIndex: 'role.roleName',
        sorter: true,
        width: '20%'
    },
    {
        title: 'Mô tả',
        dataIndex: 'role.description',
        width: '30%'
    },
    {
        title: 'User',
        dataIndex: 'users',
        width: '43%'
    },
    {
        title: 'Cài đặt',
        dataIndex: 'operation',
        width: '40px'
    }
]

onMounted(async () => {
    await fetchDataRolesUsers()
})

const handleopenPannel = (open: boolean) => {
    openPannel.value = open
}

const handleCreateRole = () => {
    openPannel.value = true
    roleDetail.value = null
    isCreateRole.value = true
    console.log('handleCreateRole', openPannel.value)
}

const handleEditRole = (value: RoleManagement) => {
    openPannel.value = true
    roleDetail.value = value
    isCreateRole.value = false
    console.log('handleEditRole', openPannel.value)
}

const onSearch = () => {
    console.log('use value', searchValue.value)
    // console.log('or use this.value', value.value)
}

const fetchDataRolesUsers = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/roles/users/${VITE_ID_SCHOOL}`)

        if (response.status === 200) {
            listRolesUsers.value = response.data
            listRoles.value = response.data.map((item: RoleManagement) => item.role)
            console.log('fetchData', response.data)
        }
    } catch (error) {
        console.error('fetchData', error)
    }
}

const getRoleName = (idRole: number): string => {
    const role = listRoles.value.find((item) => item.idRole === idRole)
    return role ? role.roleName : 'Unknown Role'
}

const showDeleteConfirm = async (id: string, name: string) => {
    Modal.confirm({
        title: `Bạn có chắc chắn muốn xóa ?`,
        icon: createVNode(ExclamationCircleOutlined),
        content: `Vai trò ${name}`,
        okText: 'Yes',
        okType: 'danger',
        cancelText: 'No',
        async onOk() {
            try {
                const response = await axios.delete(`${VITE_API_URL}/role/${id}`)
                if (response.status === 200) {
                    alertNotification(
                        'Thành công',
                        `<p>Xóa thành công chatbot <span class="font-semibold">${name}</span></p>`,
                        true
                    )
                    fetchDataRolesUsers()
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
    <div class="management-role relative h-full w-full overflow-x-auto px-8">
        <div class="w-full px-6 pt-4 pb-5 mt-8">
            <!-- <h1 class="font-semibold uppercase text-lg mb-3">Quản lý vai trò</h1> -->
            <div class="flex justify-between items-center">
                <Button
                    class="flex items-center h-10 border-black hover:shadow-lg transition-all duration-300"
                    @click="handleCreateRole()"
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
        <Table
            :columns="columns"
            :data-source="listRolesUsers"
            :pagination="{ pageSize: 5 }"
            bordered
        >
            <template #bodyCell="{ column, record }">
                <template v-if="column.dataIndex === 'role.idRole'">
                    <p>{{ record.role.idRole }}</p>
                </template>
                <template v-if="column.dataIndex === 'role.roleName'">
                    <p>{{ record.role.roleName }}</p>
                </template>
                <template v-if="column.dataIndex === 'role.description'">
                    <p>{{ record.role.description }}</p>
                </template>
                <template v-if="column.dataIndex === 'users'">
                    <AvatarGroup :maxCount="4" :size="46">
                        <Popover
                            v-for="user in record.users"
                            :key="user.idUser"
                            placement="topLeft"
                        >
                            <template #content>
                                <div class="flex items-center">
                                    <img
                                        :src="user.avatarUrl || '/icons/cat-avatar.png'"
                                        :alt="user.username"
                                        class="w-16 h-16 rounded object-cover"
                                    />
                                    <div class="ml-2">
                                        <p class="font-semibold">{{ user.username }}</p>
                                        <p>{{ user.email }}</p>
                                        <p><span>Vai trò: </span>{{ getRoleName(user.roleID) }}</p>
                                    </div>
                                </div>
                            </template>
                            <Avatar
                                :src="user.avatarUrl || '/icons/cat-avatar.png'"
                                style="background-color: #87d068"
                                :gap="100"
                                class="object-cover"
                            >
                                <!-- <template #icon>
                                    <img :src="user.avatar" :alt="user.name" />
                                </template> -->
                            </Avatar>
                        </Popover>
                    </AvatarGroup>
                </template>
                <template v-if="column.dataIndex === 'operation'">
                    <div class="flex">
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">Chỉnh sửa</span>
                            </template>
                            <div
                                class="w-fit mr-3 px-2 py-1 border-[1px] border-slate-300 cursor-pointer rounded-md hover:border-slate-500 transition-all duration-300"
                                @click="handleEditRole(record as RoleManagement)"
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
                                @click="showDeleteConfirm(record.role.idRole, record.role.roleName)"
                            >
                                <DeleteOutlined />
                            </div>
                        </Tooltip>
                    </div>
                    <!-- <Button @click="handleEditRole(record as RoleManagement)">Edit</Button> -->
                </template>
            </template>
        </Table>
        <div v-if="openPannel">
            <RoleDetail
                :openPannel="openPannel"
                :roleDetail="roleDetail"
                :handleopenPannel="handleopenPannel"
                :fetchDataRolesUsers="fetchDataRolesUsers"
                :isCreateRole="isCreateRole"
            />
        </div>
    </div>
</template>

<style>
.editable-row-operations a {
    margin-right: 8px;
}

.management-role .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}

/* .management-role .ant-table-cell {
    padding: 12px 16px !important;
} */
</style>
