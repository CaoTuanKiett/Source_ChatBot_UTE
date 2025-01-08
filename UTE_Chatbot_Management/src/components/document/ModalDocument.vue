<script setup lang="ts">
import ELValidate from '@/components/common/ELValidate.vue'
import type { File, FolderGet } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'
import type { UploadProps } from 'ant-design-vue'
import { Button, Input, Modal, Select, Textarea, Tooltip } from 'ant-design-vue'
import axios from 'axios'
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import ConfigData from '../chatbot/ConfigData.vue'

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const VITE_API_URL = import.meta.env.VITE_API_URL

const props = defineProps({
    handleOk: Function,
    openModal: Boolean,
    fileDetail: Object,
    isCreateFolder: Boolean,
    isCreateFile: Boolean,
    fetchListFoldersFiles: Function
})

const fileList = ref<UploadProps['fileList']>([])
const folderSelected = ref<number>(0)
const isOptionCreateFolderWithFile = ref<boolean>(false)
const isOptionCreateFolder = ref<boolean>(props?.isCreateFolder)
const isOptionCreateFile = ref<boolean>(props?.isCreateFile)
const isViewDetailFile = ref<boolean>(
    props.fileDetail !== null && !isOptionCreateFile.value && !isOptionCreateFolder.value
)
const dataFolder = ref<FolderGet[]>([])
const isLoadingFolder = ref<boolean>(false)
const isValidateFolderName = ref<boolean>(false)
const isLoadingCreateFile = ref<boolean>(false)
const configDataRef = ref<InstanceType<typeof ConfigData> | null>(null)

const listFileDetail = reactive<File>({
    idDocument: 0,
    documentName: '',
    documentType: '',
    dataType: 0,
    description: '',
    pineconeID: '',
    folderId: 0,
    createdTime: '',
    createdBy: ''
})

onMounted(async () => {
    // console.log('props.isCreateFile', props.isCreateFile)
    // console.log('isOptionCreateFolder', isOptionCreateFolder.value)
    console.log('props.fileDetail', props.fileDetail)
    // console.log('isViewDetailFile', isViewDetailFile.value)

    if (props.fileDetail && isViewDetailFile.value) {
        listFileDetail.idDocument = props.fileDetail.idDocument
        listFileDetail.documentName = props.fileDetail.documentName
        listFileDetail.description = props.fileDetail.description
        listFileDetail.documentType = props.fileDetail.documentType
        listFileDetail.createdTime = props.fileDetail.createdTime
        listFileDetail.createdBy = props.fileDetail.createdBy
        listFileDetail.folderId = props.fileDetail.folderId

        folderSelected.value = props.fileDetail.folderId || 1
    }

    if (props.fileDetail && isOptionCreateFile.value) {
        folderSelected.value = props.fileDetail.folderId
    }

    await fetchDataFolders()
})

onUnmounted(() => {
    resetForm()
    console.log('unmounted', listFileDetail)
})

const openModalLocal = computed({
    get: () => props.openModal,
    set: (value: boolean) => {
        props.handleOk && props.handleOk(value)
    }
})

const handleOkLocal = async () => {
    if (isOptionCreateFolder.value) {
        await handleCreateFolder()
        // } else if (isOptionCreateFile.value) {
        //     await handleCreateFile()
    } else if (isViewDetailFile.value) {
        await handleUpdateFile()
    }

    if (!isValidateFolderName.value) {
        handleCancel()
    }
}

const folderDetail = reactive({
    nameFolder: '',
    description: '',
    createdAt: '',
    createdBy: '',
    listFile: []
})

const fetchDataFolders = async () => {
    try {
        const responseFolders = await axios.get(`${VITE_API_URL}/${VITE_API_VERSION}/folders`)

        if (responseFolders.status === 200) {
            dataFolder.value = responseFolders.data
        }
    } catch (error) {
        console.log('error', error)
    }
}

const focus = () => {
    console.log('focus')
}

const handleChange = (value: number) => {
    console.log(`selected ${value}`)
    // if (configDataRef.value) {
    //     configDataRef.value.resetData()
    // }
}

const handleOptionCreateFolder = (value: boolean) => {
    isOptionCreateFolderWithFile.value = value
}

const handleCreateFolderWithFile = async () => {
    isLoadingFolder.value = true
    try {
        if (folderDetail.nameFolder.trim() === '') {
            isValidateFolderName.value = true
            return
        } else {
            isValidateFolderName.value = false
        }

        const data = {
            folderName: folderDetail.nameFolder,
            description: folderDetail.description,
            createdBy: auth.payload?.username || 'Admin'
        }

        const res = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/folder`, data)
        if (res.status === 200) {
            console.log('Create Folder', res)
            fetchDataFolders()
            alertNotification(
                'Thành công',
                `<p>Tạo thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                true
            )

            folderSelected.value = res.data.idFolder
            folderDetail.nameFolder = ''
            folderDetail.description = ''
        } else {
            alertNotification('Thất bại', 'Tạo folder thất bại', false)
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingFolder.value = false
    }

    handleOptionCreateFolder(false)
}

// const handleCreateFile = async () => {
//     isLoadingCreateFile.value = true
//     const formData = new FormData()

//     fileList.value?.forEach((file) => {
//         formData.append('files', file)
//     })
//     formData.append('folderId', folderSelected.value.toString())
//     formData.append('description', 'File đã được xử lý và lưu trữ thành công.')
//     formData.append('createdBy', auth.payload?.username || 'Admin')
//     formData.append('dataType', TypeData.DataImportFile.toString())
//     formData.append('typeData', TypeData.DataImportFile.toString())

//     try {
//         const response = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/documents`, formData)
//         if (response.status === 200) {
//             fileList.value = []
//             alertNotification(
//                 'Thành công',
//                 `<p>Tạo thành công file <span class="font-semibold">${listFileDetail.documentName}</span></p>`,
//                 true
//             )
//         } else {
//             alertNotification('Thất bại', 'Tạo file thất bại', false)
//         }
//     } catch (error) {
//         console.log('error', error)
//     } finally {
//         isLoadingCreateFile.value = false
//     }
// }

const handleCreateFolder = async () => {
    console.log('folderDetail', folderDetail)
    isLoadingFolder.value = true

    try {
        if (folderDetail.nameFolder.trim() === '') {
            isValidateFolderName.value = true
            return
        } else {
            isValidateFolderName.value = false
        }

        const data = {
            folderName: folderDetail.nameFolder,
            description: folderDetail.description,
            createdBy: auth.payload?.username || 'Admin'
        }

        const res = await axios.post(`${VITE_API_URL}/${VITE_API_VERSION}/folder`, data)
        if (res.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Tạo thành công folder <span class="font-semibold">${folderDetail.nameFolder}</span></p>`,
                true
            )

            folderDetail.nameFolder = ''
            folderDetail.description = ''
        } else {
            alertNotification('Thất bại', 'Tạo folder thất bại', false)
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingFolder.value = false
    }
}

const handleUpdateFile = () => {
    console.log('listFileDetail', listFileDetail)

    console.log('cập nhật file')
}

const handleCancel = async () => {
    resetForm()
    console.log('cancel')

    if (props.fetchListFoldersFiles) {
        console.log('fetchListFoldersFiles')

        await props.fetchListFoldersFiles()
    }
    props.handleOk && props.handleOk(false)
}

async function downloadFile(idDocument: number, documentName: string) {
    try {
        const response = await axios.get(
            `${VITE_API_URL}/${VITE_API_VERSION}/download/document/${idDocument}`,
            {
                responseType: 'blob' // Để nhận dữ liệu nhị phân
            }
        )

        // Tạo đối tượng URL từ dữ liệu nhị phân (file)
        const fileURL = window.URL.createObjectURL(new Blob([response.data]))

        // Tạo link để tải file về
        const link = document.createElement('a')
        link.href = fileURL
        link.setAttribute('download', documentName) // Tên file có thể thay đổi
        document.body.appendChild(link)
        link.click() // Bắt đầu tải file
    } catch (error) {
        console.error('Error downloading file:', error)
    }
}

const resetForm = () => {
    folderDetail.nameFolder = ''
    folderDetail.description = ''
    folderDetail.createdAt = ''
    folderDetail.createdBy = ''
    folderDetail.listFile = []

    listFileDetail.idDocument = 0
    listFileDetail.documentName = ''
    listFileDetail.description = ''
    listFileDetail.documentType = ''
    listFileDetail.createdTime = ''
    listFileDetail.createdBy = ''
    listFileDetail.folderId = 0
}
</script>

<template>
    <Modal
        v-model:open="openModalLocal"
        :title="
            isOptionCreateFolder
                ? 'Tạo mới Folder'
                : isOptionCreateFile
                ? 'Thêm mới dữ liệu'
                : 'Chi tiết File'
        "
        width="900px"
        height="500"
        class="modal-document"
        :inert="!openModalLocal"
        :maskClosable="false"
    >
        <!-- :class="isOptionCreateFile ? 'mt-[-84px]' : ''" -->
        <template #footer>
            <Button key="back" @click="handleCancel">Hủy</Button>
            <Button
                key="submit"
                type="primary"
                :disabled="isOptionCreateFolderWithFile"
                :loading="isLoadingCreateFile || isLoadingFolder"
                @click="handleOkLocal()"
            >
                {{ isViewDetailFile ? 'Cập nhật' : 'Lưu' }}
            </Button>
        </template>
        <div
            v-if="
                isOptionCreateFolder ||
                (isOptionCreateFolderWithFile && isOptionCreateFile) ||
                props.fileDetail === null
            "
            class="p-3 mb-5"
        >
            <div class="flex justify-between">
                <h1 class="font-semibold mb-1">Tạo mới thư mục:</h1>
                <div class="flex">
                    <button
                        v-if="!isOptionCreateFolder"
                        class="flex items-center font-semibold hover:opacity-60 mr-2 hover:shadow-lg transition-all duration-300 border-[1px] border-black px-2 h-8 rounded-[4px] cursor-pointer"
                        @click="handleOptionCreateFolder(false)"
                    >
                        <img
                            src="/icons/xmark-solid.svg"
                            alt="xmark-solid.svg"
                            class="w-4 mr-2"
                        />Trở lại
                    </button>
                    <button
                        v-if="!isOptionCreateFolder"
                        class="flex items-center font-semibold hover:opacity-60 hover:shadow-lg transition-all duration-300 border-[1px] border-black px-2 h-8 rounded-[4px] cursor-pointer"
                        @click="handleCreateFolderWithFile()"
                    >
                        <img
                            src="/icons/xmark-solid.svg"
                            alt="xmark-solid.svg"
                            class="w-4 mr-2"
                        />Lưu
                    </button>
                </div>
            </div>
            <div class="mb-2">
                <label for="name" class="ml-1">Tên Folder:</label>
                <Input
                    v-model:value="folderDetail.nameFolder"
                    placeholder="Tên Folder"
                    id="name"
                    class="h-10"
                    @blur="isValidateFolderName = folderDetail.nameFolder.trim() === ''"
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
                    content="Tên folder không được để trống"
                />
            </div>
            <div>
                <label for="description" class="ml-1">Mô tả:</label>
                <Input
                    v-model:value="folderDetail.description"
                    placeholder="Mô tả"
                    id="description"
                    class="h-10"
                >
                    <template #prefix>
                        <img
                            src="/icons/scroll-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-4 mr-2"
                        />
                    </template>
                </Input>
            </div>
        </div>
        <div v-else class="flex flex-col p-3">
            <label for="selectFolder" class="ml-1 font-semibold mb-2">
                {{ isOptionCreateFile ? 'Chọn thư mục:' : 'Thư mục' }}
            </label>
            <div class="flex w-full justify-between" :class="isViewDetailFile ? '' : 'px-5'">
                <Select
                    id="selectFolder"
                    ref="select"
                    v-model:value="folderSelected"
                    :options="
                        dataFolder.map((item) => ({ value: item.idFolder, label: item.folderName }))
                    "
                    @focus="focus"
                    @change="handleChange(folderSelected)"
                    class="shadow-md"
                    :class="isViewDetailFile ? 'w-full' : 'w-[660px]'"
                ></Select>
                <div
                    v-if="!isViewDetailFile"
                    @click="handleOptionCreateFolder(true)"
                    class="flex items-center border-[1px] cursor-pointer px-2 h-8 border-black w-fit rounded-[4px] overflow-hidden shadow-lg hover:shadow-2xl hover:bg-slate-100 transition-all duration-300"
                >
                    <img src="/icons/plus-solid.svg" alt="floppy-disk-solid.svg" class="w-4 mr-2" />
                    Thêm mới
                </div>
            </div>
        </div>
        <div
            v-if="(isOptionCreateFile && !isOptionCreateFolderWithFile) || isViewDetailFile"
            class="p-3"
        >
            <div v-if="!isOptionCreateFile">
                <h1 class="font-semibold mb-1">Tài liệu</h1>
                <div class="mb-2">
                    <label for="nameFile" class="ml-1">Tên tài liệu:</label>
                    <div class="flex items-center">
                        <Input
                            v-model:value="listFileDetail.documentName"
                            placeholder="Tên File"
                            id="nameFile"
                            class="h-10 shadow-sm"
                        >
                            <template #prefix>
                                <img
                                    src="/icons/folder-solid.svg"
                                    alt="envelope-regular.svg"
                                    class="w-[14px] mr-2"
                                />
                            </template>
                        </Input>
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">Tải xuống</span>
                            </template>
                            <Button
                                @click="
                                    downloadFile(
                                        listFileDetail.idDocument,
                                        listFileDetail.documentName
                                    )
                                "
                                class="h-10 ml-2 shadow-sm hover:shadow-lg"
                            >
                                <img
                                    src="/icons/download-solid.svg"
                                    alt="download-solid.svg"
                                    class="w-5 h-5"
                                />
                            </Button>
                        </Tooltip>
                    </div>
                </div>
                <div class="mb-2">
                    <label for="descriptionFile" class="ml-1">Mô tả:</label>
                    <Textarea
                        v-model:value="listFileDetail.description"
                        placeholder="Mô tả File"
                        id="descriptionFile"
                        class="shadow-sm"
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

            <div v-if="!isViewDetailFile">
                <!-- <label for="uploadFile" class="ml-1">Tải File:</label>
                <div>
                    <Upload
                        id="uploadFile"
                        class="w-[400px]"
                        :file-list="fileList"
                        :before-upload="beforeUpload"
                        @remove="handleRemove"
                        multiple
                    >
                        <template #default>
                            <Button class="mb-3 flex items-center justify-center w-36">
                                <img
                                    src="/icons/file-arrow-up-solid.svg"
                                    alt="file-arrow-up-solid.svg"
                                    class="w-3 mr-3"
                                />
                                Tải File
                            </Button>
                        </template>
                        <template #itemRender="{ file, actions }">
                            <div
                                class="flex justify-between items-center bg-white border-[1px] py-2 px-3 rounded-md"
                            >
                                <p
                                    :style="file.status === 'error' ? 'color: red' : ''"
                                    class="max-w-[624px] truncate"
                                >
                                    {{ file.name }}
                                </p>
                                <div>
                                    <button @click="actions.download" class="mr-3 hover:opacity-55">
                                        <img
                                            src="/icons/file-arrow-down-solid.svg"
                                            alt="file-arrow-down-solid.svg"
                                            class="w-3"
                                        />
                                    </button>
                                    <button @click="actions.remove" class="hover:opacity-55">
                                        <img
                                            src="/icons/trash-solid.svg"
                                            alt="trash-solid.svg"
                                            class="w-3"
                                        />
                                    </button>
                                </div>
                            </div>
                        </template>
                    </Upload>
                </div> -->
                <h1 class="font-medium mb-2 ml-1">Thêm tài liệu:</h1>
                <ConfigData ref="configDataRef" :folder-id="folderSelected" />
            </div>
        </div>
    </Modal>
</template>

<style>
.modal-document .ant-upload-list-item-container {
    margin-bottom: 4px;
    border-radius: 6px;
    box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgb(209, 213, 219) 0px 0px 0px 1px inset;
}
</style>
