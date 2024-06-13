<template>
  <div ref="mostViewedDiv" class="ml-[200px]">
  </div>
</template>

<script>
import { isUndefined, omit } from 'lodash';
import { ref, onMounted, computed } from 'vue';
import { fetchMovie } from '@/composables/useListHistory';
import { useD3 } from '@/composables/useD3';

export default {
  props: {
    data: Object
  },
  async setup (props) {
    // A component is considered SUSPENSEFUL in two ways
    // 1. having an async setup()
    // 2. top level await (in script setup)
    const mostViewed = computed(() => props?.data);

    const {
      createBarChart
    } = useD3();

    const mostViewedDiv = ref(null);
    onMounted(async () => {
      if (mostViewed && !isUndefined(mostViewed?.value)) {
        Promise.all(mostViewed?.value?.map(async (film) => {
          const results = await fetchMovie(film['film_id'])
          const movie_data = omit(results, ['_id'])
          return {
            ...film,
            ...movie_data
          }
        })).then(async v => {
          const chart = await createBarChart(
            v, 'watch_count', 'film_title',
            '#f1f5f9', 'Film Title', 'Most Watched Films', true
          )
          mostViewedDiv.value.appendChild(chart)
        })
      }
    })

    
    return {
      mostViewedDiv
    }
  }
}

</script>
