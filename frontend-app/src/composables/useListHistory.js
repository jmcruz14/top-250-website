import { useRuntimeConfig } from '#app'

export async function fetchListHistory(id, showAll) {
  try {
    const config = useRuntimeConfig();
    const apiUrl = config?.public?.apiUrl;
    const fetchMovies = showAll ? true : false
    const response = await $fetch(`${apiUrl}/list-history`, {
      method: 'GET',
      params: { id, fetch_movies: fetchMovies }
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