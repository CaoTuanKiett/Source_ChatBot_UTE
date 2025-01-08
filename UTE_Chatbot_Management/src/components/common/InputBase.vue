<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
    classInputBase: {
        type: String,
        default: ''
    },
    title: {
        type: String,
        required: true
    },
    classTitle: {
        type: String,
        default: ''
    },
    classInput: {
        type: String,
        default: ''
    },
    modelValue: {
        type: String,
        required: true
    },
    type: {
        type: String,
        default: 'text'
    },
    placeholder: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue'])

const onInput = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', target.value)
}
</script>

<template>
    <div class="`input-base ${props.classInputBase}`">
        <p :class="`text-sm font-semibold ${props.classTitle}`">{{ props.title }}</p>
        <input
            :value="props.modelValue"
            :type="props.type"
            :placeholder="props.placeholder"
            :disabled="props.disabled"
            @input="onInput"
            :class="props.classInput"
            width=""
        />
    </div>
</template>

<style scoped>
.input-base {
    /* p {
        font-size: 1.25rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    } */

    input {
        width: 100%;
        padding: 0.5rem 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        font-size: 1rem;
        line-height: 1.5;
        color: #374151;
        background-color: #fff;
        transition:
            border-color 0.15s ease-in-out,
            box-shadow 0.15s ease-in-out;
    }
}
</style>
