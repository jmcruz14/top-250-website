<template>
  <div ref="mostReviewedDiv">
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
    const mostReviewed = computed(() => props?.data);

    const {
      createBarChart
    } = useD3();

    const mostReviewedDiv = ref(null);
    onMounted(async () => {
      if (mostReviewed && !isUndefined(mostReviewed?.value)) {
        Promise.all(mostReviewed?.value?.map(async (film) => {
          const results = await fetchMovie(film['film_id'])
          const movie_data = omit(results, ['_id'])
          return {
            ...film,
            ...movie_data
          }
        })).then(async v => {
          const chart = await createBarChart(
            v, 'review_count', 'film_title',
            '#f1f5f9', 'Film Title', 'Most Reviewed Films', true
          )
          mostReviewedDiv.value.appendChild(chart)
        })
      }
    })

    
    return {
      mostReviewedDiv
    }
  }
}

</script>