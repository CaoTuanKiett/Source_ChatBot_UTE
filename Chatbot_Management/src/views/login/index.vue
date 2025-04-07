<script setup lang="ts">
import type { LoginRequest } from '@/api/auth/auth.dto.ts'
import router, { RoutePath } from '@/router'
import { useAuthStore } from '@/stores/auth'
import { Icon } from '@iconify/vue'
import { useMutation } from '@tanstack/vue-query'
import { Button, Form, FormItem, Input, InputPassword } from 'ant-design-vue'
import { reactive, ref } from 'vue'
import GotoForgotPasswordButton from './GotoForgotPasswordButton.vue'
import SSOButtons from './SSOButtons.vue'

const auth = useAuthStore()
const isHidenPassword = ref(true)

const loginFormState = reactive<LoginRequest>({
    email: '',
    password: ''
})

if (auth.isLoggedIn) router.push(RoutePath.Home)

const { mutate, isPending } = useMutation({
    mutationKey: ['login'],
    mutationFn: async () => {
        await auth.login(loginFormState)
        router.push(auth.returnUrl || RoutePath.Home)
    },
    throwOnError: true
})

const handleLoginFailed = (errInfo: any) => {
    console.log('Failed:', errInfo)

    // * Error will be handled by the AsyncErrorBoundary}
}
</script>

<template>
    <div id="login" class="my-auto w-[490px] relative p-8">
        <span class="bg-black opacity-75 absolute top-0 bottom-0 right-0 left-0 rounded-xl"></span>
        <div class="z-10 relative text-white">
            <!-- Title -->
            <div class="flex items-center justify-between">
                <h1 class="login__title font-bold text-4xl flex items-center mb-1">
                    Xin chào bạn
                    <img
                        src="/icons/hand-peace-regular.svg"
                        alt="hand-peace-regular.svg"
                        class="w-8 h-8 ml-1"
                    />
                    !
                </h1>
                <RouterLink to="/" class="flex items-center">
                    <img
                        src="/images/logo-truong-250.png"
                        alt="logo-truong-250.png"
                        class="w-12 h-12 ml-1"
                    />
                </RouterLink>
            </div>
            <p class="mb-7 flex items-center italic text-sm">Vui lòng đăng nhập!</p>

            <!-- Login form -->
            <Form
                class="login__form"
                :model="loginFormState"
                layout="vertical"
                @finish="mutate"
                @finish-failed="handleLoginFailed"
            >
                <!-- ---- -->
                <FormItem
                    name="email"
                    :rules="[
                        { required: true, message: $t('login.form.validation.email.required') }
                    ]"
                    class="mb-3"
                >
                    <label for="" class="font-semibold ml-1 mb-1 text-white">Email:</label>
                    <Input
                        type="text"
                        size="large"
                        v-model:value="loginFormState.email"
                        :placeholder="$t('login.form.email')"
                        auto-complete="off"
                        class="rounded-md shadow-md border-tk-primary-color p-2 focus:border-blue-500"
                    >
                        <template #prefix>
                            <Icon icon="ph:envelope-simple-bold" class="mx-2" />
                        </template>
                    </Input>
                </FormItem>

                <FormItem
                    name="password"
                    :rules="[
                        { required: true, message: $t('login.form.validation.password.required') }
                    ]"
                >
                    <label for="" class="font-semibold ml-1 mb-1 text-white">Mật khẩu:</label>
                    <InputPassword
                        type="password"
                        size="large"
                        v-model:value="loginFormState.password"
                        :placeholder="$t('login.form.password')"
                        auto-complete="off"
                        class="rounded-md shadow-md border-tk-primary-color p-2"
                    >
                        <template #prefix>
                            <Icon icon="ph:lock-simple-bold" class="mx-2" />
                        </template>
                        <template #iconRender="isHidenPassword">
                            <img
                                v-if="isHidenPassword"
                                src="/icons/eye-regular.svg"
                                alt="eye-regular.svg"
                                class="w-5 h-5 cursor-pointer"
                            />
                            <img
                                v-else
                                src="/icons/eye-slash-regular.svg"
                                alt="eye-slash-regular.svg"
                                class="w-5 h-5 cursor-pointer"
                            />
                        </template>
                    </InputPassword>
                    <!-- <span class="z-11 absolute right-3 bottom-[10px]">
                        <img
                            :src="true ? '/icons/eye-regular.svg' : '/icons/eye-slash-regular.svg'"
                            alt="eye-regular.svg"
                            class="w-5 h-5 cursor-pointer"
                        />
                    </span> -->
                </FormItem>

                <!-- ---- -->
                <div class="forgot-password mb-2 flex justify-end">
                    <GotoForgotPasswordButton />
                </div>
                <FormItem>
                    <Button
                        :loading="isPending"
                        size="large"
                        class="font-semibold hover:shadow-xl bg-[#891eff] border-none text-white hover:opacity-80"
                        html-type="submit"
                        block
                    >
                        Đăng nhập
                    </Button>
                </FormItem>
            </Form>

            <!-- <div class="login__suggest-register flex flex-col mt-20">
            <span class="text-center text-[16px] mb-2 cursor-default">
                {{ $t('login.register_reminder') }}
            </span>
            <GotoRegisterPageButton />
        </div> -->

            <div class="login__sso">
                <SSOButtons />
            </div>
        </div>
    </div>
</template>

<style lang="less" >
.my-auto .ant-input-password-icon {
    cursor: pointer;
    width: 20px;
}
</style>
