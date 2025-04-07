<script setup lang="ts">
import ELValidate from '@/components/common/ELValidate.vue'
import type { FolderGet, School } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'
import type { SelectProps } from 'ant-design-vue'
import { Button, Input, Select, Textarea } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref, watch } from 'vue'

const auth = useAuthStore()

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL
const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL

const props = defineProps<{
    dataInfor: {
        idChatBot: number
        nameChatbot: string
        description: string
        status: number
        folderId: number
    }
    isCreateNew: boolean
    handleUpdateFolderID: (id: number) => void
}>()

const optionsStatus = ref<SelectProps['options']>([
    {
        value: 1,
        label: 'Hoạt động'
    },
    {
        value: 0,
        label: 'Không hoạt động'
    }
])

const isValidateFolderName = ref(false)
const isValidateName = ref(false)
const isValidateFolder = ref(false)
const chatbotIdNew = ref<number | null>(null)
const isLoadingFolder = ref(false)
const isCreateFolder = ref(false)
const dataFolder = ref<FolderGet[]>([])
const dataFolderDetail = ref<FolderGet>({
    idFolder: 0,
    folderName: '',
    description: '',
    createdAt: ''
})
const dataFolderCreate = ref<any>({
    folderName: '',
    description: '',
    createdBy: auth.payload?.username
})
const dataSchool = ref<School>({
    idSchool: 0,
    schoolName: '',
    schoolCode: '',
    description: '',
    avatarUrl: '',
    dateEstablished: '',
    address: '',
    email: '',
    phone: 0,
    website: '',
    createdTime: ''
})

const dataInfor = ref({
    nameChatbot: props.dataInfor.nameChatbot || '',
    description: props.dataInfor.description || '',
    status: props.dataInfor.status ?? 1,
    folderId: props.dataInfor.folderId || 0
})

watch(
    () => props.dataInfor,
    (newVal) => {
        dataInfor.value = { ...newVal }
    },
    { immediate: true }
)

onMounted(async () => {
    console.log('onMounted Information', props.dataInfor)

    await fetchData()
    if (!props.isCreateNew) {
        const folder = dataFolder.value.find((item) => item.idFolder === dataInfor.value.folderId)
        if (folder) {
            dataFolderDetail.value = folder
        } else {
            dataFolderDetail.value = {
                idFolder: 0,
                folderName: '',
                description: '',
                createdAt: '',
                createdBy: ''
            }
        }
    }
})

const fetchData = async () => {
    console.log('Fetching data Information...')
    // Object.assign(props.dataInfo, dataInfo.value)
    try {
        const apiUrlFolders = `${VITE_API_URL}/${VITE_API_VERSION}/folders`
        const apiUrlSchool = `${VITE_API_URL}/${VITE_API_VERSION}/school/${VITE_ID_SCHOOL}`

        const [responseFolders, responseSchool] = await Promise.all([
            axios.get(apiUrlFolders),
            axios.get(apiUrlSchool)
        ])

        dataFolder.value = responseFolders.data
        dataSchool.value = responseSchool.data

        console.log('dataFolder', dataFolder.value)
        // console.log('dataSchool', dataSchool.value)
    } catch (error) {
        console.log('error', error)
    }
}

const fetchDataFolders = async () => {
    console.log('Fetching data Folders...')
    try {
        const apiUrlFolders = `${VITE_API_URL}/${VITE_API_VERSION}/folders`

        const responseFolders = await axios.get(apiUrlFolders)

        dataFolder.value = responseFolders.data

        console.log('dataFolder', dataFolder.value)
    } catch (error) {
        console.log('error', error)
    }
}

const handleCreateChatbot = async () => {
    const chatbotId = chatbotIdNew.value || props.dataInfor?.idChatBot
    if (chatbotId || !props.isCreateNew) {
        try {
            const data = {
                chatBotName: dataInfor.value.nameChatbot,
                description: dataInfor.value.description,
                status: dataInfor.value.status,
                folderId: dataInfor.value.folderId,
                schoolId: auth.payload?.schoolID,
                updateBy: auth.payload?.username
            }

            const apiUrl = `${VITE_API_URL}/${VITE_API_VERSION}/chatbot/${chatbotId}`
            const res = await axios.put(apiUrl, data)
            if (res.status === 200) {
                console.log('Update', res)
                props.handleUpdateFolderID(dataInfor.value.folderId)
                alertNotification(
                    'Thành công',
                    `<p>Cập nhật thành công chatbot <span class="font-semibold">${data.chatBotName}</span></p>`,
                    true
                )
            } else {
                alertNotification('Thất bại', 'Cập nhật chatbot thất bại', false)
            }
        } catch (error) {
            console.log('error', error)
        }
    } else {
        try {
            const apiUrl = `${VITE_API_URL}/${VITE_API_VERSION}/chatbot`
            const data = {
                chatBotName: dataInfor.value.nameChatbot,
                description: dataInfor.value.description,
                status: dataInfor.value.status,
                folderId: dataInfor.value.folderId,
                schoolId: auth.payload?.schoolID,
                updateBy: auth.payload?.username
            }

            const res = await axios.post(apiUrl, data)
            if (res.status === 200) {
                console.log('Create', res)
                chatbotIdNew.value = res.data.idChatBot
                props.handleUpdateFolderID(res.data.folderId)

                alertNotification(
                    'Thành công',
                    `<p>Tạo thành công chatbot <span class="font-semibold">${res.data.chatBotName}</span></p>`,
                    true
                )
            } else {
                alertNotification('Thất bại', 'Tạo chatbot thất bại', false)
            }
        } catch (error) {
            console.log('error', error)
        }
    }
}

const focusCreateFolder = () => {
    isValidateFolder.value = false
}

const handleChange = (value: number) => {
    console.log(`selected ${value}`)
    const folder = dataFolder.value.find((item) => item.idFolder === value)
    if (folder) {
        dataFolderDetail.value = folder
    } else {
        dataFolderDetail.value = {
            idFolder: 0,
            folderName: '',
            description: '',
            createdAt: '',
            createdBy: ''
        }
    }
    console.log('dataFolderDetail', dataFolderDetail.value)
}

const handleChangeStatus = (value: number) => {
    console.log(`selected ${value}`)
}

const validateData = () => {
    let isValidate = true
    if (dataInfor.value.nameChatbot.trim() === '') {
        isValidateName.value = true
        isValidate = false
    } else {
        isValidateName.value = false
    }

    if (dataInfor.value.folderId === 0) {
        isValidateFolder.value = true
        isValidate = false
    } else {
        isValidateFolder.value = false
    }

    return isValidate
}

const focusNameChatbot = () => {
    isValidateName.value = false
}

const handleShowCreateFolder = async (isCreate: boolean = false) => {
    console.log('handleShowCreateFolder', isCreate)

    if (isCreate) {
        isLoadingFolder.value = true
        try {
            if (dataFolderCreate.value.folderName.trim() === '') {
                isValidateFolderName.value = true
                return
            } else {
                isValidateFolderName.value = false
            }

            const data = {
                folderName: dataFolderCreate.value.folderName,
                description: dataFolderCreate.value.description,
                createdBy: auth.payload?.username
            }

            const res = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/folder`, data)
            if (res.status === 200) {
                console.log('Create Folder', res)
                fetchDataFolders()
                alertNotification(
                    'Thành công',
                    `<p>Tạo thành công folder <span class="font-semibold">${dataFolderCreate.value.folderName}</span></p>`,
                    true
                )

                dataInfor.value.folderId = res.data.idFolder
                dataFolderDetail.value.description = res.data.description

                dataFolderCreate.value.folderName = ''
                dataFolderCreate.value.description = ''
            } else {
                alertNotification('Thất bại', 'Tạo folder thất bại', false)
            }
        } catch (error) {
            console.log('error', error)
        } finally {
            isLoadingFolder.value = false
        }
    }
    isCreateFolder.value = !isCreateFolder.value
}

defineExpose({ fetchData, handleCreateChatbot, validateData })
</script>

<template>
    <div class="information w-9/12 m-auto">
        <div>
            <div>
                <div>
                    <p class="text-xl">1.Thông tin chatbot:</p>
                    <div class="flex flex-wrap justify-center">
                        <div>
                            <div class="px-6 py-2">
                                <p class="text-sm text-black font-semibold pb-1">Tên chatbot</p>
                                <input
                                    v-model="dataInfor.nameChatbot"
                                    type="text"
                                    placeholder="Nhập tên chatbot"
                                    class="border-2 w-96 border-slate-400 rounded p-2 text-sm shadow-tk-btn-2 focus:border-tk-btn-color-primary focus:outline-none"
                                    @focus="focusNameChatbot"
                                />
                                <ELValidate
                                    :isValid="isValidateName"
                                    content="Tên chatbot không được để trống"
                                />
                            </div>

                            <div class="px-6 py-2">
                                <p class="text-sm text-black font-semibold pb-1">Trường</p>
                                <input
                                    disabled
                                    v-model="dataSchool.schoolName"
                                    type="text"
                                    class="border-2 w-96 border-slate-400 rounded p-2 text-sm shadow-tk-btn-2 focus:border-tk-btn-color-primary focus:outline-none"
                                />
                            </div>
                            <div class="px-6 py-2">
                                <p class="text-sm text-black font-semibold pb-1">Trạng thái</p>
                                <Select
                                    :disabled="props.isCreateNew"
                                    ref="select"
                                    v-model:value="dataInfor.status"
                                    :options="optionsStatus"
                                    @change="handleChangeStatus(dataInfor.status)"
                                    class="border-2 w-96 border-slate-400 rounded text-sm h-10 items-center flex shadow-tk-btn-2"
                                >
                                </Select>
                            </div>
                        </div>
                        <div class="px-6 py-2">
                            <p class="text-sm text-black font-semibold pb-1">Mô tả</p>
                            <textarea
                                v-model="dataInfor.description"
                                type="text"
                                rows="9"
                                placeholder="Nhập mô tả chatbot"
                                class="border-2 w-96 border-slate-400 rounded p-2 text-sm shadow-tk-btn-2 focus:border-tk-btn-color-primary focus:outline-none"
                            />
                        </div>
                    </div>
                </div>
                <div class="">
                    <p class="text-xl">2.Chọn thư mục tài liệu:</p>
                    <div v-if="!isCreateFolder">
                        <div class="my-4 mx-6">
                            <div class="w-full">
                                <p class="text-sm text-black font-semibold pb-1">Chọn thư mục:</p>
                                <div class="flex items-start">
                                    <Select
                                        ref="select"
                                        placeholder="Chọn thư mục"
                                        v-model:value="dataInfor.folderId"
                                        :options="
                                            dataFolder.map((item) => ({
                                                value: item.idFolder,
                                                label: item.folderName
                                            }))
                                        "
                                        @focus="focusCreateFolder"
                                        @change="handleChange(dataInfor.folderId)"
                                        class="border-2 w-full border-slate-400 rounded text-sm h-10 items-center flex shadow-tk-btn-2 mr-6"
                                    >
                                    </Select>
                                    <button
                                        @click="handleShowCreateFolder()"
                                        class="border-[1px] h-10 w-[190px] px-4 py-2 border-slate-400 rounded text-sm items-center flex shadow-tk-btn-2 hover:opacity-75"
                                    >
                                        Tạo mới thư mục
                                    </button>
                                </div>
                                <ELValidate
                                    :isValid="isValidateFolder"
                                    content="Vui lòng chọn thư mục"
                                />
                            </div>
                        </div>
                        <div>
                            <p class="text-sm text-black font-semibold pb-1 ml-6">Mô tả:</p>
                            <p class="ml-6">{{ dataFolderDetail.description ?? '' }}</p>
                        </div>
                    </div>
                    <div v-else class="mt-2">
                        <div class="flex w-full items-end">
                            <div class="flex flex-col px-6 pb-1 w-full">
                                <label for="name" class="text-sm text-black font-semibold pb-1"
                                    >Tên thư mục:</label
                                >
                                <Input
                                    v-model:value="dataFolderCreate.folderName"
                                    placeholder="Tên Folder"
                                    id="name"
                                    @blur="
                                        isValidateFolderName =
                                            dataFolderCreate.folderName.trim() === ''
                                    "
                                    @focus="isValidateFolderName = false"
                                    class="h-10 w-fullborder-slate-400 rounded p-2 text-sm shadow-tk-btn-2"
                                >
                                    <template #prefix>
                                        <img
                                            src="/icons/folder-solid.svg"
                                            alt="envelope-regular.svg"
                                            class="w-[14px] mr-2"
                                        />
                                    </template>
                                </Input>
                                <ELValidate
                                    :isValid="isValidateFolderName"
                                    content="Tên Folder không được để trống"
                                />
                            </div>
                            <div class="flex justify-end pr-6 pb-1">
                                <button
                                    @click="handleShowCreateFolder()"
                                    class="border-[1px] px-3 py-2 border-slate-400 rounded text-sm items-center flex shadow-tk-btn-2 hover:opacity-75 h-10"
                                >
                                    Hủy
                                </button>
                                <Button
                                    :loading="isLoadingFolder"
                                    @click="handleShowCreateFolder(true)"
                                    class="border-[1px] px-5 py-2 ml-2 bg-tk-btn-color-primary text-white border-slate-400 rounded text-sm items-center flex shadow-tk-btn-2 hover:opacity-75 h-10"
                                >
                                    Lưu
                                </Button>
                            </div>
                        </div>
                        <div class="flex flex-col px-6 py-2">
                            <label for="description" class="text-sm text-black font-semibold pb-1"
                                >Mô tả:</label
                            >
                            <Textarea
                                placeholder="Mô tả"
                                id="description"
                                v-model:value="dataFolderCreate.description"
                                :rows="3"
                                class="h-10 w-full border-slate-400 rounded p-2 text-sm shadow-tk-btn-2"
                            >
                                <template #prefix>
                                    <img
                                        src="/icons/scroll-solid.svg"
                                        alt="envelope-regular.svg"
                                        class="w-4 mr-2"
                                    />
                                </template>
                            </Textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.information .ant-select-selector {
    height: 37px !important;
    display: flex;
    align-items: center;
    border: none !important;
}

.ant-modal-wrap {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    height: 100vh !important;
}

.ant-modal {
    top: 0 !important;
}
</style>
