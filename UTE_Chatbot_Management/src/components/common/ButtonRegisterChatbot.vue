<template>
    <!-- <button
        class="border text-gray-50 duration-300 relative group cursor-pointer overflow-hidden h-11 w-48 rounded-md bg-neutral-800 p-2 font-extrabold shadow-lg hover:shadow-tk-btn-2 hover:bg-slate-200 hover:text-tk-btn-color-primary"
    >
        <div
            class="absolute group-hover:-top-1 group-hover:-right-2 z-10 w-16 h-16 rounded-full group-hover:scale-150 duration-700 right-12 top-12 bg-yellow-500"
        ></div>
        <div
            class="absolute group-hover:-top-1 group-hover:-right-2 z-10 w-12 h-12 rounded-full group-hover:scale-150 duration-700 right-20 -top-6 bg-orange-500"
        ></div>
        <div
            class="absolute group-hover:-top-1 group-hover:-right-2 z-10 w-8 h-8 rounded-full group-hover:scale-150 duration-700 right-32 top-6 bg-pink-500"
        ></div>
        <div
            class="absolute group-hover:-top-1 group-hover:-right-2 z-10 w-4 h-4 rounded-full group-hover:scale-150 duration-700 right-2 top-12 bg-red-600"
        ></div>
        <p class="z-10 h-11 w-48 absolute bottom-0 left-0 flex justify-center items-center">
            Đăng ký Chatbot
        </p>
    </button> -->

    <button class="button">
        <span class="button_lg">
            <span class="button_sl"></span>
            <span class="button_text">Đăng ký Chatbot</span>
        </span>
    </button>
</template>

<style>
/* Đăng ký Chatbot */
.button {
    -moz-appearance: none;
    -webkit-appearance: none;
    appearance: none;
    border: none;
    background: none;
    cursor: pointer;
    position: relative;
    padding: 6px;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 14px;
    transition: all 0.9s ease-in-out;
}

.button::before,
.button::after {
    content: '';
    display: block;
    position: absolute;
    right: 0;
    left: 0;
    height: calc(50% - 5px);
    border: 1px solid #7d8082;
    transition: all 0.85s ease;
}

.button::before {
    top: 0;
    border-bottom-width: 0;
}

.button::after {
    bottom: 0;
    border-top-width: 0;
}

.button:active,
.button:focus {
    outline: none;
}

.button:active::before,
.button:active::after {
    right: 3px;
    left: 3px;
}

.button:active::before {
    top: 3px;
}

.button:active::after {
    bottom: 3px;
}

.button_lg {
    position: relative;
    display: block;
    padding: 10px 20px;
    color: #fff;
    background-color: #0f1923;
    overflow: hidden;
    box-shadow: inset 0px 0px 0px 1px transparent;
}

.button_lg::before {
    content: '';
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 2px;
    height: 2px;
    background-color: #0f1923;
}

.button_lg::after {
    content: '';
    display: block;
    position: absolute;
    right: 0;
    bottom: 0;
    width: 4px;
    height: 4px;
    background-color: #0f1923;
    transition: all 0.8s ease;
}

.button_sl {
    display: block;
    position: absolute;
    top: 0;
    bottom: -1px;
    left: -8px;
    width: 0;
    background-color: #0879a6;
    transform: skew(-15deg);
    transition: all 0.8s ease;
}

.button_text {
    position: relative;
}

.button:hover {
    color: #0f1923;
}

.button:hover .button_sl {
    width: calc(100% + 15px);
}

.button:hover .button_lg::after {
    background-color: #fff;
}
</style>
