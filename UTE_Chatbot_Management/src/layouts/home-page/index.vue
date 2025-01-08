<script setup lang="ts">
import Curtain from '@/components/Curtain.vue'
// import Footer from '@/components/shared/Footer.vue'
import Navbar from '@/components/shared/Navbar.vue'
import { ref } from 'vue'

const showCurtain = ref(true)

setTimeout(() => {
    showCurtain.value = false // Show only 500ms for "đẹp" purpose
}, 500)
</script>

<template>
    <Curtain :show="showCurtain" />
    <div class="flex flex-col">
        <Navbar />
        <div class="default-component">
            <slot />
        </div>
        <!-- <Footer /> -->
    </div>
</template>

<style lang="less" scoped>
.default-component {
    // box-shadow: rgba(0, 0, 0, 0.2) 0px 12px 28px 0px, rgba(0, 0, 0, 0.1) 0px 2px 4px 0px,
    //     rgba(255, 255, 255, 0.05) 0px 0px 0px 1px inset;
}
</style>
