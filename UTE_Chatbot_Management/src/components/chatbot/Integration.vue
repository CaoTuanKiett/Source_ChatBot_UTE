<script setup lang="ts">
import { RadioGroup } from 'ant-design-vue'
import { defineProps, ref, watch } from 'vue'

const props = defineProps<{
    testDataIntegration: {
        integrationMethod: string
        accountName: string
        password: string
        token: string
        verificationCode: string
    }
}>()

const dataIntegration = ref({
    integrationMethod: props.testDataIntegration.integrationMethod,
    accountName: props.testDataIntegration.accountName,
    password: props.testDataIntegration.password,
    token: props.testDataIntegration.token,
    verificationCode: props.testDataIntegration.verificationCode
})

const plainOptions = [
    {
        label: 'Tích hợp qua API',
        value: 'api'
    },
    {
        label: 'Tích hợp Messenger',
        value: 'messenger'
    },
    {
        label: 'Tích hợp Booking.com',
        value: 'booking'
    }
]

watch(
    () => props.testDataIntegration,
    (newVal) => {
        dataIntegration.value = { ...newVal }
    },
    { immediate: true }
)

const fetchData = () => {
    console.log('Fetching data Integration...')
}

defineExpose({ fetchData, dataIntegration })
</script>

<template>
    <div class="integration w-9/12 m-auto">
        <div class="mt-6">
            <p class="text-xl">1.Phương thức tích hợp</p>
            <RadioGroup
                v-model:value="dataIntegration.integrationMethod"
                :options="plainOptions"
                class="flex flex-col p-4"
            />
        </div>
        <div class="mt-5">
            <p class="text-xl">2.Thông tin tài khoản</p>
            <div class="flex flex-wrap">
                <div class="px-6 py-4">
                    <p class="text-sm text-black font-semibold pb-1">Tên tài khoản</p>
                    <input
                        v-model="dataIntegration.accountName"
                        type="text"
                        class="border-2 w-96 border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm"
                    />
                </div>
                <div class="px-6 py-4">
                    <p class="text-sm text-black font-semibold pb-1">Mật khẩu</p>
                    <input
                        v-model="dataIntegration.password"
                        type="password"
                        class="border-2 w-96 border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm"
                    />
                </div>
                <div v-if="dataIntegration.integrationMethod !== 'messenger'" class="px-6 py-4">
                    <p class="text-sm text-black font-semibold pb-1">Token</p>
                    <input
                        v-model="dataIntegration.token"
                        type="password"
                        class="border-2 w-96 border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm"
                    />
                </div>
                <div v-if="dataIntegration.integrationMethod === 'api'" class="px-6 py-4">
                    <p class="text-sm text-black font-semibold pb-1">Mã xác thực</p>
                    <input
                        v-model="dataIntegration.verificationCode"
                        type="password"
                        class="border-2 w-96 border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.integration .ant-radio-wrapper {
    margin-bottom: 10px;
}
</style>
