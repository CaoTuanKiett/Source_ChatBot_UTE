<!-- <script setup lang="ts">
import { TabPane, Tabs } from 'ant-design-vue'
import { nextTick, onMounted, ref, watch } from 'vue'

import ConfigData from '@/components/chatbot/ConfigData.vue'
import Information from '@/components/chatbot/Information.vue'
import Integration from '@/components/chatbot/Integration.vue'
import ChatExample from '@/components/common/ChatExample.vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const chatbotId = route.params.id

// const inputValue = ref('')
const activeKey = ref('1')
// const informationRef = ref(null)
const dataRegister = ref({
    dataInfo: {
        nameCompany: '',
        address: '',
        email: '',
        phone: '',
        nameChatbot: '',
        service: ''
    },
    dataIntegration: {
        integrationMethod: '',
        accountName: '',
        password: '',
        token: '',
        verificationCode: ''
    },
    dataConfig: {
        dataFile: [],
        dataImportFile: [],
        dataLink: [],
        dataQA: []
    }
})

type DataConfigFormat = {
    dataFile: any[]
    dataImportFile: any[]
    dataLink: any[]
    dataQA: any[]
}

const handleNextTab = () => {
    activeKey.value = (parseInt(activeKey.value) + 1).toString()
}

const handlePrevTab = () => {
    activeKey.value = (parseInt(activeKey.value) - 1).toString()
}
const informationRef = ref<InstanceType<typeof Information> | null>(null)
const integrationRef = ref<InstanceType<typeof Integration> | null>(null)
const configDataRef = ref<InstanceType<typeof ConfigData> | null>(null)

watch(activeKey, (newValue, oldValue) => {
    if (oldValue === '1' && informationRef.value) {
        if (typeof informationRef.value.fetchData === 'function') {
            informationRef.value.fetchData()
        } else {
            console.error('fetchData is not a function on Information component')
        }
    }

    if (oldValue === '2' && integrationRef.value) {
        if (typeof integrationRef.value.fetchData === 'function') {
            integrationRef.value.fetchData()
        } else {
            console.error('fetchData is not a function on Information component')
        }
    }

    if (oldValue === '3' && configDataRef.value) {
        if (typeof configDataRef.value.fetchData === 'function') {
            configDataRef.value.fetchData()
        } else {
            console.error('fetchData is not a function on Information component')
        }
    }

    // if (newValue === '4') {
    //     dataRegister.value = {
    //         dataInfo: informationRef.value?.dataInfo,
    //         dataIntegration: integrationRef.value?.dataIntegration,
    //         dataConfig: configDataRef.value?.dataConfig
    //     }

    //     // console.log('dataRegister', dataRegister.value)
    // }
})

const resetData = () => {
    if (informationRef.value && informationRef.value.dataInfo) {
        informationRef.value.dataInfo.nameCompany = ''
        informationRef.value.dataInfo.address = ''
        informationRef.value.dataInfo.email = ''
        informationRef.value.dataInfo.phone = ''
        informationRef.value.dataInfo.nameChatbot = ''
        informationRef.value.dataInfo.service = ''
    }

    if (integrationRef.value && integrationRef.value.dataIntegration) {
        integrationRef.value.dataIntegration.integrationMethod = ''
        integrationRef.value.dataIntegration.accountName = ''
        integrationRef.value.dataIntegration.password = ''
        integrationRef.value.dataIntegration.token = ''
        integrationRef.value.dataIntegration.verificationCode = ''
    }

    console.log('configDataRef', configDataRef.value)

    if (configDataRef.value && configDataRef.value.dataConfig) {
        configDataRef.value.activeKey = '1'

        if (Array.isArray(configDataRef.value.dataConfig.dataFile)) {
            configDataRef.value.dataConfig.dataFile.length = 0
        }

        if (Array.isArray(configDataRef.value.dataConfig.dataImportFile)) {
            configDataRef.value.dataConfig.dataImportFile.length = 0
        }

        if (Array.isArray(configDataRef.value.dataConfig.dataLink)) {
            configDataRef.value.dataConfig.dataLink.length = 0
        }

        if (Array.isArray(configDataRef.value.dataConfig.dataQA)) {
            configDataRef.value.dataConfig.dataQA.length = 0
        }
    }
}

const handleFinish = () => {
    const dataCheck: DataConfigFormat = {
        dataFile: configDataRef.value?.dataConfig?.dataFile
            ? Array.from(configDataRef.value?.dataConfig?.dataFile)
            : [],
        dataImportFile: configDataRef.value?.dataConfig?.dataImportFile
            ? Array.from(configDataRef.value?.dataConfig?.dataImportFile).map((item: any) => {
                  const newItem = Object.assign({}, item)
                  if (newItem.originFileObj && typeof newItem.originFileObj === 'object') {
                      newItem.originFileObj = { ...newItem.originFileObj }
                  }

                  return newItem
              })
            : [],
        dataLink: configDataRef.value?.dataConfig?.dataLink
            ? Array.from(configDataRef.value?.dataConfig?.dataLink)
            : [],
        dataQA: configDataRef.value?.dataConfig?.dataQA
            ? Array.from(configDataRef.value?.dataConfig?.dataQA).map((item: any) => {
                  return Object.assign({}, item)
              })
            : []
    }

    const data = {
        id: Date.now(),
        status: 'true',
        dataInfo: {
            nameCompany: informationRef.value?.dataInfo?.nameCompany,
            address: informationRef.value?.dataInfo?.address,
            email: informationRef.value?.dataInfo?.email,
            phone: informationRef.value?.dataInfo?.phone,
            nameChatbot: informationRef.value?.dataInfo?.nameChatbot,
            service: informationRef.value?.dataInfo?.service
        },
        dataIntegration: {
            integrationMethod: integrationRef.value?.dataIntegration?.integrationMethod,
            accountName: integrationRef.value?.dataIntegration?.accountName,
            password: integrationRef.value?.dataIntegration?.password,
            token: integrationRef.value?.dataIntegration?.token,
            verificationCode: integrationRef.value?.dataIntegration?.verificationCode
        },
        dataConfig: {
            dataFile: dataCheck.dataFile,
            dataImportFile: dataCheck.dataImportFile,
            dataLink: dataCheck.dataLink,
            dataQA: dataCheck.dataQA
        }
    }

    let existingData = localStorage.getItem('formData')
    let formDataArray: any[] = []

    if (chatbotId) {
        if (existingData) {
            try {
                formDataArray = JSON.parse(existingData)
                if (!Array.isArray(formDataArray)) {
                    formDataArray = []
                }
            } catch (e) {
                console.error('Error parsing formData from localStorage:', e)
                formDataArray = []
            }
        }
        const index = formDataArray.findIndex((item) => item.id == chatbotId)
        if (index !== -1) {
            formDataArray[index] = data
        }
    } else {
        if (existingData) {
            try {
                formDataArray = JSON.parse(existingData)
                if (!Array.isArray(formDataArray)) {
                    formDataArray = []
                }
            } catch (e) {
                console.error('Error parsing formData from localStorage:', e)
                formDataArray = []
            }
        }
        formDataArray.push(data)
    }

    localStorage.setItem('formData', JSON.stringify(formDataArray))
    resetData()
    activeKey.value = '1'

    router.push({ name: 'ChatbotManagement' })
}

onMounted(() => {
    console.log('chatbotId', chatbotId)

    console.log('configDataRef.value', configDataRef)

    nextTick(() => {
        if (chatbotId) {
            const data = localStorage.getItem('formData')
            if (data) {
                try {
                    const parsedData = JSON.parse(data)
                    const chatbot = parsedData.find((item: any) => item.id == chatbotId)
                    // console.log('chatbot', chatbot)

                    dataRegister.value = chatbot

                    // console.log('informationRef.value', informationRef.value)

                    // if (informationRef.value) {
                    //     informationRef.value.dataInfo.nameCompany = chatbot.dataInfo.nameCompany
                    //     informationRef.value.dataInfo.address = chatbot.dataInfo.address
                    //     informationRef.value.dataInfo.email = chatbot.dataInfo.email
                    //     informationRef.value.dataInfo.phone = chatbot.dataInfo.phone
                    //     informationRef.value.dataInfo.nameChatbot = chatbot.dataInfo.nameChatbot
                    //     informationRef.value.dataInfo.service = chatbot.dataInfo.service
                    // }

                    // if (integrationRef.value) {
                    //     integrationRef.value.dataIntegration.integrationMethod =
                    //         chatbot.dataIntegration.integrationMethod
                    //     integrationRef.value.dataIntegration.accountName =
                    //         chatbot.dataIntegration.accountName
                    //     integrationRef.value.dataIntegration.password =
                    //         chatbot.dataIntegration.password
                    //     integrationRef.value.dataIntegration.token = chatbot.dataIntegration.token
                    //     integrationRef.value.dataIntegration.verificationCode =
                    //         chatbot.dataIntegration.verificationCode
                    // }
                    // // console.log('configDataRef.value ,put', configDataRef.value)

                    // if (configDataRef.value) {
                    //     console.log('chatbot.dataConfig.dataFile', chatbot.dataConfig.dataFile)

                    //     configDataRef.value.dataConfig.dataFile = chatbot.dataConfig.dataFile
                    //     configDataRef.value.dataConfig.dataImportFile =
                    //         chatbot.dataConfig.dataImportFile
                    //     configDataRef.value.dataConfig.dataLink = chatbot.dataConfig.dataLink
                    //     configDataRef.value.dataConfig.dataQA = chatbot.dataConfig.dataQA
                    // }

                    // if (chatbot) {
                    //     informationRef.value?.setDataInfo(chatbot.dataInfo)
                    //     integrationRef.value?.setDataIntegration(chatbot.dataIntegration)
                    //     configDataRef.value?.setDataConfig(chatbot.dataConfig)
                    // }
                } catch (error) {
                    console.error('Error parsing JSON:', error)
                }
            } else {
                console.log('No data found in localStorage')
            }
        } else {
            resetData()
        }
    })
})
</script>

<template>
    <div class="register-chatbot w-full min-h-screen pt-28 pb-16">
        <div class="max-w-screen-xl">
            <Tabs v-model:activeKey="activeKey" centered class="h-100">
                <TabPane key="1" tab="Thông tin chung">
                    <Information ref="informationRef" :testDataInfor="dataRegister.dataInfo" />
                </TabPane>
                <TabPane key="2" tab="Cấu hình" force-render>
                    <Integration
                        ref="integrationRef"
                        :testDataIntegration="dataRegister.dataIntegration"
                    />
                </TabPane>
                <TabPane key="3" tab="Dữ liệu">
                    <ConfigData ref="configDataRef" :testDataConfig="dataRegister.dataConfig" />
                </TabPane>
                <TabPane key="4" tab="Thử nghiệm"><ChatExample /></TabPane>
            </Tabs>
        </div>

        <div class="fixed bottom-0 right-0 pr-40 py-2 w-full border-2 bg-white">
            <div class="flex justify-end">
                <button
                    v-if="activeKey !== '1'"
                    @click="handlePrevTab"
                    class="flex justify-center items-center px-4 py-2 bg-tk-btn-color rounded text-white text-sm font-medium mr-4 shadow-tk-btn transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 hover:bg-tk-hover duration-200"
                    onclick=""
                >
                    <img src="/icons/arrow-back.svg" alt="back" class="pr-2" />
                    Quay lại
                </button>
                <button
                    v-if="activeKey !== '4'"
                    @click="handleNextTab"
                    class="flex justify-center items-center px-4 py-2 bg-tk-btn-color-primary rounded text-white text-sm font-medium shadow-tk-btn transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 hover:bg-tk-hover duration-200"
                >
                    Tiếp theo
                    <img src="/icons/arrow-back.svg" alt="back" class="pr-2 rotate-180" />
                </button>
                <button
                    v-if="activeKey == '4'"
                    @click="handleFinish"
                    class="flex justify-center items-center px-4 py-2 bg-tk-btn-color-primary rounded text-white text-sm font-medium shadow-tk-btn transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 hover:bg-tk-hover duration-200"
                >
                    Hoàn thành
                    <img src="/icons/complete.svg" alt="back" class="pl-2" />
                </button>
            </div>
        </div>
    </div>
</template>

<style>
.register-chatbot {
    padding: 148px 0;
    box-shadow: rgba(0, 0, 0, 0.2) 0px 12px 28px 0px, rgba(0, 0, 0, 0.1) 0px 2px 4px 0px,
        rgba(255, 255, 255, 0.05) 0px 0px 0px 1px inset;
    /* border-radius: 8px; */
}

.register-chatbot .ant-tabs-tabpane {
    width: 1280px;
    min-height: 56vh;
}

.register-chatbot .ant-tabs-tab-btn {
    font-size: 16px;
    text-transform: uppercase;
}

.register-chatbot .ant-tabs-tab-active .ant-tabs-tab-btn {
    font-weight: 600;
    color: #0879a6 !important;
}
</style> -->
