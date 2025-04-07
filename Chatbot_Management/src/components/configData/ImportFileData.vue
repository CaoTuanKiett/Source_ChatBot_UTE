<script lang="ts" setup>
import ButtonDelete from '@/components/common/ButtonDelete.vue'
import { useAuthStore } from '@/stores/auth'
import { TypeData } from '@/utils/constants'
import { removeDocument } from '@/utils/handleDocument'
import { InboxOutlined } from '@ant-design/icons-vue'
import { Button, Skeleton, UploadDragger } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref, watch } from 'vue'

const props = defineProps<{
    folderId: number
}>()

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const fileList = ref<any[]>([])
const dataFile = ref<any>([])
const data = ref<string[]>([])
const isLoading = ref<boolean>(false)
const isLoadingData = ref<boolean>(false)
const isLoadingDelete = ref<boolean>(false)

onMounted(() => {
    console.log('onMounted ImportFileData')

    fetchData()
})

watch(
    () => props.folderId,
    (newVal, oldVal) => {
        console.log('watch folderId', newVal, oldVal)
        fetchData()
    }
)

const fetchData = async () => {
    isLoadingData.value = true
    try {
        const response = await axios.get(
            `${VITE_API_URL}/${VITE_API_VERSION}/documents/${props.folderId}/${TypeData.DataImportFile}`
        )
        console.log('response', response)
        dataFile.value = response.data
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingData.value = false
    }
}

function handleDrop(e: DragEvent) {
    console.log(e)
}

const handleChange = (file: any) => {
    console.log('file', file)
}

const handleRemove = async (idDocument: number) => {
    await removeDocument(idDocument, isLoadingDelete, fetchData)
}

const beforeUpload = (file: any) => {
    console.log('file', file)
    fileList.value = [...fileList.value, file]
    return false
}

const handleUpload = async () => {
    isLoading.value = true
    console.log('fileList', fileList.value)
    const formData = new FormData()

    fileList.value.forEach((file) => {
        console.log('file', file)

        if (file?.originFileObj) {
            formData.append('files', file.originFileObj)
        }
    })
    formData.append('folderId', props.folderId.toString())
    formData.append('description', 'File đã được xử lý và lưu trữ thành công.')
    formData.append('createdBy', auth.payload?.username || 'Admin')
    formData.append('dataType', TypeData.DataImportFile.toString())
    formData.append('typeData', TypeData.DataImportFile.toString())

    console.log('formData', formData)
    try {
        const response = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/documents`, formData)
        console.log('response', response)
        fileList.value = []
        fetchData()
        isLoading.value = false
    } catch (error) {
        isLoading.value = false
        console.log('error', error)
    }
}

const handleDleteFile = (file: any) => {
    const index = fileList.value.indexOf(file)
    const newFileList = fileList.value.slice()
    newFileList.splice(index, 1)
    fileList.value = newFileList
}

defineExpose({ fileList, fetchData })
</script>
<template>
    <div class="import-file w-full h-[506px] overflow-y-auto pr-2 relative">
        <div class="">
            <h1 class="font-medium text-base">Tải file lên:</h1>
            <div>
                <UploadDragger
                    v-model:fileList="fileList"
                    name="file"
                    :multiple="true"
                    @drop="handleDrop"
                    :beforeUpload="beforeUpload"
                    @remove="handleDleteFile"
                    @change="handleChange"
                    preview
                    class="rounded w-full border-[1px] border-dashed border-black"
                    accept=".pdf,.doc,.docx,.txt,.xlsx,.xls,.csv"
                >
                    <p class="ant-upload-drag-icon mb-2">
                        <inbox-outlined></inbox-outlined>
                    </p>
                    <p class="ant-upload-text text-xs">
                        Kéo và thả file vào đây hoặc click để chọn file
                        <span class="ant-upload-hint">(.pdf,.doc,.docx,.txt,.xlsx,.xls,.csv)</span>
                    </p>

                    <template #itemRender="{ file }">
                        <div class="flex justify-between items-center rounded">
                            <div
                                class="flex items-center"
                                :style="file.status === 'error' ? 'color: red' : ''"
                            >
                                <p>001</p>
                                <p>{{ file.name }}</p>
                            </div>
                            <button @click="handleDleteFile(file)">
                                <img
                                    src="/icons/icon-delete-black.svg"
                                    alt="delete"
                                    class="cursor-pointer"
                                />
                            </button>
                        </div>
                    </template>
                </UploadDragger>
            </div>
            <div class="p-2 bg-white rounded">
                <div class="">
                    <Button
                        class="flex justify-center items-center px-4 py-2 rounded border-[1px] text-sm font-medium border-black hover:opacity-70 hover:shadow-tk-btn shadow-lg hover:-translate-y-1 hover:scale-104 transition ease-in-out delay-150"
                        @click="handleUpload"
                        :disabled="fileList.length === 0"
                        :loading="isLoading"
                    >
                        <img
                            src="/icons/cloud-arrow-up-solid.svg"
                            alt="cloud-arrow-up-solid.svg"
                            class="w-8 pr-2"
                        />
                        Nhập File
                    </Button>
                </div>
            </div>
        </div>
        <div>
            <h1 class="font-medium text-base">Tài liệu:</h1>
            <Skeleton :loading="isLoadingData" :active="true" :paragraph="{ rows: 4 }">
                <div
                    class="h-[180px] overflow-y-auto mt-1 px-2 py-2 border-[1px] border-slate-400 rounded"
                >
                    <div v-if="dataFile.length === 0" class="flex justify-center items-center">
                        <img src="/images/img-noItem.png" alt="no item" class="w-40" />
                    </div>
                    <div v-else>
                        <div
                            class="flex justify-between items-center rounded border-[1px] border-black p-2 mb-2"
                            v-for="(file, index) in dataFile"
                            :key="index"
                        >
                            <div class="flex items-center">
                                <p class="border-r-[1px] border-black pr-2">
                                    {{ file?.idDocument }}
                                </p>
                                <p class="pl-2">{{ file.documentName }}</p>
                            </div>
                            <ButtonDelete
                                :handleDelete="handleRemove"
                                :id="file.idDocument"
                                :title="'Xác nhận xóa tài liệu?'"
                                :isLoadingDelete="isLoadingDelete"
                                srcIcon="/icons/icon-delete-black.svg"
                            />
                        </div>
                    </div>
                </div>
            </Skeleton>
        </div>
    </div>
</template>

<style>
.import-file .ant-upload-wrapper {
    display: inline-block;
    height: 90px !important;
}

.import-file .ant-upload-list {
    margin-top: 12px;
    padding: 12px;
    max-height: 120px;
    overflow-y: auto;
}

.import-file .ant-upload-btn {
    height: 50px !important;
    padding: 10px 16px !important;
}

.import-file .ant-upload-drag-icon {
    margin-bottom: 4px !important;
}

.import-file .ant-upload-list-item-container {
    border: 1px solid #d9d9d9;
    padding: 4px 8px;
    background-color: #cbd5e1;
    margin-bottom: 8px;
    border-radius: 4px;
    height: 32px !important;
    /* display: flex; */
    /* align-items: center;
    justify-content: space-between; */
}

.import-file .ant-upload-list-item {
    margin-top: 0px !important;
}

.import-file .ant-upload-list-item-name {
    color: black !important;
}

.import-file .anticon-paper-clip {
    fill: black !important;
}
</style>
