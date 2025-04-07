<template>
    <div class="checkbox-wrapper-22">
        <label class="switch" for="checkbox">
            <input type="checkbox" id="checkbox" />
            <div class="slider round"></div>
        </label>
    </div>
</template>

<style>
.checkbox-wrapper-22 .switch {
    display: inline-block;
    height: 34px;
    position: relative;
    width: 60px;
}

.checkbox-wrapper-22 .switch input {
    display: none;
}

.checkbox-wrapper-22 .slider {
    background-color: #ccc;
    bottom: 0;
    cursor: pointer;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    transition: 0.4s;
}

.checkbox-wrapper-22 .slider:before {
    background-color: #fff;
    bottom: 4px;
    content: '';
    height: 26px;
    left: 4px;
    position: absolute;
    transition: 0.4s;
    width: 26px;
}

.checkbox-wrapper-22 input:checked + .slider {
    background-color: #66bb6a;
}

.checkbox-wrapper-22 input:checked + .slider:before {
    transform: translateX(26px);
}

.checkbox-wrapper-22 .slider.round {
    border-radius: 34px;
}

.checkbox-wrapper-22 .slider.round:before {
    border-radius: 50%;
}
</style>
