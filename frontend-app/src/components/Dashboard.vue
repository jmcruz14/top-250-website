<template>
  <div class="border border-sky-500">
    <!-- <div class="grid grid-cols-3 mx-4 gap-8">
      <Card :pt="{
        title: 'text-md',
        content: 'py-0'
        }">
        <template #title>
          <div class="flex justify-between align-center">
            <div class="flex items-center gap-2">
              <span>
                Average Rating
              </span>
              <Badge value="!" size="medium"/>
            </div>
            <div class="bg-green-100 p-2 flex" style="width:2.5rem;height:2.5rem;border-radius:10px">
              <i class="pi pi-chart-line text-green-500 text-2xl"></i>
            </div>
          </div>
        </template>
        <template #content>
          <span class="text-lg">
            {{ data ? calculateAverageRating(data) : null }}
          </span>
        </template>
      </Card>

      <Card :pt="{
        root: 'backdrop',
        title: 'text-md text-white',
        content: 'py-0 text-white flex justify-between items-center'
        }">
        <template #title>
          <div class="flex justify-between align-center">
            <div>
              <span>
                Average Classic Rating
              </span>
              <Badge value="!" size="medium"/>
            </div>
          </div>
        </template>
        <template #content>
          <span class="text-lg">
            {{ data ? calculateAverageClassicRating(data) : null }}
          </span>
          <div class="bg-green-100 p-2 flex" style="width:2.5rem;height:2.5rem;border-radius:10px">
            <i class="pi pi-chart-bar text-green-500 text-2xl"></i>
          </div>
        </template>
      </Card>

      
    </div> -->

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