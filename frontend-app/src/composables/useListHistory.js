import { useRuntimeConfig } from '#app'

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
    return response;
  } catch (error) {
    console.error('Error fetching list history:', error);
    throw new Error('Failed to fetch list history');
  }
}

// export async function fetchMovie(id) {
//   try {

//   } catch (error) {
//     console.error('')
//   }
// }