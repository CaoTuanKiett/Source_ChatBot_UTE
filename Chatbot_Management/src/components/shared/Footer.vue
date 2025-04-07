<script setup lang="ts"></script>

<template>
    <div class="footer px-24 bg-tk-color">
        <div class="flex justify-between py-20">
            <div class="w-[600px]">
                <RouterLink to="/" class="flex items-center ml-[-20px]">
                    <img
                        src="/icons/logofooter.svg"
                        alt="logo-vaias"
                        class="w-24 h-20 mr-[-10px]"
                    />
                    <div>
                        <span class="font-bold text-white text-2xl">VAIAS</span>
                        <span class="text-tk-inactive text-xl">-Tourism</span>
                    </div>
                </RouterLink>
                <p class="mt-4 text-white text-base">
                    Nền tảng tự động hóa tiên tiến cho ngành dịch vụ lưu trú du lịch. Sử dụng trí
                    tuệ nhân tạo để tư vấn, đặt phòng và hỗ trợ khách hàng 24/7, VAIAS giúp giảm chi
                    phí, tối ưu hóa vận hành và nâng cao trải nghiệm khách hàng. Dễ dàng tích hợp
                    vào các nền tảng phổ biến, VAIAS mang lại sự tiện lợi và hiệu quả vượt trội cho
                    doanh nghiệp du lịch.
                </p>
            </div>
            <div class="flex gap-12 text-white">
                <div class="flex flex-col gap-4">
                    <h3 class="font-semibold text-lg mb-2">Tìm hiểu thêm</h3>
                    <p>Về chúng tôi</p>
                    <p>Tính năng</p>
                    <p>Quản lý chatbot</p>
                    <p>Chính sách</p>
                </div>
                <div class="flex flex-col gap-4">
                    <h3 class="font-semibold text-lg mb-2">Liên hệ chúng tôi</h3>
                    <div class="flex items-center justify-start">
                        <img src="/icons/location.svg" alt="icon-location" class="mr-3 w-7" />
                        <p>87 Nguyễn Phước Thái, TP. Đà Nẵng</p>
                    </div>
                    <div class="flex items-center justify-start">
                        <img src="/icons/phone.svg" alt="icon-location" class="mr-3 w-7" />
                        <p>(+84) 937546123</p>
                    </div>
                    <div class="flex items-center justify-start">
                        <img src="/icons/phone2.svg" alt="icon-location" class="mr-3 w-7" />
                        <p>(+84) 937546123</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="text-white flex justify-between border-t-4 py-7 px-1">
            <p class="text-sm">© 2021 VAIAS. All rights reserved.</p>
            <p class="text-sm">Terms & Condition</p>
        </div>
    </div>
</template>

<style lang="less" scoped></style>
