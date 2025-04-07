<script setup lang="ts">
import type { School } from '@/interfaceConfig'
import { useAuthStore } from '@/stores/auth'
import { alertNotification } from '@/utils/notification'
import axios from 'axios'
import { onMounted, ref } from 'vue'

const auth = useAuthStore()
const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL

const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const isEditData = ref<boolean>(true)
const fileAvt = ref<File | null>(null)
const fileInput = ref<HTMLDivElement | null>(null)
const previewImage = ref<string>('')
const idLoadingUpdate = ref<boolean>(false)

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

// dataSchool.value = {
//     id: 1,
//     name: 'Trường Đại học Sư phạm Kỹ thuật - Đại học Đà Nẵng',
//     code: 'DSK',
//     phone: '0477342564',
//     email: 'dhspktdn@ute.udn.vn',
//     website: 'https://ute.udn.vn/default.aspx',
//     address: '48 Cao Thắng - Hải Châu - Đà Nẵng',
//     avatar: '/images/logo-truong-250.png',
//     createdAt: '09/09/2002',
//     createdBy: 'Admin',
//     status: 'Active'
// }

onMounted(() => {
    fetchDataSchool()
})

const fetchDataSchool = async () => {
    try {
        const response = await axios.get(`${VITE_API_URL}/school/${auth.payload?.schoolID}`)
        if (response.status === 200) {
            dataSchool.value = response.data

            previewImage.value = response.data.avatarUrl || '/images/logo-truong-250.png'
        }
    } catch (error) {
        console.log('error', error)
    }
}

const handleEditSchool = () => {
    console.log('Edit')
    isEditData.value = false
}

const handleUpdateSchool = async () => {
    try {
        idLoadingUpdate.value = true
        const formData = new FormData()
        const data = {
            schoolName: dataSchool.value.schoolName,
            schoolCode: dataSchool.value.schoolCode,
            phone: dataSchool.value.phone,
            email: dataSchool.value.email,
            website: dataSchool.value.website,
            dateEstablished: dataSchool.value.dateEstablished,
            address: dataSchool.value.address,
            description: dataSchool.value.description
        }

        formData.append('school', JSON.stringify(data))

        if (fileAvt.value) {
            formData.append('avatar', fileAvt.value)
        }

        const res = await axios.put(`${VITE_API_URL}/school/${auth.payload?.schoolID}`, formData)
        if (res.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Cập nhật thành công thông tin trường <span class="font-semibold">${dataSchool.value.schoolName}</span></p>`,
                true
            )
            fetchDataSchool()
            isEditData.value = true
        } else {
            alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
        }
    } catch (error) {
        console.log('error', error)
        alertNotification('Thất bại', 'Có lỗi xảy ra, vui lòng thử lại sau', false)
    } finally {
        idLoadingUpdate.value = false
    }
}

// Kích hoạt input file
const triggerFileInput = () => {
    if (fileInput.value) {
        fileInput.value.click()
    }
}

// Xử lý khi file được chọn
const handleFileChange = (event: any) => {
    const file = event.target.files[0]
    fileAvt.value = file
    if (file && file.type.startsWith('image/')) {
        // Tạo đường dẫn để hiển thị ảnh
        const reader = new FileReader()
        reader.onload = (e) => {
            if (e.target) {
                previewImage.value = e.target.result as string // Gán đường dẫn ảnh vào biến previewImage
            }
        }
        reader.readAsDataURL(file) // Đọc file ảnh dưới dạng DataURL
    }
}
</script>

<template>
    <div class="w-full h-full flex items-center justify-center px-28 py-8">
        <div class="school-detail flex px-14 py-10 rounded-xl">
            <div class="flex flex-col items-center mr-9">
                <!-- Hidden file input -->
                <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleFileChange"
                />

                <img
                    :src="previewImage"
                    alt="Preview"
                    class="w-[200px] h-[200px] object-cover rounded-full mb-7 max-w-[200px] max-h-[200px]"
                />

                <button
                    :disabled="isEditData"
                    :class="`${
                        isEditData
                            ? 'opacity-25 cursor-not-allowed'
                            : 'hover:shadow-2xl hover:bg-slate-100'
                    }`"
                    class="flex items-center bg-br border-[1px] px-3 h-8 text-sm border-black w-fit rounded-[4px] overflow-hidden shadow-lg transition-all duration-300"
                    @click="triggerFileInput"
                >
                    <img
                        src="/icons/cloud-arrow-up-solid.svg"
                        alt="cloud-arrow-up-solid.svg"
                        class="w-4 mr-2"
                    />
                    Tải ảnh lên
                </button>
            </div>

            <div class="w-full">
                <div class="flex justify-between items-center mb-6">
                    <h1 class="font-semibold uppercase">Thông tin chung</h1>
                </div>
                <div class="w-[640px]">
                    <div class="flex w-full gap-4">
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Tên trường:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                                v-model="dataSchool.schoolName"
                            />
                        </div>
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Mã trường:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                                v-model="dataSchool.schoolCode"
                            />
                        </div>
                    </div>
                    <div class="flex w-full gap-4">
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Số điện thoại:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                                v-model="dataSchool.phone"
                            />
                        </div>
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Email:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                                v-model="dataSchool.email"
                            />
                        </div>
                    </div>
                    <div class="flex w-full gap-4">
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Website:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] w-full border-slate-500 py-2 px-3 shadow-md rounded-md"
                                v-model="dataSchool.website"
                            />
                        </div>
                        <div class="flex flex-col w-1/2 mb-4">
                            <label class="font-medium ml-1" for="">Ngày thành lập:</label>
                            <input
                                type="text"
                                :disabled="isEditData"
                                class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                                v-model="dataSchool.dateEstablished"
                            />
                        </div>
                    </div>
                    <div class="flex flex-col mb-4">
                        <label class="font-medium ml-1" for="">Địa chỉ:</label>
                        <input
                            :disabled="isEditData"
                            type="text"
                            class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                            v-model="dataSchool.address"
                        />
                    </div>
                    <div class="flex flex-col mb-4">
                        <label class="font-medium ml-1" for="">Mô tả:</label>
                        <textarea
                            :disabled="isEditData"
                            type="text"
                            class="border-[1px] border-slate-500 py-2 px-3 shadow-md rounded-md w-full"
                            v-model="dataSchool.description"
                        />
                    </div>
                </div>

                <div class="flex w-full justify-end mt-8">
                    <button
                        @click="handleEditSchool"
                        :disabled="!isEditData"
                        :class="`${
                            !isEditData
                                ? 'opacity-35 cursor-not-allowed'
                                : 'hover:shadow-2xl hover:bg-slate-100'
                        }`"
                        class="flex items-center border-[1px] mr-3 px-3 h-10 border-black w-fit rounded-[4px] overflow-hidden shadow-lg transition-all duration-300"
                    >
                        <img
                            src="/icons/pen-to-square-solid.svg"
                            alt="floppy-disk-solid.svg"
                            class="w-4 mr-2"
                        />
                        Chỉnh sửa
                    </button>
                    <button
                        :disabled="isEditData"
                        @click="handleUpdateSchool"
                        :class="`${
                            isEditData
                                ? 'opacity-35 cursor-not-allowed'
                                : 'hover:shadow-2xl hover:bg-slate-100'
                        }`"
                        class="flex items-center bg-br border-[1px] px-3 h-10 border-black w-fit rounded-[4px] overflow-hidden shadow-lg transition-all duration-300"
                    >
                        <img
                            src="/icons/floppy-disk-solid.svg"
                            alt="pen-to-square-solid.svg"
                            class="w-4 mr-2"
                        />
                        Cập nhật
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.school-detail {
    box-shadow: rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px;
}
</style>
