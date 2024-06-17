<template>
  <div ref="mostLikedDiv" class="drop-shadow-md">
  </div>
</template>

<script>
import { isUndefined, omit } from 'lodash';
import { ref, onMounted, computed } from 'vue';
import { fetchMovie } from '~/composables/useFilmApi';
import { useD3 } from '@/composables/useD3';

export default {
  props: {
    data: Object
  },
  async setup (props) {
    // A component is considered SUSPENSEFUL in two ways
    // 1. having an async setup()
    // 2. top level await (in script setup)
    const mostLiked = computed(() => props?.data);

    const {
      createBarChart
    } = useD3();

    const mostLikedDiv = ref(null);
    onMounted(async () => {
      if (mostLiked && !isUndefined(mostLiked?.value)) {
        Promise.all(mostLiked?.value?.map(async (film) => {
          const results = await fetchMovie(film['film_id'])
          const movie_data = omit(results, ['_id'])
          return {
            ...film,
            ...movie_data
          }
        })).then(async v => {
          const chart = await createBarChart(
            v, 'like_count', 'film_title',
            '#f1f5f9', 'Film Title', 'Most Liked Films', true
          )
          mostLikedDiv.value.appendChild(chart)
        })
      }
    })

    
    return {
      mostLikedDiv
    }
  }
}

</script>