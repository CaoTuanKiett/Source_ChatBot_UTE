<script setup lang="ts">
import Navbar from '@/components/shared/Navbar.vue'
import { RoutePath } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const auth = useAuthStore()
const url = computed(() => route.path)

// onMounted(() => {
//     console.log('onMounted Management', auth.payload)
// })

const isAdminSystem = (menuName: string) => {
    const listMenuAdminSystem = [
        'Quản Lý Chatbot',
        'Quản Lý Tài Khoản',
        'Quản Lý Vai Trò',
        'Quản Lý Trường'
    ]

    if (auth.payload?.roleID === 1 && listMenuAdminSystem.includes(menuName)) {
        return true
    }

    return false
}

const isAdmissionsManagement = (menuName: string) => {
    const listMenuAdmissionsManagement = ['Quản Lý Câu Hỏi', 'Quản Lý Góp Ý', 'Quản Lý Tài Liệu']

    if (auth.payload?.roleID === 2 && listMenuAdmissionsManagement.includes(menuName)) {
        return true
    }

    return false
}

const isDocumentManagement = (menuName: string) => {
    const listMenuDocumentManagement = ['Quản Lý Tài Liệu']

    if (auth.payload?.roleID === 3 && listMenuDocumentManagement.includes(menuName)) {
        return true
    }

    return false
}

const isAuthorizedMenu = (menuName: string) => {
    const menuPermissions: { [key: number]: string[] } = {
        1: ['Quản Lý Chatbot', 'Quản Lý Tài Khoản', 'Quản Lý Vai Trò', 'Quản Lý Trường'],
        2: ['Quản Lý Câu Hỏi', 'Quản Lý Góp Ý', 'Quản Lý Tài Liệu'],
        3: ['Quản Lý Tài Liệu'],
        4: [
            'Quản Lý Chatbot',
            'Quản Lý Tài Khoản',
            'Quản Lý Vai Trò',
            'Quản Lý Trường',
            'Quản Lý Câu Hỏi',
            'Quản Lý Góp Ý',
            'Quản Lý Tài Liệu'
        ]
    }

    const userRoleID = auth.payload?.roleID ?? -1

    return menuPermissions[userRoleID]?.includes(menuName) || false
}

const listMenu = [
    {
        name: 'Quản Lý Chatbot',
        router: RoutePath.ManagementChatbot,
        icon: '/icons/robot-solid.svg',
        iconActive: '/icons/robot-active.svg'
    },
    {
        name: 'Quản Lý Tài Khoản',
        router: RoutePath.ManagementUser,
        icon: '/icons/users-solid.svg',
        iconActive: '/icons/users-active.svg'
    },
    {
        name: 'Quản Lý Vai Trò',
        router: RoutePath.ManagementRole,
        icon: '/icons/users-gear-solid.svg',
        iconActive: '/icons/users-gear-active.svg'
    },
    {
        name: 'Quản Lý Câu Hỏi',
        router: RoutePath.ManagementQuestion,
        icon: '/icons/circle-question-solid.svg',
        iconActive: '/icons/circle-question-active.svg'
    },
    {
        name: 'Quản Lý Góp Ý',
        router: RoutePath.ManagementFeedback,
        icon: '/icons/comments-solid.svg',
        iconActive: '/icons/comments-active.svg'
    },
    {
        name: 'Quản Lý Tài Liệu',
        router: RoutePath.ManagementDocument,
        icon: '/icons/folder-solid.svg',
        iconActive: '/icons/folder-active.svg'
    },
    {
        name: 'Quản Lý Trường',
        router: RoutePath.ManagementSchool,
        icon: '/icons/school-solid.svg',
        iconActive: '/icons/school-active.svg'
    }
]
</script>

<template>
    <div class="w-full h-screen">
        <Navbar />
        <div class="flex justify-between h-screen relative">
            <div class="side-bar w-1/6 h-full fixed left-0 pt-32 z-40">
                <RouterLink
                    v-for="menu in listMenu"
                    :key="menu.name"
                    :to="menu.router"
                    class="flex items-center h-14 text-base font-semibold hover:bg-gray-200 transition delay-150"
                    :class="!isAuthorizedMenu(menu.name) ? 'hidden' : ''"
                >
                    <span
                        v-if="url === menu.router"
                        :class="url === menu.router ? 'bg-tk-text-sidebar' : ''"
                        class="h-full w-1 transition"
                    >
                    </span>
                    <img
                        :src="url === menu.router ? menu.iconActive : menu.icon"
                        :alt="'icon-' + menu.name"
                        class="mr-4 ml-4 w-6 transition"
                    />
                    <p
                        :class="url === menu.router ? 'text-tk-text-sidebar ' : ''"
                        class="transition"
                    >
                        {{ menu.name }}
                    </p>
                </RouterLink>
            </div>
            <div class="w-5/6 h-full absolute right-0 pt-[86px] flex justify-center">
                <slot />
            </div>
        </div>
    </div>
</template>

<style scoped>
.side-bar {
    box-shadow: rgba(9, 30, 66, 0.25) 0px 4px 8px -2px, rgba(9, 30, 66, 0.08) 0px 0px 0px 1px;
}
</style>
