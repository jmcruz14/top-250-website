<template>
  <div class="mx-4 flex flex-col gap-3">
    <span class="font-tabular">This is a graph</span>
    <!-- <pre>
      {{ result }}
    </pre> -->
    <span class="font-proportional">This is also a graph</span>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as d3 from "d3"; 
// import d3

export default {
  setup () {
    const result = ref(null);
    onMounted(async () => {
    })

    return {
      result
    }
  }
}

</script>