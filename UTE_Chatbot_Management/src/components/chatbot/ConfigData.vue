<script setup lang="ts">
import FileData from '@/components/configData/FileData.vue'
import ImportFileData from '@/components/configData/ImportFileData.vue'
import QAData from '@/components/configData/QAData.vue'
import { TabPane, Tabs } from 'ant-design-vue'
import { defineProps, onMounted, ref, watch } from 'vue'
import LinkData from '../configData/LinkData.vue'
const props = defineProps<{
    folderId: number
}>()

const activeKey = ref('1')
const folderIdLocal = ref<number>(props.folderId)
const fileDataRef = ref<InstanceType<typeof FileData> | null>(null)
const importFileDataRef = ref<InstanceType<typeof ImportFileData> | null>(null)
const qaDataRef = ref<InstanceType<typeof QAData> | null>(null)
const linkDataRef = ref<InstanceType<typeof LinkData> | null>(null)

onMounted(() => {
    console.log('dataConfig', props.folderId)
})

watch(
    () => props.folderId,
    (newVal, oldVal) => {
        console.log('watch folderId', newVal, oldVal)
        folderIdLocal.value = newVal
        console.log('folderIdLocal', folderIdLocal.value)
        resetData()
    }
)

const resetData = () => {
    fileDataRef.value?.fetchData()
    importFileDataRef.value?.fetchData()
    qaDataRef.value?.fetchData()
    linkDataRef.value?.fetchData()
}

defineExpose({ resetData })
</script>

<template>
    <div class="config-data h-[490px]">
        <Tabs v-model:activeKey="activeKey" tab-position="left">
            <TabPane key="1" tab="Văn bản">
                <FileData ref="fileDataRef" :folderId="folderIdLocal" />
            </TabPane>
            <TabPane key="2" tab="File">
                <ImportFileData ref="importFileDataRef" :folderId="folderIdLocal" />
            </TabPane>
            <TabPane key="3" tab="Câu hỏi">
                <QAData ref="qaDataRef" :folderId="folderIdLocal" />
            </TabPane>
            <TabPane key="4" tab="Link">
                <LinkData ref="linkDataRef" :folderId="folderIdLocal" />
            </TabPane>
        </Tabs>
    </div>
</template>

<style></style>
