<script setup lang="ts">
import type { File, Folder, FoldersFiles } from '@/interfaceConfig'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Dropdown, Menu, MenuItem, Skeleton, TabPane, Tabs } from 'ant-design-vue'
import { onMounted, reactive, ref, watch } from 'vue'

import ModalDocument from '@/components/document/ModalDocument.vue'
import TabFolder from '@/components/document/TabFolder.vue'
import axios from 'axios'

const listFolder = ref<Folder[]>([])
const listFile = ref<File[]>([])
const tabActiveKey = ref<number>(1)
const openModal = ref<boolean>(false)
const isCreateFolder = ref<boolean>(false)
const isCreateFile = ref<boolean>(false)
const isLoadingData = ref<boolean>(false)
const scrollContainer = ref<HTMLDivElement | null>(null)

const activeScroll = ref(false)
const listFoldersFiles = ref<FoldersFiles[]>([])
const folderIdNew = ref<number>(0)

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const fileDetail = reactive<File>({
    idDocument: 0,
    documentName: '',
    description: '',
    documentType: '',
    dataType: 0,
    folderId: 0,
    pineconeID: '',
    createdTime: '',
    createdBy: ''
})

onMounted(async () => {
    console.log('mounted')
    await fetchListFoldersFiles()
})

watch(tabActiveKey, (newValue) => {
    console.log('tabActiveKey', newValue)
})

const searchValue = ref<string>('')
const onSearch = async () => {
    if (searchValue.value) {
        try {
            const response = await axios.get(
                `${VITE_API_URL}/search/folders/documents/${searchValue.value}`
            )

            if (response.status === 200) {
                listFoldersFiles.value = response.data
            }
        } catch (error) {
            console.error(error)
        }
    } else {
        await fetchListFoldersFiles()
    }
}

const handleResetSearch = () => {
    searchValue.value = ''
    fetchListFoldersFiles()
}

const handleOpenModal = (
    file: File | null,
    openValue: boolean,
    isCreateFolderValue: boolean = false,
    isCreateFileValue: boolean = false
) => {
    if (file) {
        fileDetail.idDocument = file.idDocument
        fileDetail.documentName = file.documentName
        fileDetail.description = file.description
        fileDetail.documentType = file.documentType
        fileDetail.dataType = file.dataType
        fileDetail.folderId = file.folderId
        fileDetail.pineconeID = file.pineconeID
        fileDetail.createdTime = file.createdTime
        fileDetail.createdBy = file.createdBy
    }

    if (isCreateFileValue) {
        console.log('tabActiveKey.value', tabActiveKey.value)
        console.log('listFoldersFiles.value', listFoldersFiles.value[tabActiveKey.value])

        const folderId = listFoldersFiles.value[tabActiveKey.value - 1]?.idFolder
        fileDetail.folderId = folderId
    }
    console.log('fileDetail', fileDetail)

    isCreateFolder.value = isCreateFolderValue
    isCreateFile.value = isCreateFileValue

    openModal.value = openValue
}

const handleOk = (openValue: boolean) => {
    openModal.value = openValue
}

const fetchListFoldersFiles = async () => {
    isLoadingData.value = true
    try {
        const response = await axios.get(`${VITE_API_URL}/folders_documents`)

        if (response.status === 200) {
            listFoldersFiles.value = response.data
        }
    } catch (error) {
        console.error(error)
    } finally {
        isLoadingData.value = false
    }
}

const handleScroll = () => {
    if (scrollContainer.value) {
        // console.log('scrollContainer.value.scrollTop', scrollContainer.value.scrollTop)
        activeScroll.value = scrollContainer.value.scrollTop > 50
    }
}

const handleUpdateTabActiveKey = (key: number) => {
    tabActiveKey.value = key
}

const handleUpdateFolderIdNew = (id: number) => {
    folderIdNew.value = id
}
</script>

<template>
    <div class="document relative w-full overflow-x-auto px-6">
        <div
            :class="`flex flex-col bg-white right-0 w-full z-10 p-8 px-8 ${
                activeScroll ? 'activeScroll' : ''
            }`"
        >
            <div class="flex justify-between items-center">
                <Dropdown>
                    <div
                        class="border-[1px] py-2 px-3 border-black w-fit rounded-[4px] overflow-hidden shadow-lg hover:shadow-2xl hover:bg-slate-100 transition-all duration-300"
                    >
                        <PlusOutlined />
                        <span class="pl-2 text-base">Thêm mới</span>
                    </div>
                    <template #overlay>
                        <Menu class="p-2">
                            <MenuItem class="p-2" @click="handleOpenModal(null, true, true)"
                                >Thêm mới thư mục</MenuItem
                            >
                            <MenuItem class="p-2" @click="handleOpenModal(null, true, false, true)"
                                >Thêm mới tài liệu</MenuItem
                            >
                        </Menu>
                    </template>
                </Dropdown>

                <div class="relative flex items-center">
                    <button class="absolute left-4" @click="onSearch()">
                        <img
                            src="/icons/magnifying-glass-solid.svg"
                            alt="magnifying-glass-solid.svg"
                            class="w-5 h-5"
                        />
                    </button>
                    <input
                        class="input-search w-96 rounded-full px-11 py-3 border-2 border-gray-200 border-transparent focus:outline-none focus:border-blue-500 placeholder-gray-400 transition-all duration-300 shadow-lg"
                        placeholder="Search..."
                        required="true"
                        type="text"
                        v-model="searchValue"
                        @keydown.enter="onSearch()"
                    />
                    <button @click="handleResetSearch" type="reset" class="absolute right-3 p-1">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="w-5 h-5 text-gray-700"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M6 18L18 6M6 6l12 12"
                            ></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <Skeleton :loading="isLoadingData" :active="true">
            <Tabs
                v-model:activeKey="tabActiveKey"
                tab-position="left"
                class="h-4/5 w-full pr-4"
                ref="scrollContainer"
            >
                <TabPane
                    v-for="folder in listFoldersFiles"
                    :key="folder.idFolder"
                    :tab="folder.folderName"
                    class="h-[562px]"
                >
                    <TabFolder
                        :listFile="folder.documents"
                        :folder="folder"
                        :handleOpenModal="handleOpenModal"
                        :fetchListFoldersFiles="fetchListFoldersFiles"
                        :handleUpdateTabActiveKey="handleUpdateTabActiveKey"
                    />
                </TabPane>
            </Tabs>
        </Skeleton>
    </div>
    <div v-if="openModal">
        <ModalDocument
            :handleOk="handleOk"
            :openModal="openModal"
            :fileDetail="fileDetail"
            :isCreateFolder="isCreateFolder"
            :isCreateFile="isCreateFile"
            :fetchListFoldersFiles="fetchListFoldersFiles"
        />
    </div>
</template>

<style>
.activeScroll {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.document .input-search {
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em,
        rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset;
}

.document .ant-menu-submenu-selected {
    span {
        color: black !important;
        /* background-color: red !important; */
    }
}

.document .ant-menu-submenu-selected::after {
    border-bottom-color: black !important;
    border-bottom-width: none !important;
}

.document .ant-menu-submenu-active::after {
    border: none !important;
    border-bottom-width: none !important;
}

.document .ant-tabs-nav {
    max-width: 160px !important;
}

.document .ant-tabs-nav .ant-tabs-tab {
    padding-right: 10px !important;
}

.document .ant-tabs-nav .ant-tabs-tab .ant-tabs-tab-btn {
    text-overflow: ellipsis;
    overflow: hidden;
}
</style>
