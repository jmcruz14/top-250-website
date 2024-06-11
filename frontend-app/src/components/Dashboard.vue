<template>
  <div>

    <div class="mx-4 grid grid-cols-3 gap-8">
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

    <!-- TODO: add graph here then package into a separate component -->


    <pre>
      {{ data }}
    </pre>
  </div>
</template>


<script>
import { ref, computed } from 'vue'
import { useComputeList } from '~/composables/useComputeList';

import Widgets from './dashboard-widgets';

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
    Card
  },
  setup (props, { emit }) {
    const data = computed(() => props?.data)
    const lastUpdate = computed(() => props?.lastUpdate)
    const publishDate = computed(() => props?.publishDate)
    const { 
      calculateAverageRating,
      calculateAverageClassicRating,
      calculateRange,
      calculateMedian
    } = useComputeList();    

    return {
      calculateAverageRating,
      calculateAverageClassicRating,
      calculateRange,
      calculateMedian,

      data,
      lastUpdate,
      publishDate
    }
  }
}
</script>