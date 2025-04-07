<script setup lang="ts"></script>

<template>
    <div class="relative border-2 p-2 px-4 flex items-center">
        <img src="/icons/school-flag-solid.svg" alt="school-flag-solid.svg" class="w-20 mr-12" />
        <div class="flex w-full">
            <div class="pr-20">
                <p class="text-sm"><span class="font-medium mr-1">Tên trường: </span>School Name</p>
                <p class="text-sm"><span class="font-medium mr-1">Mã trường: </span>Code</p>
            </div>
            <div class="pr-20">
                <p class="text-sm"><span class="font-medium mr-1">Số điện thoại: </span>Phone</p>
                <p class="text-sm"><span class="font-medium mr-1">Email: </span>Email</p>
            </div>
            <div class="pr-20">
                <p class="text-sm"><span class="font-medium mr-1">Website: </span>Website</p>
                <p class="text-sm"><span class="font-medium mr-1">Địa chỉ: </span>Địa chỉ</p>
            </div>
            <div class="absolute right-4 top-4 flex">
                <Button
                    class="flex items-center mr-3 hover:opacity-60"
                    @click="handleOpenModal(file, true)"
                    ><img
                        src="/icons/pen-to-square-solid.svg"
                        class="w-4"
                        alt="pen-to-square-solid.svg"
                /></Button>
                <Button
                    class="flex items-center hover:opacity-60"
                    @click="showDeleteConfirm(file.idFile)"
                    ><img src="/icons/trash-solid.svg" class="w-4" alt="trash-solid.svg"
                /></Button>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
