<template>
  <div class="flex flex-col justify-center gap-2">
    <span class="font-weight-500 text-3xl font-proportional text-center">Top 250 Filipino Movies Dashboard</span>
    <TestGraph />
  </div>
</template>

<script>
import { definePageMeta, useSeoMeta } from '#imports'
import TestGraph from '@/components/TestGraph'
// import ... from 'd3'

export default {
  components: {
    TestGraph
  },
  setup () {
    definePageMeta({ layouts: 'Generic '})
    useSeoMeta({
      title: 'Top 250 Dashboard',
      description: 'Front-end dashboard for the Letterboxd Top 250 Filipino list',
    })
  }
}

</script>