<script setup lang="ts">
import ButtonDelete from '@/components/common/ButtonDelete.vue'
import ELValidate from '@/components/common/ELValidate.vue'
import type { Document } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { TypeData } from '@/utils/constants'
import { removeDocument } from '@/utils/handleDocument'
import { Button, Skeleton, Textarea } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref, watch } from 'vue'

const props = defineProps<{
    folderId: number
}>()

interface Input {
    content: string
    isValid: boolean
}

const auth = useAuthStore()

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const inputs = ref<Input[]>([{ content: '', isValid: false }])
const dataFile = ref<Document[]>([])
const isLoading = ref<boolean>(false)
const isLoadingData = ref<boolean>(false)
const isLoadingDelete = ref<boolean>(false)

onMounted(() => {
    console.log('onMounted FileData', props.folderId)

    fetchData()
})

watch(
    () => props.folderId,
    (newVal, oldVal) => {
        console.log('watch folderId', newVal, oldVal)
        fetchData()
    }
)

const addInput = () => {
    inputs.value.push({ content: '', isValid: false })
}

const removeInput = (index: number) => {
    inputs.value.splice(index, 1)
}

const fetchData = async () => {
    isLoadingData.value = true
    try {
        const response = await axios.get(
            `${VITE_API_URL}/${VITE_API_VERSION}/documents/${props.folderId}/${TypeData.DataFile}`
        )
        console.log('response', response)
        dataFile.value = response.data
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingData.value = false
    }
}

const importData = async () => {
    isLoading.value = true

    // const isAllValid = inputs.value.some((input) => input.isValid)
    if (validateListInput(inputs.value)) {
        isLoading.value = false
        return
    }

    const filteredInputs = inputs.value.filter((input) => input.content.trim() !== '')

    const formData = new FormData()

    filteredInputs.forEach((input) => {
        formData.append('texts', input.content)
    })

    formData.append('folderId', props.folderId.toString())
    formData.append('description', 'File đã được xử lý và lưu trữ thành công.')
    formData.append('createdBy', auth.payload?.username || 'Admin')
    formData.append('dataType', TypeData.DataFile.toString())

    try {
        const response = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/documents`, formData)
        console.log('response', response)

        inputs.value = [{ content: '', isValid: false }]
        fetchData()
        isLoading.value = false
    } catch (error) {
        isLoading.value = false
        console.log('error', error)
    }
}

const clearAll = () => {
    dataFile.value = []
    // inputs.value = [{ content: '' }]
}

const removeData = async (idDocument: number) => {
    await removeDocument(idDocument, isLoadingDelete, fetchData)
}

const validateInput = (content: string) => {
    return content.trim() === ''
}

const validateListInput = (inputs: Input[]) => {
    inputs.forEach((input) => {
        if (input.content.trim() === '') {
            input.isValid = true
        } else {
            input.isValid = false
        }
    })

    return inputs.some((input) => input.isValid)
}

defineExpose({ dataFile, fetchData })
</script>

<template>
    <div class="file-data w-full h-[506px] overflow-y-auto pr-4">
        <div class="mb-4">
            <div v-for="(input, index) in inputs" :key="index">
                <div class="w-full mb-3">
                    <p class="text-sm font-semibold mb-1">Văn bản {{ index + 1 }}</p>
                    <div class="relative w-full">
                        <Textarea
                            v-model:value="input.content"
                            class="border-[1px] border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm w-full"
                            :rows="4"
                            placeholder="Nhập nội dung"
                            :class="input.isValid ? '' : 'border-red-500 border-2'"
                            @blur="input.isValid = validateInput(input.content)"
                        ></Textarea>
                        <ELValidate :isValid="input.isValid" content="Vui lòng nhập giá trị!" />
                        <img
                            v-if="index !== 0"
                            @click="removeInput(index)"
                            src="/icons/icon-delete.svg"
                            alt="delete"
                            class="absolute top-[-8px] right-[-8px] cursor-pointer shadow-sm"
                        />
                    </div>
                </div>
            </div>
        </div>
        <div class="flex justify-between">
            <button
                @click="addInput"
                class="button2 flex justify-center items-center h-10 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
            >
                <img src="/icons/plus-black.svg" alt="add" class="pr-2 w-6" />
                Thêm văn bản
            </button>
            <Button
                @click="importData"
                :loading="isLoading"
                class="button2 flex justify-center items-center h-10 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
            >
                <img src="/icons/cloud-arrow-up-solid.svg" alt="import" class="pr-2 w-7" />
                Nhập
            </Button>
        </div>
        <div class="bg-white pt-4 rounded">
            <div class="flex justify-between mb-1">
                <p class="text-lg font-semibold">Data</p>
                <!-- <button
                    v-if="dataFile.length > 0"
                    @click="clearAll"
                    class="btn-delete flex justify-center items-center px-2 py-1 bg-tk-btn-color rounded text-white text-sm font-medium shadow-tk-btn transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 hover:bg-tk-hover duration-200"
                >
                    <img src="/icons/icon-delete-white.svg" alt="delete all" class="pr-2" />
                    Xóa tất cả
                </button> -->
            </div>
            <Skeleton :loading="isLoadingData" :active="true" :paragraph="{ rows: 4 }">
                <div
                    class="h-[260px] overflow-y-auto px-2 py-2 border-[1px] border-slate-400 rounded"
                >
                    <div v-if="dataFile.length === 0" class="flex justify-center items-center">
                        <img src="/images/img-noItem.png" alt="no item" class="w-40" />
                    </div>
                    <div
                        v-else
                        v-for="(item, index) in dataFile"
                        :key="index"
                        class="flex justify-between items-center bg-slate-300 p-2 rounded mb-2"
                    >
                        <div class="flex items-center space-x-2">
                            <p class="border-r-2 border-black pr-2">00{{ index + 1 }}</p>
                            <p class="max-w-[484px] text-nowrap text-ellipsis overflow-hidden">
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
                </div>
            </Skeleton>
        </div>
    </div>
</template>

<style >
.file-data {
    /* max-width: 600px; */
    /* margin: auto; */
}

.shadow-tk-btn {
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
