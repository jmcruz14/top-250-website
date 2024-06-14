<template>
  <div class="flex flex-col justify-center gap-2">
    <span class="font-weight-500 text-3xl font-proportional text-center pt-4">Top 250 Filipino Movies Dashboard</span>
    <span class="font-weight-300 text-xl font-tabular text-center">A Simple Dashboard by Jay</span>
            
    <!-- TODO: throw in animations -->
    <div class="my-4">
      <div v-if="loadingState" class="m-4 flex flex-col">
        <ProgressBar style="height: 10px;" mode="indeterminate" />
        <span class="self-center">Loading...</span>
      </div>
      <Dashboard v-else 
        :data="response?.data" 
        :data-map="responseMap?.data"
        :last-update="lastUpdate" 
        :publish-date="publishDate" 
      />
    </div>

  </div>
</template>

<script>
import { definePageMeta, useSeoMeta } from '#imports'
import { onMounted, ref, watch } from 'vue'
import { getDate } from '~/utils/list'
import { fetchListHistory } from '~/composables/useFilmApi'

// import TabMenu from 'primevue/tabmenu';
import Panel from 'primevue/panel';
import ProgressBar from 'primevue/progressbar';

export default {
  components: {
    ProgressBar,
    // TabMenu,
    Panel,

    // Dashboard,
    // TestGraph
  },
  setup () {
    definePageMeta({ layouts: 'Generic' })
    useSeoMeta({
      title: 'Top 250 Dashboard',
      description: 'Front-end dashboard for the Letterboxd Top 250 Filipino list',
    })

    const loadingState = ref(false);
    const selectedTabIndex = ref(0);
    const items = ref([
      { label: 'Dashboard', icon: 'pi pi-home' },
      { label: 'About', icon: 'pi pi-question' },
    ])

    const lastUpdate = ref(null);
    const publishDate = ref(null);

    // 2020-12-02T13:32:32.647000
    const response = ref(null);
    const responseMap = ref(null);
    onMounted(async () => {
        loadingState.value = true
        // response.value = await fetchListHistory(15294077)
        const results = await fetchListHistory(15294077)
        
        response.value = results?.response;
        responseMap.value = results?.responseMap;

        loadingState.value = false

        lastUpdate.value = getDate(response?.value?.last_update, 'MMMM dd yyyy')
        publishDate.value = getDate(response?.value?.publish_date, 'MMMM dd yyyy')
      }
    )
    
    watch(selectedTabIndex, (v) => {
      console.warn('v-change', v)
    })

    return {
      loadingState,
      selectedTabIndex,
      response,
      responseMap,
      items,

      lastUpdate,
      publishDate
    }
  }
}

</script>