<script lang="ts" setup>
import { defineProps } from 'vue'

const props = defineProps<{
    isValid: boolean
    content: string
}>()
</script>

<template>
    <span v-if="props.isValid" class="text-red-700 text-xs flex items-center mt-1 pl-1 font-medium">
        <img src="@/assets/icons/circle-xmark-solid.svg" alt="error" class="w-3 mr-1" />{{
            props.content
        }}</span
    >
</template>