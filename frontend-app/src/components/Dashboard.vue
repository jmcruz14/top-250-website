<template>
  <div class="mx-8">

    <div class="grid grid-cols-3 gap-8">
      <div class="col-span-1 flex flex-col gap-2 justify-center">
        <span class="font-proportional font-weight-700 text-2xl">About</span>
        <p class="font-tabular">
          This dashboard was conceptualized and slowly worked on starting in 2022
          as an excuse to explore Data Analysis on my own Letterboxd list. Considering
          the obstacles and challenges faced, I'm very satisfied that I was able to make
          time to show this off to you all.
        </p>
      </div>
      <Card
        class="col-span-2"
        :pt="{
          title: 'm-0 border-b border-slate-300',
          footer: 'border-t border-slate-300'
        }"
      >
        <template #title>General List Stats</template>
        <template #content>
          <div class="grid grid-cols-2 gap-5">
            <span class="font-proportional">Average Rating</span>
            <span class="font-tabular">{{ averageRating }}</span>
            <span class="font-proportional">Average Classic* Rating</span>
            <span class="font-tabular">{{ averageClassicRating }}</span>
            <span class="font-proportional">Range of Ratings</span>
            <span class="font-tabular">{{ rangeRating }}</span>
            <span class="font-proportional">Median</span>
            <span class="font-tabular">{{ medianRating }}</span>
          </div>
          </template>
          <template #footer>
            <div class="flex justify-between">
              <div class="text-sm flex flex-col align-start">
                <span class="font-tabular font-bold">Last update</span>
                <span class="font-proportional">{{ lastUpdate }}</span>
              </div>
              <div class="text-sm flex flex-col align-start">
                <span class="font-tabular font-bold">Publish date</span>
                <span class="font-proportional">{{ publishDate }}</span>
              </div>
            </div>
        </template>
      </Card>
    </div>

    <Divider />
  
    <!-- TODO: add graph here then package into a separate component -->
    <Suspense>
      <template #default>
        <MostReviewed :data="mostReviewedResult" />
      </template>
      <template #fallback>
        <ProgressSpinner v-if="!mostReviewedResult" />
      </template>
    </Suspense>

    <Suspense>
      <template #default>
        <MostViewed :data="mostViewedResult" />
      </template>
      <template #fallback>
        <ProgressSpinner />
      </template>
    </Suspense>

    <Suspense>
      <template #default>
        <MostLiked :data="mostLikedResult" />
      </template>
      <template #fallback>
        <ProgressSpinner />
      </template>
    </Suspense>
    
    <!-- sad annoying statistics -->
    <div class="flex flex-col gap-6">
      <span class="text-3xl font-proprtional ml-[150px]">Sad Numbers...</span>
      <Suspense>
        <template #default>
          <UnratedMovies 
            :data="unratedMoviesResult"
            :lowest-viewed-rating="lowestViewedRating"
            :highest-viewed-unrated="highestViewedUnrated"
          />
        </template>
        <template #fallback>
          <ProgressSpinner class="bg-white" />
        </template>
      </Suspense>
    </div>
    
    <div class="flex flex-col gap-6 pt-12">
      <Suspense>
        <template #default>
          <RickyLee />
        </template>
        <template #fallback>
          <ProgressSpinner class="bg-white" />
        </template>
      </Suspense>
    </div>

      
    <pre>
      {{ data }}
    </pre>

    <Footer />
  </div>
</template>


<script>
import { isUndefined, omit } from 'lodash'
import { ref, computed, watch, onMounted } from 'vue'
import { useD3 } from '~/composables/useD3';
import { useComputeList } from '~/composables/useComputeList';
import { useStatistics } from '~/composables/useStatistics';
import { fetchMovie } from '~/composables/useFilmApi';

import Divider from 'primevue/divider';
import Badge from 'primevue/badge';
import Card from 'primevue/card';
import ProgressSpinner from 'primevue/progressspinner';

import MostReviewed from './dashboard-widgets/MostReviewed';
import MostViewed from './dashboard-widgets/MostViewed';
import MostLiked from './dashboard-widgets/MostLiked'
import RickyLee from './dashboard-widgets/RickyLee'
import UnratedMovies from './dashboard-widgets/UnratedMovies'
import Footer from './dashboard-widgets/Footer'

export default {
  props: {
    data: Object,
    dataMap: Object,
    lastUpdate: String,
    publishDate: String,
  },
  components: {
    Badge,
    Card,
    Divider,
    ProgressSpinner,

    MostReviewed,
	  MostViewed,
    MostLiked,
    UnratedMovies,
    RickyLee,
    Footer
  },
  async setup (props, { emit }) {
    const data = computed(() => props?.data);
    const lastUpdate = computed(() => props?.lastUpdate);
    const publishDate = computed(() => props?.publishDate);

    const averageRating = ref(null);
    const averageClassicRating = ref(null);
    const rangeRating = ref(null);
    const medianRating = ref(null);

    const graphSection = ref(null);
    const lowestViewedRating = ref(null);
    const highestViewedUnrated = ref(null);

    const { 
      calculateAverageRating,
      calculateAverageClassicRating,
      calculateRange,
      calculateMedian,
      calculateLowestStat,
      calculateHighestStat
      } = useComputeList();
      
    const {
      mostReviewed,
      mostViewed,
      mostLiked,
      unratedMovies,
      ratedMovies,
    } = useStatistics();

    const mostReviewedResult = ref(null);
    const mostViewedResult = ref(null);
    const mostLikedResult = ref(null);
    const unratedMoviesResult = ref(null);
    const ratedMoviesResult = ref(null);
    onMounted(async () => {
      if (data?.value && !isUndefined(data?.value)) {
        averageRating.value = calculateAverageRating(data?.value);
        averageClassicRating.value = calculateAverageClassicRating(data?.value);
        rangeRating.value = calculateRange(data?.value);
        medianRating.value = calculateMedian(data?.value);

        mostReviewedResult.value = mostReviewed(data?.value);
		    mostViewedResult.value = mostViewed(data?.value);
        mostLikedResult.value = mostLiked(data?.value);
        unratedMoviesResult.value = unratedMovies(data?.value);
        ratedMoviesResult.value = ratedMovies(data?.value);

        lowestViewedRating.value = calculateLowestStat(ratedMoviesResult?.value?.films, 'watch_count');
        highestViewedUnrated.value = calculateHighestStat(unratedMoviesResult.value?.films, 'watch_count');
      }
    })

    return {
      averageRating,
      averageClassicRating,
      medianRating,
      rangeRating,

      graphSection,
      mostReviewedResult,
	    mostViewedResult,
      mostLikedResult,
      unratedMoviesResult,

      lowestViewedRating,
      highestViewedUnrated,
			
      data,
      lastUpdate,
      publishDate
    }
  }
}
</script>
