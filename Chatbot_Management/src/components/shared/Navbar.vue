<script setup lang="ts">
import { RoutePath } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { DownOutlined } from '@ant-design/icons-vue'
import { Icon } from '@iconify/vue'
import { Dropdown, Menu, MenuItem, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import UserDetail from '../user/UserDetail.vue'

import type { Role, User } from '@/interfaceConfig'
const route = useRoute()

const auth = useAuthStore()
const url = ref(route.path)
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

// const fullPath = computed(() => window.location.href)

// watch(fullPath, (newValue, oldValue) => {
//     console.log('fullPath', newValue, oldValue)
// })

const activeScroll = ref(false)
const openPannel = ref<boolean>(false)
const listRole = ref<Role[]>([])
const user = ref<User>({
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

onMounted(async () => {
    await fetchData()
})

const convertRole = (roleID: number) => {
    const role = listRole.value?.find((role) => role.idRole === roleID)
    return role ? role.roleName : ''
}

const handleopenPannel = async (value: boolean) => {
    openPannel.value = value
}

const fetchData = async () => {
    await getUserDetail()
    await fetchDataRoles()
}

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

const getUserDetail = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/user/${auth.payload?.idUser}`)

        if (response.status === 200) {
            user.value = response.data
        }
    } catch (error) {
        console.error('error', error)
    }
}

window.addEventListener('scroll', () => {
    if (window.scrollY > 50 && url.value === '/') {
        activeScroll.value = true
        // console.log('activeScroll', activeScroll.value)
    } else {
        activeScroll.value = false
    }
})
</script>

<template>
    <div class="nav-bar bg-white fixed top-0 left-0 right-0 z-50" :class="{ hidden: activeScroll }">
        <div class="mx-auto px-[8%]">
            <header
                :class="`flex flex-col lg:flex-row justify-between items-center my-3 transition ease-in-out delay-350 duration-300 ${
                    activeScroll ? 'activeScroll' : ''
                }`"
            >
                <div class="flex w-full lg:w-auto items-center justify-between">
                    <RouterLink to="/" class="flex items-center">
                        <img
                            src="/images/logo-truong-250.png"
                            alt="logo-vaias"
                            class="w-[70px] h-[70px] object-cover mr-2"
                        />
                        <div class="flex flex-col ml-2">
                            <span class="font-semibold text-slate-800 text-xl uppercase"
                                >Trường Đại học Sư phạm Kỹ thuật</span
                            >
                            <span class="text-slate-800 text-base uppercase">Đại học Đà Nẵng</span>
                        </div>
                    </RouterLink>
                    <div class="block lg:hidden">
                        <button aria-label="Toggle Menu">
                            <title>Toggle Menu</title>
                            <Icon icon="ph:list-bold" />
                        </button>
                    </div>
                </div>
                <div class="flex">
                    <nav class="hidden w-full lg:w-auto mt-2 lg:flex lg:mt-0">
                        <ul class="flex flex-col items-center lg:flex-row lg:gap-3">
                            <li
                                class="font-semibold transition ease-in-out delay-150 hover:opacity-85 duration-200 hover:border-b-2 border-tk-text-sidebar"
                            >
                                <RouterLink
                                    to="/#"
                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                >
                                    <span class="text-base font-semibold">TRANG CHỦ</span>
                                </RouterLink>
                            </li>
                            <li
                                class="font-semibold transition ease-in-out delay-150 hover:opacity-85 duration-200 hover:border-b-2 border-tk-text-sidebar"
                            >
                                <RouterLink
                                    to="/#"
                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                >
                                    <span class="text-base font-semibold">TỔNG QUAN</span>
                                </RouterLink>
                            </li>
                            <li
                                class="font-semibold transition ease-in-out delay-150 hover:opacity-85 duration-200 hover:border-b-2 border-tk-text-sidebar mr-5"
                            >
                                <Dropdown>
                                    <div
                                        class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900 cursor-pointer"
                                    >
                                        <span class="pr-2 text-base font-semibold">QUẢN LÝ</span>
                                        <DownOutlined />
                                    </div>
                                    <template #overlay>
                                        <Menu class="p-2" v-if="auth.isLoggedIn">
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 1 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementChatbot"
                                                    class="flex lg:px-3 py-1 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    Quản lý Chatbot
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 1 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementUser"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý tài khoản</span>
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 1 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementRole"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý vai trò</span>
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 1 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementSchool"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý trường học</span>
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 2 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementQuestion"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý câu hỏi</span>
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 2 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementFeedback"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý góp ý</span>
                                                </RouterLink>
                                            </MenuItem>
                                            <MenuItem
                                                v-if="
                                                    auth.payload?.roleID === 3 ||
                                                    auth.payload?.roleID === 2 ||
                                                    auth.payload?.roleID === 4
                                                "
                                            >
                                                <RouterLink
                                                    :to="RoutePath.ManagementDocument"
                                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Quản lý tài liệu</span>
                                                </RouterLink>
                                            </MenuItem>
                                        </Menu>
                                    </template>
                                </Dropdown>
                            </li>

                            <!-- <li
                                class="font-semibold transition ease-in-out delay-150  hover:opacity-85 duration-200"
                            >
                                <RouterLink
                                    :to="RoutePath.ChatbotRegister"
                                    class="flex lg:px-3 py-2 items-center text-gray-600 hover:text-gray-900"
                                >
                                   
                                    <ButtonRegisterChatbot />
                                </RouterLink>
                            </li> -->
                        </ul>
                    </nav>
                    <div class="flex gap-4 items-center">
                        <!-- <LanguageChanger size="large" /> -->
                        <div v-if="!auth.isLoggedIn" class="hidden lg:flex items-center gap-4">
                            <!-- <RouterLink :to="RoutePath.Register"> Đăng nhập </RouterLink> -->
                            <RouterLink
                                :to="RoutePath.Login"
                                class="rounded text-center transition focus-visible:ring-2 ring-offset-2 ring-gray-200 px-4 py-[6px] bg-blue-900 text-white hover:opacity-80 border-2 border-transparent font-semibold shadow-lg"
                            >
                                Đăng nhập
                            </RouterLink>
                        </div>
                        <div v-else class="hidden lg:flex items-center gap-4">
                            <div>
                                <Dropdown :trigger="['click']">
                                    <div
                                        @click.prevent
                                        :class="`w-[222px] flex items-center py-2 px-3 rounded-lg shadow-md cursor-pointer transition ease-in-out delay-350 duration-300 ${
                                            activeScroll ? 'activeScroll-user' : ''
                                        }`"
                                    >
                                        <img
                                            :src="user.avatarUrl || '/icons/cat-avatar.png'"
                                            alt="avatar"
                                            class="avatar w-14 h-14 object-cover rounded-full mr-3"
                                        />
                                        <div class="max-w-[130px] truncate">
                                            <Tooltip
                                                color="#ccc"
                                                :title="user.username"
                                                placement="top"
                                            >
                                                <p class="font-semibold truncate">
                                                    {{ user.username }}
                                                </p>
                                            </Tooltip>
                                            <p class="text-sm">
                                                {{ convertRole(user?.roleID || 0) }}
                                            </p>
                                        </div>
                                    </div>
                                    <template #overlay>
                                        <Menu class="p-2">
                                            <!-- <MenuItem>
                                                <RouterLink
                                                    :to="RoutePath.ManagementChatbot"
                                                    class="flex lg:px-3 py-1 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    Quản lý Chatbot
                                                </RouterLink>
                                            </MenuItem> -->
                                            <MenuItem>
                                                <button
                                                    @click="handleopenPannel(true)"
                                                    class="flex lg:px-3 py-1 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    <span>Hồ sơ cá nhân</span>
                                                </button>
                                            </MenuItem>
                                            <MenuItem>
                                                <button
                                                    @click="auth.logout"
                                                    class="flex lg:px-3 py-1 items-center text-gray-600 hover:text-gray-900"
                                                >
                                                    Đăng xuất
                                                </button>
                                            </MenuItem>
                                        </Menu>
                                    </template>
                                </Dropdown>
                            </div>
                        </div>
                    </div>
                </div>
            </header>
        </div>
        <UserDetail
            v-if="openPannel"
            :openPannel="openPannel"
            :userDetail="user"
            :handleopenPannel="handleopenPannel"
            :isCreate="false"
            :listRole="listRole"
            :isView="true"
            :fetchDataUsers="fetchData"
        />
    </div>
</template>

<style lang="less" scoped>
.nav-bar {
    box-shadow: rgba(0, 0, 0, 0.15) 0px 2px 8px;
}

.activeScroll {
    margin: 4px 0 !important;
}

.activeScroll-user {
    padding: 2px 12px;
    border: none;
    box-shadow: none;
}

.activeScroll-user .avatar {
    width: 40px;
    height: 40px;
    margin-right: 8px;
}
</style>
