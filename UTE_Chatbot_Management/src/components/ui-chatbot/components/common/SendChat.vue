<template>
    <button>
        <div class="svg-wrapper-1 opacity-85">
            <div class="svg-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22" width="28" height="28">
                    <path fill="none" d="M0 0h24v24H0z"></path>
                    <path
                        fill="currentColor"
                        d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"
                    ></path>
                </svg>
            </div>
        </div>
    </button>
</template>

<style scoped>
button {
    font-family: inherit;
    background: transparent;
    color: black;
    padding: 8px;
    /* padding-left: 0.9em; */
    display: flex;
    align-items: center;
    border: none;
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.2s;
    cursor: pointer;
    outline: none;
}

button span {
    display: block;
    margin-left: 0.3em;
    transition: all 0.3s ease-in-out;
}

button svg {
    display: block;
    transform-origin: center center;
    transition: transform 0.3s ease-in-out;
}

button:hover .svg-wrapper {
    animation: fly-1 0.6s ease-in-out infinite alternate;
}

button:hover svg {
    transform: rotate(45deg) scale(1.2);
}

button:hover span {
    transform: translateX(5em);
}

button:active {
    transform: scale(0.95);
}

@keyframes fly-1 {
    from {
        transform: translateY(0.1em);
    }

    to {
        transform: translateY(-0.1em);
    }
}
</style>
