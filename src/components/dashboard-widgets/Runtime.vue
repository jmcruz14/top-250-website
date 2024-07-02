<template>
  <Card>
    <template #title>Runtime Data</template>
    <template #subtitle>just some numbers</template>
    <template #content>
        <ul class="list-disc ml-2">
          <li>
            <span><b>Shortest Film:</b> sdfasdfa</span>
          </li>
          <li>
            <span><b>Longest Film:</b> adsfsaf</span>
          </li>
          <li>
            <span><b>Average Runtime:</b> His works run at an average of mins.</span>
          </li>
        </ul>
      </template>
  </Card>
  <div ref="runtimeDiv" class="drop-shadow-md">
  </div>
</template>

<script>
import { isUndefined, omit } from 'lodash';
import { ref, onMounted, computed, toRefs } from 'vue';
import Card from 'primevue/card'
import { fetchMovieAgg } from '@/composables/useFilmApi';
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
    const { createScatterPlot } = useD3();
    const runtimeDiv = ref(null);

    onMounted(async () => {
      // NOTE: insert flag to filter out lav diaz movies
      const longestFilm = [
        {
          "$match": {
            "runtime": {"$ne": null}
          }
        },
        {
          "$sort": {
            "runtime": -1
          }
        },
        {
          "$limit": 1
        },
        {
          "$project": {
            "_id": 1,
            "film_title": 1,
            "director": 1
          }
        }
      ]
      const shortestFilm = [
        {
          "$match": {
            "runtime": {"$ne": null}
          }
        },
        {
          "$sort": {
            "runtime": 1
          }
        },
        {
          "$limit": 1
        },
        {
          "$project": {
            "_id": 1,
            "film_title": 1,
            "director": 1
          }
        }
      ]
      const longestFilmResult = await fetchMovieAgg(longestFilm);
      const shortestFilmResult = await fetchMovieAgg(shortestFilm);

      console.warn('longest-film', longestFilmResult?.data, shortestFilmResult?.data)

      const frequencyQuery = [
        {
          "$match": {
              "runtime": {"$ne": null}
          }
        },
        {
          "$sortByCount": "$runtime"
        },
        {
          "$sort": {
              "_id": -1
          }
        },
        {
          "$addFields": {
            "runtime": "$_id"
          }
        }
      ];
      const results = await fetchMovieAgg(frequencyQuery);
      const data = results?.data;
      
      const chart = await createScatterPlot(
        data, 'count', 'runtime', '#f1f5f9', 'Count', 'Runtime', true
      )

      runtimeDiv.value.appendChild(chart)
      
    })

    return {
      runtimeDiv,
    }
  }
}
</script>