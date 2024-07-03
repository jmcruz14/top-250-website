<template>
  <div class="flex flex-row-reverse">
    <Card class="w-1/2 h-fit">
      <template #title>Runtime Data</template>
      <template #content>
          <ul class="list-disc ml-2">
            <li>
              <span><b>Shortest Film:</b> 
                {{ shortestFilmResult?.film_title ? shortestFilmResult?.film_title : null }} 
                ({{ shortestFilmResult?.director?.[0] ? shortestFilmResult?.director?.[0] : null }} - 
                 {{ shortestFilmResult?.runtime ? shortestFilmResult?.runtime : null }} minutes)
                </span>
            </li>
            <li>
              <span><b>Longest Film:</b> 
                {{ longestFilmResult?.film_title ? longestFilmResult?.film_title : null }} 
                ({{ longestFilmResult?.director?.[0] ? longestFilmResult?.director?.[0] : null }} - 
                 {{ longestFilmResult?.runtime ? longestFilmResult?.runtime : null }} minutes)</span>
            </li>
            <li>
              <span><b>Average Runtime:</b> The list has an average runtime of <b>{{ averageOverallRuntime?.avgRuntime.toPrecision(4) }}</b> minutes</span>
            </li>
          </ul>
        </template>
    </Card>
  </div>
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
    const { createHistogram } = useD3();
    const shortestFilmResult = ref(null);
    const longestFilmResult = ref(null);
    const averageOverallRuntime = ref(null);
    const runtimeDiv = ref(null);

    onMounted(async () => {
      // NOTE: insert flag to filter out lav diaz movies
      const shortestAndLongestFilm = [
        {
          "$match": {
            "runtime": { "$ne": null }
          }
        },
        {
          "$facet": {
            "longestFilm": [
              { "$sort": { "runtime": -1 } },
              { "$limit": 1 },
              {
                "$project": {
                  "_id": 1,
                  "film_title": 1,
                  "director": 1,
                  "runtime": 1
                }
              }
            ],
            "shortestFilm": [
              { "$sort": { "runtime": 1 } },
              { "$limit": 1 },
              {
                "$project": {
                  "_id": 1,
                  "film_title": 1,
                  "director": 1,
                  "runtime": 1
                }
              }
            ],
            "averageRuntime": [
                { "$group": {
                    "_id": 1,
                    "avgRuntime": { "$avg": "$runtime" }
                }}
            ]
          }
        }
      ];
      const shortestAndLongestResult = await fetchMovieAgg(shortestAndLongestFilm);
      shortestFilmResult.value = shortestAndLongestResult?.data?.[0]?.shortestFilm?.[0];
      longestFilmResult.value = shortestAndLongestResult?.data?.[0]?.longestFilm?.[0];
      averageOverallRuntime.value = shortestAndLongestResult?.data?.[0]?.averageRuntime?.[0];

      const frequencyQuery = [
        {
          "$match": {
              "runtime": {"$ne": null}
          }
        },
        {
          "$addFields": {
            "runtimeBin": {
              "$switch": {
                "branches": [
                  { "case": { "$lte": ["$runtime", 60] }, "then": { "bin": "<60", "lower": -Infinity, "upper": 60 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 60] }, { "$lte": ["$runtime", 70] }] }, "then": { "bin": "61-70", "lower": 61, "upper": 70 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 70] }, { "$lte": ["$runtime", 80] }] }, "then": { "bin": "71-80", "lower": 71, "upper": 80 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 80] }, { "$lte": ["$runtime", 90] }] }, "then": { "bin": "81-90", "lower": 81, "upper": 90 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 90] }, { "$lte": ["$runtime", 100] }] }, "then": { "bin": "91-100", "lower": 91, "upper": 100 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 100] }, { "$lte": ["$runtime", 110] }] }, "then": { "bin": "101-110", "lower": 101, "upper": 110 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 110] }, { "$lte": ["$runtime", 120] }] }, "then": { "bin": "111-120", "lower": 111, "upper": 120 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 120] }, { "$lte": ["$runtime", 130] }] }, "then": { "bin": "121-130", "lower": 121, "upper": 130 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 130] }, { "$lte": ["$runtime", 140] }] }, "then": { "bin": "131-140", "lower": 131, "upper": 140 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 140] }, { "$lte": ["$runtime", 150] }] }, "then": { "bin": "141-150", "lower": 141, "upper": 150 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 150] }, { "$lte": ["$runtime", 160] }] }, "then": { "bin": "151-160", "lower": 151, "upper": 160 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 160] }, { "$lte": ["$runtime", 170] }] }, "then": { "bin": "161-170", "lower": 161, "upper": 170 } },
                  { "case": { "$and": [{ "$gt": ["$runtime", 170] }, { "$lte": ["$runtime", 180] }] }, "then": { "bin": "171-180", "lower": 171, "upper": 180 } },
                  { "case": { "$gt": ["$runtime", 180] }, "then": { "bin": ">180", "lower": 181, "upper": Infinity } }
                ],
                "default": { "bin": "Unknown", "lower": null, "upper": null }
              }
            }
          }
        },
        {
          "$group": {
            "_id": "$runtimeBin",
            "count": { "$sum": 1 },
            "lower": { "$first": { "$or": ["$runtimeBin.lower", 0]} },
            "upper": { "$first": { "$or": ["$runtimeBin.upper", null]} }
          }
        },
        {
          "$project": {
            "_id": "$_id.bin",
            "bin": {
              "lower": "$_id.lower",
              "upper": "$_id.upper"
            },
            "count": 1,
          }
        },
        {
          "$sort": {
            "bin.lower": 1
          }
        }
      ];
      const results = await fetchMovieAgg(frequencyQuery);
      const data = results?.data;

      const chart = await createHistogram(
        data, 'bin', 'count', '#f1f5f9', 'Runtime (in minutes)', 'Runtime Distribution',
        false, 1000
      )

      runtimeDiv.value.appendChild(chart)
    })

    return {
      runtimeDiv,
      shortestFilmResult,
      longestFilmResult,
      averageOverallRuntime,
    }
  }
}
</script>