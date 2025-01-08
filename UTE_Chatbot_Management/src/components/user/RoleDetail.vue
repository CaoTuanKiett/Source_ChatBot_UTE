<script setup lang="ts">
import type { listPermission, RoleManagement, User } from '@/interfaceConfig'
import { alertNotification } from '@/utils/notification'
import { Button, Drawer, Input, Select, Textarea } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref } from 'vue'

const props = defineProps({
    roleDetail: Object,
    openPannel: Boolean,
    isCreateRole: Boolean,
    handleopenPannel: Function,
    fetchDataRolesUsers: Function
})

const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const listPermissions = ref<listPermission[]>([])
const listUsers = ref<User[]>([])
const isLoadingUpdate = ref<boolean>(false)
const listRoleDetail = ref<RoleManagement>({
    role: {
        idRole: 0,
        roleName: '',
        description: '',
        createdTime: '',
        updatedTime: '',
        createdBy: '',
        updatedBy: ''
    },
    users: []
})
const searchValue = ref<string>('')

onMounted(async () => {
    if (!props.isCreateRole) {
        await handleConvertData()
    }
    await fetchDataListUsers()
})

const fetchDataListUsers = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/users/school/${VITE_ID_SCHOOL}`)
        if (response.status === 200) {
            listUsers.value = response.data
        }
    } catch (error) {
        console.log('error', error)
    }
}

const handleConvertData = () => {
    if (props.roleDetail) {
        listRoleDetail.value = {
            role: {
                idRole: props.roleDetail.role.idRole,
                roleName: props.roleDetail.role.roleName,
                description: props.roleDetail.role.description,
                createdTime: props.roleDetail.role.createdTime,
                updatedTime: props.roleDetail.role.updatedTime,
                createdBy: props.roleDetail.role.createdBy,
                updatedBy: props.roleDetail.role.updatedBy
            },
            users: props.roleDetail.users
        }

        valueSelectUserID.value = props.roleDetail.users.map((user) => user.idUser)
    }
}

listPermissions.value = [
    {
        id: 1,
        title: 'Quản lý chatbot',
        value: 'Admin',
        roleID: [1, 4]
    },
    {
        id: 2,
        title: 'Quản lý tài khoản',
        value: 'Admin',
        roleID: [1, 4]
    },
    {
        id: 3,
        title: 'Quản lý vai trò',
        value: 'Admin',
        roleID: [1, 4]
    },
    {
        id: 5,
        title: 'Quản lý trường học',
        value: 'Admin',
        roleID: [1, 4]
    },
    {
        id: 6,
        title: 'Quản lý câu hỏi',
        value: 'Admin',
        roleID: [2, 4]
    },
    {
        id: 7,
        title: 'Quản lý góp ý',
        value: 'Admin',
        roleID: [2, 4]
    },
    {
        id: 9,
        title: 'Quản lý tài liệu',
        value: 'Admin',
        roleID: [2, 3, 4]
    }
]

const localOpen = ref(props.openPannel)
const valueSelectUserID = ref<string[]>([])

// Handle Drawer open/close changes
const afterOpenChange = (bool: boolean) => {
    console.log('afterOpenChange', bool)
}

const handleSave = async () => {
    isLoadingUpdate.value = true

    listRoleDetail.value.users = listUsers.value.filter((user) =>
        valueSelectUserID.value.includes(user.idUser)
    )
    const listUserID = listRoleDetail.value.users.map((user) => user.idUser)

    try {
        if (props.isCreateRole) {
            console.log('create')
            await handleCreateRole(listUserID)
        } else {
            console.log('update')
            await handleUpdateRole(listUserID)
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingUpdate.value = false
    }
}

const handleCreateRole = async (listUserID: any) => {
    try {
        const res = await axios.post(`${VITE_API_URL}/roles/users`, {
            role: listRoleDetail.value.role,
            user_ids: listUserID
        })
        if (res.status === 200) {
            console.log('res', res)
            alertNotification(
                'Thành công',
                `<p>Tạo mới thành công Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
                true
            )
            props.fetchDataRolesUsers && props.fetchDataRolesUsers()
            handleClose()
        } else {
            alertNotification(
                'Thất bại',
                `<p>Tạo mới thất bại Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
                false
            )
        }
    } catch (error) {
        console.log('error', error)
        alertNotification(
            'Thất bại',
            `<p>Tạo mới thất bại Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
            false
        )
    }
}

const handleUpdateRole = async (listUserID: any) => {
    try {
        const res = await axios.put(`${VITE_API_URL}/roles/users`, {
            role: listRoleDetail.value.role,
            user_ids: listUserID
        })
        if (res.status === 200) {
            console.log('res', res)
            alertNotification(
                'Thành công',
                `<p>Cập nhật thành công Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
                true
            )
            props.fetchDataRolesUsers && props.fetchDataRolesUsers()
            handleClose()
        } else {
            alertNotification(
                'Thất bại',
                `<p>Cập nhật thất bại Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
                false
            )
        }
    } catch (error) {
        console.log('error', error)
        alertNotification(
            'Thất bại',
            `<p>Cập nhật thất bại Role <span class="font-semibold">${listRoleDetail.value.role.roleName}</span></p>`,
            false
        )
    }
}

const handleClose = () => {
    console.log('handleClose')
    localOpen.value = false
    props.handleopenPannel && props.handleopenPannel(false)
}

const handleChange = () => {
    console.log('valueSelectUserID.value', valueSelectUserID.value)
}

const handleSearch = (val: string) => {
    searchValue.value = val.toLowerCase()
}

const handleFilter = (searchValue: string, option: any) => {
    if (!option?.label) return false
    const search = searchValue.toLowerCase()
    const label = option.label.toLowerCase()
    return label.includes(search)
}
</script>

<template>
    <div class="role-detail">
        <Drawer
            :title="
                props.isCreateRole
                    ? 'Thêm mới vai trò'
                    : `Chỉnh sửa vai trò ${listRoleDetail?.role.roleName}`
            "
            placement="right"
            :open="openPannel"
            width="620"
            @afterOpenChange="afterOpenChange"
            @close="handleClose"
            :maskClosable="false"
            :footer-style="{ textAlign: 'right' }"
        >
            <div class="mb-3">
                <p class="font-semibold mb-1">Tên vai trò</p>
                <Input
                    type="text"
                    id="status"
                    v-model:value="listRoleDetail.role.roleName"
                    class="w-full border border-black-900 rounded p-2"
                />
            </div>
            <div class="mb-3">
                <p class="font-semibold mb-1">Mô tả</p>
                <Textarea
                    type="text"
                    id="status"
                    v-model:value="listRoleDetail.role.description"
                    :rows="4"
                    class="w-full border border-black-900 rounded p-2"
                />
            </div>

            <div class="mb-3">
                <label for="user" class="font-semibold mb-1">Người dùng</label>
                <Select
                    v-model:value="valueSelectUserID"
                    mode="multiple"
                    style="width: 100%"
                    placeholder="Please select"
                    class=""
                    :options="
                        listUsers.map((user) => ({
                            ...user,
                            value: user.idUser,
                            label: user.username
                        }))
                    "
                    :filterOption="handleFilter"
                    @change="handleChange()"
                    @search="handleSearch"
                >
                    <template #option="{ avatarUrl, username, email }">
                        <div class="flex justify-between">
                            <div class="flex items-center">
                                <img
                                    :src="avatarUrl || '/icons/cat-avatar.png'"
                                    :alt="username"
                                    class="rounded-full w-8 h-8 object-cover mr-2"
                                />
                                <span>{{ username }}</span>
                            </div>
                            <span>{{ email }}</span>
                        </div>
                    </template>
                </Select>
            </div>
            <div>
                <p class="font-semibold mb-1">Quyền</p>
                <div>
                    <div
                        v-for="permission in listPermissions"
                        :key="permission.id"
                        :class="['flex items-center justify-between p-2 border-b border-black-900']"
                    >
                        <p>{{ permission.title }}</p>
                        <div class="flex items-center mr-10">
                            <input
                                disabled
                                :checked="permission.roleID.includes(listRoleDetail.role.idRole)"
                                type="checkbox"
                                :value="permission.value"
                                class="w-4 h-4"
                            />
                            <p class="ml-3">Quản lý</p>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button type="default" @click="handleClose" class="mr-3 h-10 font-bold">Hủy</Button>
                <Button
                    type="primary"
                    :loading="isLoadingUpdate"
                    @click="handleSave"
                    class="w-28 h-10 font-bold"
                    >Lưu</Button
                >
            </template>
        </Drawer>
    </div>
</template>

<style>
/* .ant-drawer-right .ant-select-selector {
    min-height: 62px !important;
    display: flex !important;
    align-items: flex-start !important;
} */
</style>
