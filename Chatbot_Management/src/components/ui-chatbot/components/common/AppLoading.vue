<template>
  <svg
    version="1.1"
    id="L4"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    x="0px"
    y="0px"
    viewBox="0 0 100 100"
    enable-background="new 0 0 0 0"
    xml:space="preserve"
  >
    <circle fill="currentColor" stroke="none" cx="0" cy="50" r="20">
      <animate
        attributeName="opacity"
        dur="1s"
        values="0;1;0"
        repeatCount="indefinite"
        begin="0.1"
      />
    </circle>
    <circle fill="currentColor" stroke="none" cx="66" cy="50" r="20">
      <animate
        attributeName="opacity"
        dur="1s"
        values="0;1;0"
        repeatCount="indefinite"
        begin="0.2"
      />
    </circle>
    <circle fill="currentColor" stroke="none" cx="126" cy="50" r="20">
      <animate
        attributeName="opacity"
        dur="1s"
        values="0;1;0"
        repeatCount="indefinite"
        begin="0.3"
      />
    </circle>
  </svg>
</template>

<style scoped>
svg {
  width: 30px;
  height: 16px;
  display: inline-block;
}
</style>
