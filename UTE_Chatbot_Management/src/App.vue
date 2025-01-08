<script setup lang="ts">
import { theme } from '@/theme'
import { ConfigProvider } from 'ant-design-vue'
import { RouterView, useRoute } from 'vue-router'

import AsyncErrorBoundary from '@/components/AsyncErrorBoundary.vue'
import AdminLayout from '@/layouts/admin/index.vue'
import AuthLayout from '@/layouts/auth/index.vue'
import DefaultLayout from '@/layouts/empty/index.vue'
import HomeLayout from '@/layouts/home-page/index.vue'
import LandingLayout from '@/layouts/landing-page/index.vue'
import ManagementLayout from '@/layouts/management/index.vue'
import NoLayout from '@/layouts/no-layout.vue'
import { markRaw, ref, watch } from 'vue'

const layouts: Record<string, typeof DefaultLayout> = {
    default: DefaultLayout,
    auth: AuthLayout,
    admin: AdminLayout,
    'home-page': HomeLayout,
    'landing-page': LandingLayout,
    'no-layout': NoLayout,
    management: ManagementLayout
}

const route = useRoute()

const layout = ref()

watch(
    () => route.meta.layout as string | undefined,
    (layoutName: string | undefined) => {
        if (layoutName === '404') {
            layout.value = undefined
            return
        }
        try {
            layout.value = markRaw(layouts[layoutName || 'default'])
        } catch (err) {
            layout.value = markRaw(layouts['default'])
        }
    },
    { immediate: true }
)
</script>

<template>
    <ConfigProvider :theme="theme">
        <AsyncErrorBoundary />
        <Transition>
            <div v-if="layout" class="w-full h-full">
                <component :is="layout">
                    <RouterView />
                </component>
            </div>
        </Transition>
    </ConfigProvider>
</template>

<style scoped>
/*
    Enter and leave animations can use different
    durations and timing functions.
*/
.fade-enter-active {
    transition: all 0.3s ease;
}

.fade-leave-active {
    transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
