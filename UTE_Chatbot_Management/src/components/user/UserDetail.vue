<script setup lang="ts">
import ELValidate from '@/components/common/ELValidate.vue'
import type { Role, User } from '@/interfaceConfig'
import { alertNotification } from '@/utils/notification'
import { Button, DatePicker, Drawer, Input, Modal, Select } from 'ant-design-vue'
import axios from 'axios'
import dayjs, { Dayjs } from 'dayjs'
import { defineProps, onMounted, onUnmounted, reactive, ref, type PropType } from 'vue'

const props = defineProps({
    isCreate: Boolean,
    userDetail: Object,
    openPannel: Boolean,
    handleopenPannel: Function,
    listRole: Array as PropType<Role[]>,
    fetchDataUsers: Function,
    isView: Boolean
})

const VITE_API_VERSION = import.meta.env.VITE_API_VERSION
const baseURL = import.meta.env.VITE_API_URL
const VITE_API_URL = `${baseURL}/${VITE_API_VERSION}`

const VITE_ID_SCHOOL = import.meta.env.VITE_ID_SCHOOL
const VITE_PASSWORD_DEFAULT = import.meta.env.VITE_PASSWORD_DEFAULT

const user = reactive<User>({
    idUser: 0,
    username: '',
    avatarUrl: '/icons/cat-avatar.png',
    phone: '',
    email: '',
    birthday: '',
    gender: null,
    address: '',
    password: '',
    status: '',
    createdTime: '',
    updatedTime: '',
    createdBy: '',
    roleID: null,
    schoolID: 0
})

const dateFormat = 'DD/MM/YYYY'
const dateOfBirth = ref<Dayjs>()
const imagesNew = ref<string>('')
const imagesUpload = ref<File>()
const isLoadingUser = ref<boolean>(false)
const isLoadingResetPassword = ref<boolean>(false)

const passwordChangeDetail = reactive({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
})

// const handleDateChange = (date: string) => {
//     const dateFormat = 'DD/MM/YYYY'
//     return dayjs(date, dateFormat).format(dateFormat)
// }

// const convertRole = (roleID: number) => {
//     const role = props.listRole?.find((role) => role.idRole === roleID)
//     return role ? role.roleName : ''
// }

const localOpen = ref(props.openPannel)
const openModalChangePassword = ref(false)
const isValidatePasswordConfirm = ref(false)
const isLoadingChangePassword = ref(false)

// const dateFormatList = ['DD/MM/YYYY', 'DD/MM/YY']
// const date = ref<Dayjs>(dayjs('01/01/2015', dateFormatList[0]))
const listStatus = [
    {
        id: 1,
        name: 'Hoạt động'
    },
    {
        id: 2,
        name: 'Vô hiệu hóa'
    }
]

const listGender = [
    {
        name: 'Nam'
    },
    {
        name: 'Nữ'
    },
    {
        name: 'Khác'
    }
]

onMounted(() => {
    console.log('isView', !props.isCreate && props.isView)

    if (props.userDetail && !props.isCreate) {
        dateOfBirth.value = dayjs(props.userDetail?.birthday, dateFormat)

        user.idUser = props.userDetail?.idUser
        user.username = props.userDetail?.username
        user.avatarUrl = props.userDetail?.avatarUrl || '/icons/cat-avatar.png'
        user.phone = props.userDetail?.phone
        user.email = props.userDetail?.email
        user.gender = props.userDetail?.gender
        user.birthday = props.userDetail?.birthday
        user.address = props.userDetail?.address
        user.password = props.userDetail?.password
        user.role = props.userDetail?.role
        user.status = props.userDetail?.status
        user.createdTime = props.userDetail?.createdTime
        user.updatedTime = props.userDetail?.updatedTime
        user.createdBy = props.userDetail?.createdBy
        user.roleID = props.userDetail?.roleID
        user.schoolID = props.userDetail?.schoolID
    } else {
        dateOfBirth.value = dayjs('00/00/0000', dateFormat)
    }

    imagesNew.value = user?.avatarUrl || '/icons/cat-avatar.png'
    console.log('onMounted', user)
})

onUnmounted(() => {
    console.log('Unmounted')
    resetUser()
})

// Handle Drawer open/close changes
const afterOpenChange = (bool: boolean) => {
    console.log('afterOpenChange', bool)
}

const handleClose = () => {
    localOpen.value = false
    props.handleopenPannel && props.handleopenPannel(false)

    //Reser user
    resetUser()
}

const handleSave = async () => {
    isLoadingUser.value = true
    console.log('imagesUpload', imagesUpload.value)

    user.birthday = dateOfBirth.value?.format(dateFormat) || ''

    try {
        if (props.isCreate) {
            // Create user
            console.log('Create user')
            try {
                const formData = new FormData()

                user.password = VITE_PASSWORD_DEFAULT
                user.schoolID = VITE_ID_SCHOOL

                if (imagesUpload.value) {
                    formData.append('fileAvt', imagesUpload.value as Blob)
                }
                formData.append('user', JSON.stringify(user))

                const res = await axios.post(`${VITE_API_URL}/user`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })

                if (res.status === 200) {
                    console.log('res', res)
                    props.fetchDataUsers && props.fetchDataUsers()
                    alertNotification(
                        'Thành công',
                        `<p>Tạo thành công chatbot <span class="font-semibold">${res.data.user.username}</span></p>`,
                        true
                    )
                    handleClose()
                } else {
                    alertNotification('Thất bại', 'Tạo thất bại', false)
                }
            } catch (error) {
                alertNotification('Thất bại', 'Tạo thất bại', false)
                console.log('error', error)
            }
        } else {
            // Update user
            try {
                const formData = new FormData()
                if (imagesUpload.value) {
                    formData.append('fileAvt', imagesUpload.value as Blob)
                }
                formData.append('user', JSON.stringify(user))

                const res = await axios.put(`${VITE_API_URL}/user/${user.idUser}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })

                if (res.status === 200) {
                    props.fetchDataUsers && props.fetchDataUsers()
                    alertNotification(
                        'Thành công',
                        `<p>Cập nhật thành công chatbot <span class="font-semibold">${res.data.username}</span></p>`,
                        true
                    )
                    handleClose()
                } else {
                    alertNotification('Thất bại', 'Cập nhật thất bại', false)
                }
            } catch (error) {
                alertNotification('Thất bại', 'Cập nhật thất bại', false)
                console.log('error', error)
            }
            console.log('Update user')
        }
    } catch (error) {
        console.log('error', error)
    } finally {
        isLoadingUser.value = false
    }
}

const handleChangeImage = (event: Event) => {
    const target = event.target as HTMLInputElement
    console.log('target', target.files)

    if (target.files && target.files[0]) {
        imagesUpload.value = target.files[0]
        const file = target.files[0]
        const reader = new FileReader()
        reader.onload = (e) => {
            imagesNew.value = e.target?.result as string
        }
        reader.readAsDataURL(file)
    }
}

const handleResetPassword = async () => {
    isLoadingResetPassword.value = true
    try {
        const VITE_PASSWORD_DEFAULT = import.meta.env.VITE_PASSWORD_DEFAULT

        const res = await axios.post(`${VITE_API_URL}/user/reset-password/${user.idUser}`, {
            new_password: VITE_PASSWORD_DEFAULT
        })

        if (res.status === 200) {
            alertNotification(
                'Thành công',
                `<p>Đặt lại mật khẩu thành công chatbot <span class="font-semibold">${res.data.user.username}</span></p>`,
                true
            )
        } else {
            alertNotification('Thất bại', 'Đặt lại mật khẩu thất bại', false)
        }
    } catch (error) {
        alertNotification('Thất bại', 'Đặt lại mật khẩu thất bại', false)
        console.log('error', error)
    } finally {
        isLoadingResetPassword.value = false
    }
}

const handleOpenChangePassword = async (value: boolean) => {
    openModalChangePassword.value = value

    if (!value) {
        passwordChangeDetail.oldPassword = ''
        passwordChangeDetail.newPassword = ''
        passwordChangeDetail.confirmPassword = ''
    }
}

const handleChangePassword = async () => {
    // console.log('passwordChangeDetail', passwordChangeDetail)
    if (isValidatePasswordConfirm.value) {
        try {
            isLoadingChangePassword.value = true
            const res = await axios.post(`${VITE_API_URL}/user/change-password/${user.idUser}`, {
                old_password: passwordChangeDetail.oldPassword,
                new_password: passwordChangeDetail.newPassword
            })

            if (res.status === 200) {
                alertNotification(
                    'Thành công',
                    `<p>Đổi mật khẩu thành công chatbot <span class="font-semibold">${res.data.user.username}</span></p>`,
                    true
                )
                handleOpenChangePassword(false)
            } else {
                console.log('res', res.data)

                alertNotification('Thất bại', `<p>${res.data.detail}</p>`, false)
            }
        } catch (error: any) {
            alertNotification('Thất bại', `<p>${error?.response?.data?.detail}</p>`, false)
            console.log('error', error)
        } finally {
            isLoadingChangePassword.value = false
        }
    }
}

const handleCheckPasswordConfirm = () => {
    isValidatePasswordConfirm.value =
        passwordChangeDetail.newPassword.trim() === passwordChangeDetail.confirmPassword.trim() ||
        (passwordChangeDetail.newPassword.trim() === '' &&
            passwordChangeDetail.confirmPassword.trim() === '')

    console.log('isValidatePasswordConfirm', isValidatePasswordConfirm.value)
}

//reser user
const resetUser = () => {
    user.idUser = 0
    user.username = ''
    user.avatarUrl = ''
    user.phone = ''
    user.email = ''
    user.birthday = ''
    user.address = ''
    user.password = ''
    user.role = ''
    user.status = ''
    user.createdTime = ''
    user.updatedTime = ''
    user.createdBy = ''
    user.roleID = 0
    user.schoolID = 0
}
</script>

<template>
    <div>
        <Drawer
            :title="isCreate ? 'Thêm mới người dùng' : 'Chi tiết người dùng'"
            placement="right"
            v-model:open="localOpen"
            width="700"
            @afterOpenChange="afterOpenChange"
            @close="handleClose"
            :maskClosable="false"
            :footer-style="{ textAlign: 'right' }"
        >
            <div>
                <div class="flex mb-4 pl-2 relative">
                    <img
                        :src="imagesNew"
                        alt="avatar"
                        class="w-24 h-24 object-cover mr-6 rounded-lg border-[1px] border-slate-300 p-1 border-solid"
                    />
                    <div>
                        <p class="font-medium mb-3">Chọn ảnh đại diện</p>
                        <input type="file" @change="handleChangeImage" accept="image/*" />
                    </div>

                    <Button
                        v-if="!props.isCreate && !props.isView"
                        :loading="isLoadingResetPassword"
                        @click="handleResetPassword"
                        class="absolute flex items-center shadow-md hover:bg-slate-100 right-4 top-0 h-8"
                    >
                        <img
                            src="/icons/clock-rotate-left-solid.svg"
                            alt="clock-rotate-left-solid.svg"
                            class="w-4 mr-2"
                        />
                        Đặt lại mật khẩu
                    </Button>
                    <Button
                        v-if="props.isView"
                        :loading="isLoadingResetPassword"
                        @click="handleOpenChangePassword(true)"
                        class="absolute flex items-center shadow-md hover:bg-slate-100 right-4 top-0 h-8"
                    >
                        <img
                            src="/icons/clock-rotate-left-solid.svg"
                            alt="clock-rotate-left-solid.svg"
                            class="w-4 mr-2"
                        />
                        Đổi mật khẩu
                    </Button>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="name" class="pb-2 font-medium">Họ và tên:</label>
                    <Input
                        v-model:value="user.username"
                        placeholder="Nhập họ và tên"
                        id="name"
                        class="h-10"
                    >
                        <template #prefix>
                            <img
                                src="/icons/user-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[14px] mr-2"
                            />
                        </template>
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="email" class="pb-2 font-medium">Email:</label>
                    <Input
                        v-model:value="user.email"
                        placeholder="Nhập email"
                        id="email"
                        class="h-10"
                        type="email"
                    >
                        <template #prefix>
                            <img
                                src="/icons/envelope-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[15px] mr-2"
                            />
                        </template>
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="phone" class="pb-2 font-medium">Số điện thoại:</label>
                    <Input
                        v-model:value="user.phone"
                        placeholder="Nhập số điện thoại"
                        id="phone"
                        class="h-10"
                        type="number"
                    >
                        <template #prefix>
                            <img
                                src="/icons/phone-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[15px] mr-2"
                            />
                        </template>
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="role" class="pb-2 font-medium">Vai trò:</label>
                    <div class="flex border-[1px] rounded-md h-10 pl-2 items-center">
                        <img
                            src="/icons/address-card-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-4 ml-[5px]"
                        />
                        <Select
                            ref="select"
                            placeholder="Chọn vai trò"
                            v-model:value="user.roleID"
                            :options="
                                listRole?.map((item) => ({
                                    value: item.idRole,
                                    label: item.roleName
                                }))
                            "
                            class="select-role w-full border-none"
                        >
                        </Select>
                    </div>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="gender" class="pb-2 font-medium">Giới tính:</label>
                    <div class="flex border-[1px] rounded-md h-10 pl-2 items-center">
                        <img
                            src="/icons/venus-mars-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-[18px] mr-2"
                        />
                        <Select
                            ref="select"
                            placeholder="Chọn giới tính"
                            v-model:value="user.gender"
                            :options="
                                listGender?.map((item) => ({
                                    value: item.name,
                                    label: item.name
                                }))
                            "
                            class="select-role w-full border-none"
                        >
                        </Select>
                    </div>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="status" class="pb-2 font-medium">Trạng thái:</label>
                    <div class="flex border-[1px] rounded-md h-10 pl-2 items-center">
                        <img
                            src="/icons/star-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-4 ml-[5px]"
                        />
                        <Select
                            ref="select"
                            placeholder="Chọn thư mục"
                            v-model:value="user.status"
                            :options="
                                listStatus.map((item) => ({
                                    value: item.id,
                                    label: item.name
                                }))
                            "
                            class="select-role w-full border-none"
                        >
                        </Select>
                    </div>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="address" class="pb-2 font-medium">Địa chỉ:</label>
                    <Input
                        v-model:value="user.address"
                        placeholder="Basic usage"
                        id="address"
                        class="h-10"
                        type="text"
                    >
                        <template #prefix>
                            <img
                                src="/icons/location-dot-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[14px] mr-2"
                            />
                        </template>
                    </Input>
                </div>

                <div class="flex flex-col mb-4">
                    <label for="dateOfBirth" class="pb-2 font-medium">Ngày Sinh</label>
                    <div class="flex border-[1px] rounded-md">
                        <img
                            src="/icons/calendar-days-solid.svg"
                            alt="envelope-regular.svg"
                            class="w-[14px] mx-2"
                        />
                        <DatePicker
                            v-model:value="dateOfBirth"
                            :format="dateFormat"
                            class="h-10 border-none w-full"
                            @change="
                                () => {
                                    console.log('dateOfBirth', dateOfBirth)
                                }
                            "
                        />
                    </div>
                </div>
            </div>
            <template #footer>
                <Button type="default" @click="handleClose" class="mr-3 h-10 font-bold">Hủy</Button>
                <Button
                    :loading="isLoadingUser"
                    type="primary"
                    @click="handleSave"
                    class="w-28 h-10 font-bold"
                    >Lưu</Button
                >
            </template>
        </Drawer>
        <Modal
            v-if="openModalChangePassword"
            v-model:open="openModalChangePassword"
            title="Đổi mật khẩu"
            width="600px"
            :mask-closable="false"
            :footer-style="{ textAlign: 'right' }"
        >
            <div class="py-3 px-5">
                <div class="flex flex-col mb-4">
                    <label for="password" class="pb-2 font-semibold">Mật khẩu cũ:</label>
                    <Input
                        v-model:value="passwordChangeDetail.oldPassword"
                        placeholder="Nhập mật khẩu cũ"
                        id="password"
                        class="h-10 shadow-md border-[1px] border-solid border-slate-300"
                        type="password"
                    >
                        <!-- <template #prefix>
                            <img
                                src="/icons/lock-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[15px] mr-2"
                            />
                        </template> -->
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="passwordNew" class="pb-2 font-semibold">Mật khẩu mới:</label>
                    <Input
                        v-model:value="passwordChangeDetail.newPassword"
                        placeholder="Nhập mật khẩu mới"
                        id="passwordNew"
                        class="h-10 shadow-md border-[1px] border-solid border-slate-300"
                        type="password"
                    >
                        <!-- <template #prefix>
                            <img
                                src="/icons/lock-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[15px] mr-2"
                            />
                        </template> -->
                    </Input>
                </div>
                <div class="flex flex-col mb-4">
                    <label for="passwordNewConfirm" class="pb-2 font-semibold"
                        >Xác nhận mật khẩu mới:</label
                    >
                    <Input
                        v-model:value="passwordChangeDetail.confirmPassword"
                        placeholder="Nhập xác nhận mật khẩu mới"
                        id="passwordNewConfirm"
                        class="h-10 shadow-md border-[1px] border-solid border-slate-300"
                        type="password"
                        @blur="handleCheckPasswordConfirm"
                    >
                        <!-- <template #prefix>
                            <img
                                src="/icons/lock-solid.svg"
                                alt="envelope-regular.svg"
                                class="w-[15px] mr-2"
                            />
                        </template> -->
                    </Input>
                    <ELValidate
                        :isValid="!isValidatePasswordConfirm"
                        content="Mật khẩu không khớp"
                    />
                </div>
            </div>
            <template #footer>
                <Button
                    type="default"
                    @click="handleOpenChangePassword(false)"
                    class="mr-3 h-10 font-bold shadow-md"
                >
                    Hủy
                </Button>
                <Button
                    :disabled="!isValidatePasswordConfirm"
                    :loading="isLoadingChangePassword"
                    type="primary"
                    @click="handleChangePassword"
                    class="w-28 h-10 font-bold shadow-md"
                >
                    Cập nhật
                </Button>
            </template>
        </Modal>
    </div>
</template>

<style>
.select-role .ant-select-selector {
    border: none !important;
    box-shadow: none !important;
}
</style>
