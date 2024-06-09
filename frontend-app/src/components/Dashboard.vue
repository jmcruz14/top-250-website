<template>
  <div class="border border-sky-500">
    <div class="grid grid-cols-3 mx-4 gap-8">
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

      
    </div>
    <pre>
      {{ data }}
    </pre>
  </div>
</template>


<script>
import { isNull } from 'lodash'
import { ref, computed } from 'vue'

import Widgets from './dashboard-widgets';

import Badge from 'primevue/badge';
import Card from 'primevue/card';

export default {
  props: {
    data: Object
  },
  components: {
    Badge,
    Card
  },
  setup (props, { emit }) {
    const data = computed(() => props?.data)

    function calculateAverageRating (data) {
      const listLength = data?.length;
      const nullCount = data?.filter(i => isNull(i?.rating)).length;
      const sum = data?.reduce((a, item) => {
        const rating = item?.rating;
        if (!isNull(rating)) return a + rating;
        return a
      }, 0)
      return (sum / (listLength - nullCount)).toFixed(2)
    }

    function calculateAverageClassicRating (data) {
      const listLength = data?.length;  
      const nullCount = data?.filter(i => isNull(i?.classic_rating)).length;
      const sum = data?.reduce((a, item) => {
        const rating = item?.classic_rating;
        if (!isNull(rating)) return a + rating;
        return a
      }, 0)
      return (sum / (listLength - nullCount)).toFixed(2)
    }

    // function calculateAverageClassicRating

    return {
      calculateAverageRating,
      calculateAverageClassicRating,

      data
    }
  }
}
</script>