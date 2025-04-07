<script setup lang="ts">
import { TabPane, Tabs } from 'ant-design-vue'
import { onMounted, reactive, ref, watch } from 'vue'

import ConfigData from '@/components/chatbot/ConfigData.vue'
import Information from '@/components/chatbot/Information.vue'
import { alertNotification } from '@/utils/notification'

const props = defineProps({
    handleClose: Function,
    isCreateNew: Boolean,
    dataChatbotDetail: Object
})

const activeKey = ref('1')
const informationRef = ref<InstanceType<typeof Information> | null>(null)
const configDataRef = ref<InstanceType<typeof ConfigData> | null>(null)

const dataInfor = reactive({
    idChatBot: props.dataChatbotDetail?.idChatBot || 0,
    nameChatbot: props.dataChatbotDetail?.chatBotName || '',
    description: props.dataChatbotDetail?.description || '',
    status: props.dataChatbotDetail?.status ?? 1,
    folderId: props.dataChatbotDetail?.folderId || 0
})

const dataConfig = ref([])

const handleUpdateFolderID = (id: number) => {
    console.log('handleUpdateFolderID', id)

    dataInfor.folderId = id
}

const handleNextTab = async () => {
    if (informationRef.value) {
        const isValid = await informationRef.value.validateData()
        if (!isValid) {
            alertNotification('Thất bại', 'Vui lòng nhập đầy đủ thông tin', false)
            return
        }
    }
    if (informationRef.value && typeof informationRef.value.handleCreateChatbot === 'function') {
        await informationRef.value.handleCreateChatbot()
    }

    if (configDataRef.value) {
        configDataRef.value.resetData()
    }

    activeKey.value = (parseInt(activeKey.value) + 1).toString()
}

const handlePrevTab = () => {
    activeKey.value = (parseInt(activeKey.value) - 1).toString()
}

watch(activeKey, (newVal, oldVal) => {
    console.log('activeKey', newVal, oldVal)
    if (newVal === '2') {
        if (configDataRef.value) {
            configDataRef.value.resetData()
        }
    }
})

const handleFinish = () => {
    alertNotification(
        'Tuyệt vời',
        '<p>Chatbot đã được tạo thành công. Hãy <span class="font-semibold">thử nghiệm</span> nó ngay</p>',
        true
    )
    props.handleClose && props.handleClose()
}

onMounted(() => {
    console.log('onMounted AddNewChatbot')
})
</script>

<template>
    <div class="add-new-chatbot w-full relative h-[600px]">
        <div class="max-w-screen-xl">
            <Tabs v-model:activeKey="activeKey" centered class="h-100">
                <TabPane key="1" tab="Thông tin chung">
                    <Information
                        ref="informationRef"
                        :dataInfor="dataInfor"
                        :isCreateNew="props.isCreateNew"
                        :handleUpdateFolderID="handleUpdateFolderID"
                    />
                </TabPane>
                <TabPane key="2" tab="Dữ liệu">
                    <ConfigData
                        ref="configDataRef"
                        :testDataConfig="dataConfig"
                        :isCreateNew="props.isCreateNew"
                        :folderId="dataInfor.folderId"
                    />
                </TabPane>
            </Tabs>
        </div>
        <div class="flex justify-end absolute right-0 bottom-[-16px]">
            <button
                v-if="activeKey !== '1'"
                @click="handlePrevTab"
                class="flex justify-center items-center px-4 py-2 bg-tk-btn-color rounded text-white text-sm font-medium mr-4 shadow-tk-btn transition ease-in-out delay-100 hover:-translate-y-1 hover:scale-104 hover:bg-tk-hover duration-150"
                onclick=""
            >
                <img src="/icons/arrow-back.svg" alt="back" class="pr-2" />
                Quay lại
            </button>
            <button
                v-if="activeKey !== '2'"
                @click="handleNextTab"
                class="flex justify-center items-center px-4 py-2 bg-tk-btn-color-primary rounded text-white text-sm font-medium shadow-tk-btn transition ease-in-out delay-100 hover:-translate-y-1 hover:scale-104 hover:bg-tk-hover duration-150"
            >
                Tiếp theo
                <img src="/icons/arrow-back.svg" alt="back" class="pr-2 rotate-180" />
            </button>
            <button
                v-if="activeKey == '2'"
                @click="handleFinish"
                class="flex justify-center items-center px-4 py-2 bg-tk-btn-color-primary rounded text-white text-sm font-medium shadow-tk-btn transition ease-in-out delay-100 hover:-translate-y-1 hover:scale-104 hover:bg-tk-hover duration-150"
            >
                Hoàn thành
                <img src="/icons/complete.svg" alt="back" class="pl-2" />
            </button>
        </div>
    </div>
</template>

<style>
.add-new-chatbot .ant-tabs-tab-btn {
    font-size: 16px;
    text-transform: uppercase;
}

.add-new-chatbot .ant-tabs-tab-active .ant-tabs-tab-btn {
    font-weight: 600;
    color: #0879a6 !important;
}
</style>
