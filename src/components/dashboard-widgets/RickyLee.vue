<template>
  <div class="flex flex-row">
    <Card class="w-1/2 h-fit">
      <template #title>
        <div class="flex flex-row gap-2 items-center">
          <Avatar 
            image="https://assets.mubicdn.net/images/notebook/post_images/34742/images-w1400.jpg?1642102960"
            size="large"
            shape="square"
          ></Avatar>
          <span>
            Ricky Lee Counter
          </span>
        </div>
      </template>
      <template #content>
        <blockquote
          cite="https://mubi.com/en/notebook/posts/ricky-lee-life-beyond-the-screenplay"
        >
          <p class="text-xs bg-gray-300 p-3 italic">
            There is no corner in Philippine cinema, television, and literature that remains untouched and unshaped by Ricky Lee.
          </p>
          <footer class="text-sm pt-3 pb-6">- Jason Tan Liwag for <cite>
            <a href="https://mubi.com/en/notebook/posts/ricky-lee-life-beyond-the-screenplay" class="hover:underline">
              MUBI
            </a>
          </cite></footer>
        </blockquote>
        
        <ul class="list-disc ml-2">
          <li>
            <span><b>{{ percent }}</b>% ({{ totalCount }} of 250) of films in the list are written by Ricky Lee.</span>
          </li>
          <li>
            <span>The list currently has an average runtime of <b>{{ avgRuntime }}</b> mins.</span>
          </li>
        </ul>
      </template>
    </Card>
  </div>
</template>

<script>
import { isUndefined } from 'lodash';
import { ref, onMounted, computed, toRefs } from 'vue';
import Card from 'primevue/card'
import Avatar from 'primevue/avatar';
import { fetchMovieAgg } from '@/composables/useFilmApi';

export default {
  components: {
    Avatar,
    Card
  },
  async setup (props) {
    // A component is considered SUSPENSEFUL in two ways
    // 1. having an async setup()
    // 2. top level await (in script setup
    const totalCount = ref(null);
    const percent = ref(null);
    const avgRuntime = ref(null);

    onMounted(async () => {
			const query = [
				{
					"$match": { 
						"$or": [ {"writer": {"$eq": "Ricardo Lee"}}, {"writers": {"$eq": "Ricardo Lee"}} ]
					}
				}
			]
      const results = await fetchMovieAgg(query);

      totalCount.value = results?.length
      percent.value = ((totalCount?.value / 250) * 100).toPrecision(4);
      avgRuntime.value = (results?.data?.reduce((acc, film) => {
        return acc += film?.runtime
      }, 0) / totalCount.value).toPrecision(4);
    })

    
    return {
      totalCount,
      percent,
      avgRuntime,
    }
  }
}
</script>
