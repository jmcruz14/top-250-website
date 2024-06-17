import { useRuntimeConfig } from '#app'
import { cloneDeep } from 'lodash'

/**
 * Fetches the most recent list history
 * stored in the database.
 * @param {Number} id numerical id
 * @param {Boolean} showAll flag to toggle retrieval of all metadata
 * @returns {Promise<Object>}
 */
export async function fetchListHistory(id) {
  try {
    const config = useRuntimeConfig();
    const apiUrl = config?.public?.apiUrl;
    const response = await $fetch(`${apiUrl}/list-history`, {
      method: 'GET',
      params: { id }
    });

    const data = response?.data;
    const dataMap = new Map(data.map((obj) => [obj?.film_id, obj]));
    const responseMap = cloneDeep(response);
    responseMap.data = dataMap

    return {response, responseMap}
  } catch (error) {
    console.error('Error fetching list history:', error);
    throw new Error('Failed to fetch list history');
  }
}

export async function fetchMovie(id) {
  try {
    const config = useRuntimeConfig();
    const apiUrl = config?.public?.apiUrl;
    const response = await $fetch(`${apiUrl}/movie/fetch/${id}`, {
      method: 'GET'
    })
    const data = response?.data
    return data
  } catch (error) {
    console.error('Error fetching movie:', error);
    throw new Error('Failed to fetch movie');
  }
}


// export async function fetchMovie(id) {
//   try {

//   } catch (error) {
//     console.error('')
//   }
// }