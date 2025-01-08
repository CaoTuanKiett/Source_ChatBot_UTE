<script lang="ts" setup>
import ButtonDelete from '@/components/common/ButtonDelete.vue'
import type { DataChatbot } from '@/interfaceConfig'
import { Button, Tooltip } from 'ant-design-vue'
import { defineProps, onMounted, ref } from 'vue'

const props = defineProps<{
    item: DataChatbot
    toggleCheckbox: (item: any) => void
    handleSetting: (item: any) => void
    handleDelete: (item: any) => void
    handleShowChatbot: (show: boolean, token: string) => void
}>()

const isActive = ref(props.item.status)
const isLoadingDelete = ref<boolean>(false)

onMounted(() => {
    isActive.value = props.item.status
    // console.log('item', props.item)
})

const handleDelete = async (item: any) => {
    isLoadingDelete.value = true
    await props.handleDelete(item)
    isLoadingDelete.value = false
}

const copyToClipboard = (token: string) => {
    navigator.clipboard.writeText(token)
}
</script>

<template>
    <div
        class="chatbot border-2 border-slate-300 rounded-lg p-4 mb-6 shadow-tk-btn flex w-[1000px]"
    >
        <img src="/images/bot.png" alt="itemhotel" class="w-32 h-32 object-cover rounded mr-4" />
        <div class="flex justify-between w-full">
            <div class="flex flex-col justify-between py-2">
                <div class="flex items-center">
                    <h2 class="font-semibold text-xl text-nowrap mr-3">
                        {{ props.item.chatBotName }}
                    </h2>
                    <Tooltip
                        color="#ccc"
                        :title="props.item.status ? 'Đang hoạt động' : 'Không hoạt động'"
                        placement="right"
                    >
                        <span
                            class="block w-3 h-3 rounded-full"
                            :class="props.item.status ? 'bg-tk-active' : 'bg-tk-inactive'"
                        >
                        </span>
                    </Tooltip>
                </div>
                <p class="text-sm">Tạo bởi: {{ props.item.createdBy || 'Admin' }}</p>
                <p class="text-sm truncate max-w-[500px]">Mô tả: {{ props.item.description }}</p>
                <div class="flex">
                    <p class="text-sm mr-2">Token:</p>
                    <p class="text-sm max-w-64 truncate">{{ props.item.token }}</p>

                    <Tooltip placement="right" color="#ccc">
                        <template #title>
                            <span class="text-xs text-black">Copy token</span>
                        </template>
                        <button class="ml-2" @click="copyToClipboard(props.item.token)">
                            <img
                                src="/icons/copy-regular.svg"
                                alt="copy-regular.svg"
                                class="w-4 h-4 cursor-pointer"
                            />
                        </button>
                    </Tooltip>
                </div>
            </div>
            <div class="flex flex-col justify-between items-end py-2 mr-4">
                <div class="flex items-end">
                    <p class="text-sm">
                        Cập nhật lần cuối:
                        <span class="font-medium">{{
                            props.item.updatedTime || props.item.createdTime
                        }}</span>
                    </p>
                </div>
                <div class="flex row">
                    <div class="flex">
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">Thử nghiệm</span>
                            </template>
                            <Button
                                class="flex items-center mr-3 hover:opacity-60 hover:border-slate-500 transition-all duration-300"
                                @click="props.handleShowChatbot(true, props.item.token)"
                            >
                                <img
                                    src="/icons/robot-solid.svg"
                                    class="w-5"
                                    alt="robot-solid.svg"
                                />
                            </Button>
                        </Tooltip>
                        <Tooltip color="#ccc">
                            <template #title>
                                <span class="text-xs text-black">Chỉnh sửa</span>
                            </template>
                            <Button
                                class="flex items-center mr-3 hover:opacity-60 hover:border-slate-500 transition-all duration-300"
                                @click="handleSetting(props.item)"
                            >
                                <img
                                    src="/icons/pen-to-square-solid.svg"
                                    class="w-4"
                                    alt="pen-to-square-solid.svg"
                                />
                            </Button>
                        </Tooltip>

                        <ButtonDelete
                            :handleDelete="handleDelete"
                            :id="props.item"
                            :title="'Xác nhận xóa chatbot?'"
                            :isLoadingDelete="isLoadingDelete"
                            srcIcon="/icons/trash-solid.svg"
                            :isChatbot="true"
                        />

                        <!-- <Popconfirm
                            title="Xác nhận xóa chatbot?"
                            okText="Xóa"
                            cancelText="Không"
                            @confirm="handleDelete(props.item)"
                        >
                            <Tooltip color="#ccc">
                                <template #title>
                                    <span class="text-xs text-black">Xóa</span>
                                </template>

                                <Button class="flex items-center hover:opacity-60">
                                    <img
                                        src="/icons/trash-solid.svg"
                                        class="w-4"
                                        alt="trash-solid.svg"
                                    />
                                </Button>
                            </Tooltip>
                        </Popconfirm> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
/* Include any styles needed for the component here */
</style>
