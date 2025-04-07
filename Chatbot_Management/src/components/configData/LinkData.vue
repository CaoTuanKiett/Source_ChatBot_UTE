<script setup lang="ts">
import ButtonDelete from '@/components/common/ButtonDelete.vue'
import ELValidate from '@/components/common/ELValidate.vue'
import type { Document } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { TypeData } from '@/utils/constants'
import { removeDocument } from '@/utils/handleDocument'
import { Button, Input, Modal, Skeleton, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref, watch } from 'vue'

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const auth = useAuthStore()

const props = defineProps<{
    folderId: number
}>()

const open = ref<boolean>(false)
const isLoadingData = ref<boolean>(false)
const isLoadingUpload = ref<boolean>(false)
const isLoadingDelete = ref<boolean>(false)
const isValidUrl = ref<boolean>(true)

interface InputInterface {
    content: string
    isValid: boolean
}

const inputs = ref<InputInterface[]>([{ content: '', isValid: false }])

const inputUrl = ref('')
const dataLink = ref<Document[]>([])
// const dataLink = ref<string[]>([])

onMounted(() => {
    console.log('onMounted LinkData')
    fetchData()
})

watch(
    () => props.folderId,
    (newVal, oldVal) => {
        console.log('watch folderId', newVal, oldVal)
        fetchData()
    }
)

const showModal = (item: string) => {
    open.value = true
    inputUrl.value = item
}

const validateUrl = (url: string) => {
    if (url.trim() === '') {
        isValidUrl.value = true
        return isValidUrl.value
    }

    const pattern = new RegExp(
        '^(https?:\\/\\/)?' + // protocol
            '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
            '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
            '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
            '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
            '(\\#[-a-z\\d_]*)?$',
        'i'
    ) // fragment locator
    isValidUrl.value = !pattern.test(url)

    return isValidUrl.value
}

const fetchData = async () => {
    isLoadingData.value = true
    try {
        const response = await axios.get(
            `${VITE_API_URL}/${VITE_API_VERSION}/documents/${props.folderId}/${TypeData.DataLink}`
        )
        console.log('response', response)
        dataLink.value = response.data
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingData.value = false
    }
}

const addInput = () => {
    inputs.value.push({ content: '', isValid: false })
}

const removeInput = (index: number) => {
    inputs.value.splice(index, 1)
}

const importData = async () => {
    try {
        isLoadingUpload.value = true

        // const isAllValid = inputs.value.some((input) => input.isValid)
        if (validateListInput(inputs.value)) {
            isLoadingUpload.value = false
            return
        }

        const formData = new FormData()
        inputs.value
            .filter((input) => input.content.trim() !== '')
            .forEach((input) => {
                formData.append('links', input.content)
            })

        formData.append('folderId', props.folderId.toString())
        formData.append('createdBy', auth.payload?.username || 'Admin')
        formData.append('description', 'File đã được xử lý và lưu trữ thành công.')
        formData.append('dataType', TypeData.DataLink.toString())

        const response = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/documents`, formData)
        console.log('response', response)

        inputs.value = [{ content: '', isValid: false }]
        fetchData()
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingUpload.value = false
    }
}

const clearAll = () => {
    dataLink.value = []
    // inputs.value = [{ content: '' }]
}

const removeData = async (idDocument: number) => {
    await removeDocument(idDocument, isLoadingDelete, fetchData)
}

const validateListInput = (inputs: InputInterface[]) => {
    inputs.forEach((input) => {
        if (input.content.trim() === '') {
            input.isValid = true
        } else {
            input.isValid = false
        }
    })

    return inputs.some((input) => input.isValid)
}

defineExpose({ dataLink, fetchData })
</script>

<template>
    <div class="link-data w-full h-[506px] overflow-y-auto pr-2">
        <div class="w-full">
            <!-- <h1>Nhập URL để hiển thị trang</h1>
            <input v-model="inputUrl" type="text" placeholder="Nhập URL" />
            <button @click="showModal">Hiển thị trang</button> -->

            <div v-for="(input, index) in inputs" :key="index">
                <div class="mb-3">
                    <p class="text-sm font-semibold mb-1">Link {{ index + 1 }}</p>
                    <div class="relative w-full">
                        <Input
                            :status="isValidUrl ? '' : 'error'"
                            v-model:value="input.content"
                            type="text"
                            placeholder="Nhập URL"
                            class="border-[1px] border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm w-full"
                            :class="input.isValid ? '' : 'border-red-500 border-2'"
                            @blur="input.isValid = validateUrl(input.content)"
                        />
                        <img
                            v-if="index !== 0"
                            @click="removeInput(index)"
                            src="/icons/icon-delete.svg"
                            alt="delete"
                            class="absolute top-[-8px] right-[-8px] cursor-pointer shadow-sm"
                        />
                        <ELValidate :isValid="input.isValid" content="Vui lòng nhập URL hợp lệ!" />
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between mt-4">
            <Button
                @click="addInput"
                class="button2 flex justify-center items-center h-10 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
            >
                <img src="/icons/plus-black.svg" alt="add" class="pr-2 w-6" />
                Thêm link
            </Button>
            <Button
                :loading="isLoadingUpload"
                @click="importData"
                class="button2 flex justify-center items-center h-10 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
            >
                <img src="/icons/cloud-arrow-up-solid.svg" alt="import" class="pr-2 w-7" />
                Nhập
            </Button>
        </div>

        <div class="mt-8">
            <div class="flex justify-between mb-4">
                <p class="text-lg font-semibold">Data</p>
                <button
                    v-if="dataLink.length > 0"
                    @click="clearAll"
                    class="button2 flex justify-center items-center h-8 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
                >
                    <img src="/icons/icon-delete-black.svg" alt="delete all" class="pr-2" />
                    Xóa tất cả
                </button>
            </div>
            <Skeleton :loading="isLoadingData" :active="true" :paragraph="{ rows: 4 }">
                <div
                    class="h-[280px] overflow-y-auto mt-1 px-2 py-2 border-[1px] border-slate-400 rounded"
                >
                    <div v-if="dataLink.length === 0" class="flex justify-center items-center">
                        <img src="/images/img-noItem.png" alt="no item" class="w-40" />
                    </div>

                    <div
                        v-else
                        v-for="(item, index) in dataLink"
                        :key="index"
                        class="border-[1px] border-black p-2 rounded mb-2 transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-106 hover:bg-slate-200 hover:shadow-lg duration-150 hover:z-50"
                    >
                        <Tooltip color="#ccc" placement="top" width="900px">
                            <template #title>
                                <span class="text-xs text-black whitespace-pre-wrap">
                                    Xem chi tiết</span
                                >
                            </template>
                            <div class="flex justify-between items-center">
                                <div
                                    class="flex items-center space-x-2 cursor-pointer"
                                    @click="showModal(item.documentName)"
                                >
                                    <p class="border-r-2 border-black pr-2">00{{ index + 1 }}</p>
                                    <p
                                        class="max-w-[484px] text-nowrap text-ellipsis overflow-hidden"
                                    >
                                        {{ item.documentName }}
                                    </p>
                                </div>
                                <div>
                                    <ButtonDelete
                                        :handleDelete="removeData"
                                        :id="item.idDocument"
                                        :title="'Xác nhận xóa tài liệu?'"
                                        :isLoadingDelete="isLoadingDelete"
                                        srcIcon="/icons/icon-delete-black.svg"
                                    />
                                </div>
                            </div>
                        </Tooltip>
                    </div>
                </div>
            </Skeleton>
        </div>

        <div v-if="open">
            <Modal v-model:open="open" title="Page" width="1280px" class="overflow-auto">
                <template #footer> </template>
                <div>
                    <iframe :src="inputUrl" width="100%" height="600px"></iframe>
                </div>
            </Modal>
        </div>
    </div>
</template>

<style scoped>
#app {
    text-align: center;
    margin-top: 20px;
}

iframe {
    border: none;
}

.button2:hover img {
    opacity: 0.45;
    transition-duration: 300ms;
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}
</style>
