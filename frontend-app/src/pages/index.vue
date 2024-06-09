<template>
  <div class="flex flex-col justify-center gap-2">
    <span class="font-weight-500 text-3xl font-proportional text-center pt-4">Top 250 Filipino Movies Dashboard</span>
    <span class="font-weight-300 text-xl font-tabular text-center">A Simple Dashboard by Jay</span>
    <!-- <TabMenu 
      :model="items"
      :activeIndex="selectedTabIndex"
    /> -->

    <div class="mx-4">
      <ProgressBar style="height: 10px;" v-if="loadingState" mode="indeterminate" />
      <div v-else class="mx-4 grid grid-cols-2 gap-8">
        <!-- add border border-sky-500 to panel if needed -->
        <Panel header="Last update:" class="font-proportional drop-shadow-md" toggleable collapsed>
          <span class="text-xl font-tabular">{{ lastUpdate }}</span>
        </Panel>
        <Panel header="Publish date:" class="font-proportional drop-shadow-md" toggleable collapsed>
          <span class="text-xl font-tabular">{{ publishDate }}</span>
        </Panel>
      </div>
    </div>

    <Dashboard :data="response?.data" />
  </div>
</template>

<script>
import { definePageMeta, useSeoMeta } from '#imports'
import { onMounted, ref, watch } from 'vue'
import { getDate } from '~/utils/list'
import { fetchListHistory } from '~/composables/useListHistory'

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
    const response = ref(null)
    onMounted(async () => {
        loadingState.value = true
        response.value = await fetchListHistory(15294077, true)
        loadingState.value = false

        lastUpdate.value = getDate(response?.value?.last_update, 'MMMM dd yyyy hh:mm b')
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
      items,

      lastUpdate,
      publishDate
    }
  }
}

</script>