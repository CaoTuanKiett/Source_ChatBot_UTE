<script setup lang="ts">
import type { File } from '@/interfaceConfig'
import { alertNotification } from '@/utils/notification'
import { Button, Empty, Input, Modal, Textarea, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { defineProps, onMounted, reactive, ref } from 'vue'

const props = defineProps({
    listFile: Array as () => File[],
    folder: Object,
    handleOpenModal: Function,
    fetchListFoldersFiles: Function,
    handleUpdateTabActiveKey: Function
})

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const folderDetail = reactive({
    idFolder: '',
    nameFolder: '',
    description: '',
    createdAt: '',
    createdBy: '',
    listFile: []
})

const isLoadingUpdateFolder = ref<boolean>(false)
const isLoadingDeleteFolder = ref<boolean>(false)
const isLoadingDeleteFile = ref<boolean>(false)

onMounted(() => {
    console.log('mounted TabFolder')

    if (props.folder) {
        folderDetail.idFolder = props.folder.idFolder
        folderDetail.nameFolder = props.folder.folderName
        folderDetail.description = props.folder.description
        folderDetail.createdAt = props.folder.createdAt
        folderDetail.createdBy = props.folder.createdBy
        folderDetail.listFile = props.folder.documents
    }
})

const onSearch = (searchValue: string) => {
    console.log('use value', searchValue)
    // console.log('or use this.value', value.value)
}

const showDeleteConfirm = async (id: number) => {
    isLoadingDeleteFile.value = true
    Modal.confirm({
        title: 'Xác nhận xóa',
        content: 'Bạn có chắc chắn muốn xóa file này không?',
        okText: 'Xóa',
        okType: 'danger',
        cancelText: 'No',
        async onOk() {
            console.log('OK delete', id)
            try {
                const res = await axios.delete(`${VITE_API_URL}/${VITE_API_VERSION}/document/${id}`)
                if (res.status === 200) {
                    alertNotification(
                        'Thành công',
                        `<p>Xóa thành công file <span class="font-semibold">${res.data.documentId}</span></p>`,
                        true
                    )
                } else {
                    alertNotification(
                        'Thất bại',
                        `<p>Xóa file <span class="font-semibold">${res.data.documentId}</span> không thành công</p>`,
                        false
                    )
                }
            } catch (error) {
                console.log('error', error)
            } finally {
                isLoadingDeleteFile.value = false
            }
        },
        onCancel() {
            console.log('Cancel')
        }
    })
}

const handleOpenModal = (file: File, isEdit: boolean) => {
    props.handleOpenModal && props.handleOpenModal(file, isEdit)
}

const getFileIcon = (fileType: string) => {
    const tpye = convertDocumentType(fileType)
    const icons: { [key: string]: string } = {
        docx: '/icons/file-word-regular.svg',
        // text: 'text/plain',
        pdf: '/icons/file-pdf-regular.svg',
        csv: '/icons/file-csv-solid.svg',
        excel: '/icons/file-excel-regular.svg'
    }

    return icons[tpye] || '/icons/file-default.svg'
}

const handleUpdateFolder = async () => {
    isLoadingUpdateFolder.value = true
    try {
        const data = {
            folderName: folderDetail.nameFolder,
            description: folderDetail.description
        }
        const response = await axios.put(
            `${VITE_API_URL}/${VITE_API_VERSION}/folder/${folderDetail.idFolder}`,
            data
        )

        if (response.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Cập nhật thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                true
            )
        } else {
            alertNotification(
                'Thành công',
                `<p>Cập nhật thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                true
            )
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingUpdateFolder.value = false
    }
}

const handleDeleteFolder = async () => {
    isLoadingDeleteFolder.value = true
    Modal.confirm({
        title: 'Xác nhận xóa',
        content: 'Bạn có chắc chắn muốn xóa folder này không?',
        okText: 'Xóa',
        okType: 'danger',
        cancelText: 'Hủy',
        async onOk() {
            try {
                const res = await axios.delete(
                    `${VITE_API_URL}/${VITE_API_VERSION}/folder/${folderDetail.idFolder}`
                )
                if (res.status === 200) {
                    props.fetchListFoldersFiles && props.fetchListFoldersFiles()
                    props.handleUpdateTabActiveKey && props.handleUpdateTabActiveKey(1)
                    alertNotification(
                        'Thành công',
                        `<p>Xóa thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                        true
                    )
                } else {
                    console.log('res', res)

                    alertNotification(
                        'Thất bại',
                        `<p>Xóa không thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                        false
                    )
                }
            } catch (error: any) {
                alertNotification('Thất bại', `<p>${error?.response?.data?.detail}</p>`, false)

                console.log('error', error)
            } finally {
                isLoadingDeleteFolder.value = false
            }
        },
        onCancel() {
            console.log('Cancel')
            isLoadingDeleteFolder.value = false
        }
    })
}

const convertDocumentType = (type: string) => {
    switch (type) {
        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return 'docx'
        case 'text/plain':
            return 'text'
        case 'application/pdf':
            return 'pdf'
        case 'text/csv':
            return 'csv'
        case 'application/vnd.ms-excel':
            return 'excel'
        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            return 'excel'
        default:
            return 'default'
    }
}
</script>

<template>
    <div class="h-full w-full">
        <div class="h-1/6 flex justify-between">
            <div class="flex">
                <div class="flex flex-col mr-8">
                    <label for="name" class="pb-2 font-medium">Tên Folder:</label>
                    <Input
                        v-model:value="folderDetail.nameFolder"
                        placeholder="Tên Folder"
                        id="name"
                        class="h-10 w-80"
                    >
                        <template #prefix>
                            <img
                                src="/icons/folder-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[14px] mr-2"
                            />
                        </template>
                    </Input>
                </div>
                <div class="flex flex-col">
                    <label for="name" class="pb-2 font-medium">Mô tả:</label>
                    <Textarea
                        v-model:value="folderDetail.description"
                        placeholder="Mô tả"
                        id="name"
                        :rows="2"
                        class="w-[500px]"
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
            <div class="flex flex-col items-end">
                <Button
                    :loading="isLoadingUpdateFolder"
                    @click="handleUpdateFolder"
                    class="flex items-center border-[1px] cursor-pointer px-3 mb-2 h-10 border-black w-fit rounded-[4px] overflow-hidden shadow-lg hover:shadow-2xl hover:bg-slate-100 transition-all duration-300"
                >
                    <img
                        src="/icons/floppy-disk-solid.svg"
                        alt="floppy-disk-solid.svg"
                        class="w-4 mr-2"
                    />
                    Cập nhật
                </Button>
                <Button
                    :loading="isLoadingDeleteFolder"
                    @click="handleDeleteFolder"
                    class="flex items-center border-[1px] cursor-pointer px-3 h-10 border-black w-fit rounded-[4px] overflow-hidden shadow-lg hover:shadow-2xl hover:bg-slate-100 transition-all duration-300"
                >
                    <img
                        src="/icons/trash-solid.svg"
                        alt="floppy-disk-solid.svg"
                        class="w-4 mr-2"
                    />
                    Xóa
                </Button>
            </div>
        </div>
        <div class="h-4/5 w-full overflow-x-auto mt-3">
            <div
                v-for="file in props.listFile"
                :key="file.idDocument"
                class="relative border-2 h-20 px-6 flex items-center mt-3 mr-5 shadow-lg rounded-lg overflow-y-auto"
            >
                <div>
                    <img
                        :src="getFileIcon(file.documentType)"
                        :alt="file.documentType"
                        class="w-8"
                    />
                </div>
                <div class="flex ml-6 items-end">
                    <div class="pr-12 w-[400px]">
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">{{ file.documentName }}</span>
                            </template>
                            <h1 class="truncate mb-1">
                                <span class="font-medium">Tên file: </span>{{ file.documentName }}
                            </h1>
                        </Tooltip>

                        <p class="truncate">
                            <span class="font-medium">Mô tả: </span>{{ file.description }}
                        </p>
                    </div>
                    <div class="pr-12 w-[250px]">
                        <p class="truncate mb-1">
                            <span class="font-medium">Loại file: </span
                            >{{ convertDocumentType(file.documentType) }}
                        </p>
                        <p class="truncate">
                            <span class="font-medium">Thời gian: </span>{{ file.createdTime }}
                        </p>
                    </div>
                    <div class="pr-12 w-[200px]">
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">{{ file.createdBy }}</span>
                            </template>
                            <p class="truncate">
                                <span class="font-medium">Tạo bởi: </span>{{ file.createdBy }}
                            </p>
                        </Tooltip>
                    </div>
                </div>
                <div class="absolute right-4 top-3 flex">
                    <Button
                        class="flex items-center mr-3 hover:opacity-60"
                        @click="handleOpenModal(file, true)"
                        ><img
                            src="/icons/pen-to-square-solid.svg"
                            class="w-4"
                            alt="pen-to-square-solid.svg"
                    /></Button>
                    <Button
                        class="flex items-center hover:opacity-60"
                        @click="showDeleteConfirm(file.idDocument)"
                        ><img src="/icons/trash-solid.svg" class="w-4" alt="trash-solid.svg"
                    /></Button>
                </div>
            </div>
            <Empty v-if="props.listFile?.length === 0" class="mt-16" />
        </div>
    </div>
</template>

<style></style>
