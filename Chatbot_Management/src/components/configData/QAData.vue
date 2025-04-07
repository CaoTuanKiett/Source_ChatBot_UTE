<script setup lang="ts">
import ButtonDelete from '@/components/common/ButtonDelete.vue'
import ELValidate from '@/components/common/ELValidate.vue'
import { useAuthStore } from '@/stores/auth'
import { TypeData } from '@/utils/constants'
import { removeDocument } from '@/utils/handleDocument'
import { Button, Input, Skeleton, Textarea, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, ref, watch } from 'vue'

const props = defineProps<{
    folderId: number
}>()

interface InputInterface {
    question: string
    content: string
    isValid: boolean
}

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const inputs = ref<InputInterface[]>([{ question: '', content: '', isValid: false }])
const dataQA = ref<any[]>([])
// const dataQA = ref<any[]>([])
const isLoadingData = ref<boolean>(false)
const isLoadingUpload = ref<boolean>(false)
const isLoadingDelete = ref<boolean>(false)

onMounted(() => {
    console.log('onMounted QAData')
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
            `${VITE_API_URL}/${VITE_API_VERSION}/documents/${props.folderId}/${TypeData.DataQA}`
        )
        console.log('response', response)
        dataQA.value = response.data
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingData.value = false
    }
}

const addInput = () => {
    inputs.value.push({ question: '', content: '', isValid: false })
}

const removeInput = (index: number) => {
    inputs.value.splice(index, 1)
}

const importData = async () => {
    isLoadingUpload.value = true

    if (validateListInput(inputs.value)) {
        isLoadingUpload.value = false
        return
    }

    const filteredInputs = inputs.value.filter((input) => {
        return input.question.trim() !== '' && input.content.trim() !== ''
    })

    const formData = new FormData()

    filteredInputs.forEach((input) => {
        const dataQuestion = `Câu hỏi: ${input.question}? \nĐáp án: ${input.content}`

        console.log('dataQuestion', dataQuestion)

        formData.append('texts', dataQuestion)
        formData.append('description', dataQuestion)
    })
    formData.append('folderId', props.folderId.toString())

    formData.append('createdBy', auth.payload?.username || 'Admin')
    formData.append('dataType', TypeData.DataQA.toString())

    try {
        const response = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/documents`, formData)
        console.log('response', response)

        inputs.value = [{ question: '', content: '', isValid: false }]
        fetchData()
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingUpload.value = false
    }
}

const clearAll = () => {
    dataQA.value = []
    // inputs.value = [{ content: '' }]
}

const removeData = async (idDocument: number) => {
    await removeDocument(idDocument, isLoadingDelete, fetchData)
}

const validateInput = (input: any) => {
    return input.question.trim() === '' || input.content.trim() === ''
}

const validateListInput = (listInput: any[]) => {
    listInput.forEach((input) => {
        if (input.question.trim() === '' || input.content.trim() === '') {
            input.isValid = true
        } else {
            input.isValid = false
        }
    })

    return listInput.some((input) => input.isValid)
}

defineExpose({ dataQA, fetchData })
</script>

<template>
    <div class="file-data h-[506px] overflow-y-auto pr-2">
        <div class="mb-4">
            <div v-for="(input, index) in inputs" :key="index" class="mb-3">
                <p class="text-sm font-semibold mb-1">Câu hỏi {{ index + 1 }}</p>
                <div class="relative">
                    <Input
                        type="text"
                        v-model:value="input.question"
                        placeholder="Nhập câu hỏi"
                        class="border-[1px] border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm w-full mb-2"
                    />
                    <Textarea
                        v-model:value="input.content"
                        class="border-[1px] border-slate-400 shadow-tk-btn-2 rounded p-2 text-sm w-full"
                        :rows="4"
                        placeholder="Nhập câu trả lời"
                        @blur="input.isValid = validateInput(input)"
                    ></Textarea>
                    <ELValidate :isValid="input.isValid" content="Vui lòng đầy đủ giá trị!" />
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
        <div class="flex justify-between">
            <Button
                @click="addInput"
                class="button2 flex justify-center items-center h-10 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
            >
                <img src="/icons/plus-black.svg" alt="add" class="pr-2 w-6" />
                Thêm câu hỏi
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
        <div class="bg-white pt-4 rounded">
            <div class="flex justify-between items-center mb-4">
                <p class="text-lg font-semibold">Data</p>
                <button
                    v-if="dataQA.length > 0"
                    @click="clearAll"
                    class="button2 flex justify-center items-center h-8 px-4 py-2 border-[1px] border-slate-500 rounded text-black text-sm font-medium shadow-lg hover:bg-slate-200 hover:shadow-tk-btn transition-all duration-300"
                >
                    <img src="/icons/icon-delete-black.svg" alt="delete all" class="pr-2" />
                    Xóa tất cả
                </button>
            </div>
            <Skeleton :loading="isLoadingData" :active="true" :paragraph="{ rows: 4 }">
                <div
                    class="h-[218px] overflow-y-auto px-2 py-2 border-[1px] border-slate-400 rounded"
                >
                    <div v-if="dataQA.length === 0" class="flex justify-center items-center">
                        <img src="/images/img-noItem.png" alt="no item" class="w-40" />
                    </div>
                    <div
                        v-else
                        v-for="(item, index) in dataQA"
                        :key="index"
                        class="flex justify-between items-center bg-slate-300 p-2 rounded mb-2"
                    >
                        <div class="flex items-center space-x-2 text-ellipsis overflow-hidden">
                            <p class="border-r-2 border-black pr-2">00{{ index + 1 }}</p>
                            <div>
                                <Tooltip color="#ccc" placement="rightBottom" width="900px">
                                    <template #title>
                                        <span class="text-xs text-black whitespace-pre-wrap">
                                            {{ item.description }}</span
                                        >
                                    </template>
                                    <div class="max-w-[484px] text-nowrap flex">
                                        <span class="font-semibold text-nowrap mr-1">Câu hỏi:</span>
                                        <p class="text-ellipsis overflow-hidden">
                                            {{ item.description }}
                                        </p>
                                    </div>
                                </Tooltip>
                            </div>
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

<style>
.file-data {
    /* max-width: 600px; */
    margin: auto;
}

textarea {
    margin-bottom: 10px;
}
.shadow-tk-btn {
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
