<script setup lang="ts">
import Curtain from '@/components/Curtain.vue'
import LanguageChanger from '@/components/LanguageChanger.vue'
import { ref } from 'vue'

const showCurtain = ref(true)

setTimeout(() => {
    showCurtain.value = false // Show only 500ms for "đẹp" purpose
}, 500)
</script>

<template>
    <Curtain :show="showCurtain" />
    <div class="__auth-layout__ relative">
        <div class="absolute flex flex-col justify-center items-center p-8 w-full h-full">
            <!-- <RouterLink to="/" class="cursor-pointer flex items-center">
                <img src="/images/logo-truong-250.png" alt="logo" class="h-[60px] mr-2" />
                <div class="text-base uppercase font-medium">
                    <p class="font-semibold">Trường ĐH Sư phạm Kỹ thuật</p>
                    <p>Đại học Đà Nẵng</p>
                </div>
            </RouterLink> -->
            <slot />
        </div>
        <div class="right hidden lg:block flex-1">
            <div class="overflow-hidden w-full h-full">
                <div class="bg-image w-full h-full">
                    <div
                        class="w-full h-full bg-black bg-opacity-25 text-white flex flex-col justify-end items-start"
                    >
                        <div class="bg-black bg-opacity-55 w-full px-5 py-3">
                            <p class="uppercase text-xl font-semibold pb-1">
                                Trường Đại học Sư phạm Kỹ thuật - Đại học Đà Nẵng
                                <!-- <span class="uppercase text-xl font-medium">Đại học Đà Nẵng</span> -->
                            </p>

                            <div class="flex">
                                <div class="flex items-start text-xs font-normal mr-6">
                                    <p class="pr-2">Địa chỉ:</p>
                                    <p>
                                        - Cơ sở 1 số 48 Cao Thắng, TP. Đà Nẵng<br />
                                        - Cơ sở 2 khu Đô thị đại học, Hòa Quý, Ngũ Hành Sơn, Đà Nẵng
                                    </p>
                                </div>
                                <div>
                                    <p class="text-xs font-normal">Điện thoại: (0236) 3822571</p>
                                    <p class="text-xs font-normal">Email: dhspktdn@ute.udn.vn</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <LanguageChanger className="absolute hehe right-2 bottom-2 w-28 bg-transparent" />
        </div>
    </div>
</template>

<style lang="less" scoped>
.__auth-layout__ {
    @apply flex w-screen h-screen justify-center;
}
.bg-image {
    background-color: #dda267;
    background-image: url(/images/auth-layout-img1.jpg);
    background-position: center;
    background-size: cover;
    object-fit: cover;
}
</style>
