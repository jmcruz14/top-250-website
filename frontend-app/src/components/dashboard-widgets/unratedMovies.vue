<template>
  <!--  -->
  <div class="flex flex-row gap-6">
    <Card class="w-1/2 h-fit">
      <!-- get the ff -->
      <template #title>Unrated Movies</template>
      <template #subtitle>
        <span class="italic text-sm">
          The <a href="https://letterboxd.com/journal/the-score-new-weighted-average-ratings/" class="underline">New Algorithm</a> Does Not Show All The Ratings
        </span>
      </template>
      <template #content>
        <ul class="list-disc ml-2">
          <li>
            <span class="font-tabular">
              <span class="font-bold">{{ percentUnrated }}%</span> of Filipino films in the list are currently
              unrated.
            </span>
          </li>
          <li>
            <span class="font-tabular">
              <span class="font-bold">{{ lowestViewedRating ? lowestViewMovie?.film_title : null }}</span>
              with <span class="font-bold">{{ lowestViewedRating ? lowestViewMovie?.watch_count : null }}</span> views is the 
              <span class="">lowest viewed film</span>
              with a visible rating.
            </span>
          </li>
          <li> 
            <span class="font-tabular">
              <span class="font-bold">{{ highestViewUnratedMovie ? highestViewUnratedMovie?.film_title : null }}</span>
              with <span class="font-bold">{{ highestViewUnratedMovie ? highestViewUnratedMovie?.watch_count : null }}</span> views is the 
              highest viewed film without a visible rating.
            </span>
          </li>
        </ul>
      </template>
    </Card>

    <Card class="w-1/2 h-fit mt-[100px]">
      <template #title>Outside the Canon</template>
      <template #subtitle>
        <span class="italic text-sm">
          What we lost...
        </span>
      </template>
      <template #content>
        <p>Maiores fugiat dolorum dicta deleniti minima veniam. Molestias voluptatibus temporibus. Libero necessitatibus nisi.
Doloremque cupiditate illo quam. Officia iusto officia quaerat ullam. Cupiditate ad debitis deserunt modi minima dignissimos quibusdam dolorem explicabo.
Modi laboriosam hic voluptatem corrupti quasi inventore. Blanditiis assumenda delectus pariatur quod hic. Modi eum deserunt animi.</p>
      </template>
    </Card>
  </div>
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
  async setup (props) {
    // A component is considered SUSPENSEFUL in two ways
    // 1. having an async setup()
    // 2. top level await (in script setup)

    const films = computed(() => props?.data?.films);
    const average_rating = computed(() => props?.data?.average_rating);
    const average_watch_count = computed(() => props?.data?.average_watch_count);
    const count = computed(() => props?.data?.count);
    const lowestViewedRating = computed(() => props?.lowestViewedRating);
    const highestViewedUnrated = computed(() => props?.highestViewedUnrated);

    // const {
    //   createBarChart
    // } = useD3();

    // unrated stats
    // - average rating of unrated films based on histogram

    // const mostViewedDiv = ref(null);
    const percentUnrated = ref(null);
    const lowestViewMovie = ref(null);
    const highestViewUnratedMovie = ref(null);
    onMounted(async () => {
      percentUnrated.value = ((count?.value / 250) * 100).toPrecision(4);
      if (lowestViewedRating && !isUndefined(lowestViewedRating?.value)) {
        const results = await fetchMovie(lowestViewedRating?.value?.film_id);
        const movie_data = omit(results, ['_id']);
        lowestViewMovie.value = {
          ...lowestViewedRating?.value,
          ...movie_data
        }
      }

      if (highestViewedUnrated && !isUndefined(highestViewedUnrated?.value)) {
        const results = await fetchMovie(highestViewedUnrated?.value?.film_id);
        const movie_data = omit(results, ['_id']);
        highestViewUnratedMovie.value = {
          ...highestViewedUnrated?.value,
          ...movie_data
        }
      }
    })

    
    return {
      percentUnrated,
      lowestViewMovie,
      highestViewUnratedMovie
    }
  }
}
</script>