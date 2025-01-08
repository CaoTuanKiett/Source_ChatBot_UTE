<script lang="ts" setup>
import { Button, Popconfirm, Tooltip } from 'ant-design-vue'
import { defineProps } from 'vue'

const props = defineProps<{
    handleDelete: (item: any) => void
    id: any
    title: string
    isLoadingDelete: boolean
    srcIcon: string
    isChatbot?: boolean | false
}>()

// onMounted(() => {
//     console.log('props', props)
// })
</script>

<template>
    <Popconfirm :title="props.title">
        <template #okButton>
            <Button :loading="props.isLoadingDelete" @click="props.handleDelete(id)"> Xóa </Button>
        </template>

        <template #cancelButton>
            <!-- <Button>Không</Button> -->
        </template>
        <Tooltip color="#ccc">
            <template #title>
                <span class="text-xs text-black">Xóa</span>
            </template>
            <Button
                v-if="props.isChatbot"
                class="flex items-center hover:opacity-60 hover:border-slate-500 transition-all duration-300"
            >
                <img :src="props.srcIcon" class="w-4" alt="deleteIcon" />
            </Button>
            <button v-else>
                <img
                    src="/icons/icon-delete-black.svg"
                    alt="delete"
                    class="cursor-pointer hover:border-slate-500 transition-all duration-300"
                />
            </button>
        </Tooltip>
    </Popconfirm>
</template>

<style>
.ant-popover-content .ant-popover-inner .ant-popconfirm-inner-content {
    display: flex !important;
    align-items: center !important;
}

.ant-popover-content
    .ant-popover-inner
    .ant-popconfirm-inner-content
    .ant-popconfirm-buttons
    button {
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
}

.ant-popover-content .ant-popconfirm-message {
    margin: 0px !important;
}
</style>