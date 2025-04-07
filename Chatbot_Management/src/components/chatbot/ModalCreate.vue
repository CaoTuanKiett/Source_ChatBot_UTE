<script setup lang="ts">
import { Modal } from 'ant-design-vue'
import { computed, defineProps } from 'vue'
import AddNewChatbot from './AddNewChatbot.vue'

const props = defineProps({
    openModal: Boolean,
    isCreateNew: Boolean,
    handleCloseModal: Function,
    dataChatbotDetail: Object
})

const openModalLocal = computed({
    get: () => props.openModal,
    set: (value) => {
        if (!value) {
            props.handleCloseModal && props.handleCloseModal()
        }
    }
})
const isCreateNewLocal = computed(() => props.isCreateNew)

const handleClose = () => {
    console.log('hehe')
    openModalLocal.value = false
    props.handleCloseModal && props.handleCloseModal()
}
</script>

<template>
    <Modal
        v-model:open="openModalLocal"
        :title="isCreateNewLocal ? 'Tạo mới ChatBot' : 'Chỉnh sửa ChatBot'"
        width="1200px"
        :maskClosable="false"
    >
        <template #footer> </template>
        <AddNewChatbot
            :handleClose="handleClose"
            :isCreateNew="props.isCreateNew"
            :dataChatbotDetail="props.dataChatbotDetail"
        />
    </Modal>
</template>

<style scoped></style>
