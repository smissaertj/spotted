<template>
  <footer class="footer items-center p-4 bg-base-100 text-neutral-content">
    <div class="items-center grid-flow-col font-bold">
      <a href="https://joerismissaert.dev" target="_blank">
        <p>Copyright © 2022 - Joeri JM Smissaert</p>
      </a>
    </div>
    <div class="grid-flow-col gap-4 fmd:place-self-center md:justify-self-end">
      <a href="https://github.com/smissaertj/spotted" target="_blank">
        <button class="btn btn-ghost">
          <font-awesome-icon icon="fa-brands fa-github" size="2x" />
        </button>
      </a>
    </div>
  </footer>
</template>

<script>
export default {
  name: "appFooter",
};
</script>
