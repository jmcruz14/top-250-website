<template>

</template>

<script>
import { isUndefined, omit } from 'lodash';
import { ref, onMounted, computed, toRefs } from 'vue';
import Card from 'primevue/card'
import { fetchMovie } from '@/composables/useFilmApi';
// import { useD3 } from '@/composables/useD3';

export default {
  props: {
    data: Object,
    lowestViewedRating: Object,
    highestViewedUnrated: Object
  },
  components: {
    Card
  },
  async setup (props){
    return {}
  }
}
</script>