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
            <span class="font-tabular">{{ data ? calculateAverageRating(data) : null }}</span>
            <span class="font-proportional">Average Classic* Rating</span>
            <span class="font-tabular">{{ data ? calculateAverageClassicRating(data) : null }}</span>
            <span class="font-proportional">Range of Ratings</span>
            <span class="font-tabular">{{ data ? calculateRange(data) : null }}</span>
            <span class="font-proportional">Median</span>
            <span class="font-tabular">{{ data ? calculateMedian(data) : null }}</span>
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
      <div ref="graphSection">
      </div>
    </Suspense>

    <pre>
      {{ data }}
    </pre>
  </div>
</template>


<script>
import { isUndefined, omit } from 'lodash'
import { ref, computed, watch, onMounted, createVNode } from 'vue'
import { useD3 } from '~/composables/useD3';
import { useComputeList } from '~/composables/useComputeList';
import { useStatistics } from '~/composables/useStatistics';
import { fetchMovie } from '~/composables/useListHistory';

import Widgets from './dashboard-widgets';
import Divider from 'primevue/divider';
import Badge from 'primevue/badge';
import Card from 'primevue/card';

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
    Divider
  },
  async setup (props, { emit }) {
    const data = computed(() => props?.data);
    const lastUpdate = computed(() => props?.lastUpdate);
    const publishDate = computed(() => props?.publishDate);

    const graphSection = ref(null);

    const { 
      calculateAverageRating,
      calculateAverageClassicRating,
      calculateRange,
      calculateMedian
    } = useComputeList();

    const {
      mostReviewed,
      mostViewed
    } = useStatistics();

    const {
      createBarChart
    } = useD3();

    const mostReviewedResult = ref(null);
    const mostViewedResult = ref(null);
    onMounted(async () => {
      if (data?.value && !isUndefined(data?.value)) {
        mostReviewedResult.value = mostReviewed(data?.value)
        Promise.all(mostReviewedResult?.value?.map(async (film) => {
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
          graphSection.value.appendChild(chart)
        })
      }
    })

    return {
      calculateAverageRating,
      calculateAverageClassicRating,
      calculateRange,
      calculateMedian,

      graphSection,

      data,
      lastUpdate,
      publishDate
    }
  }
}
</script>